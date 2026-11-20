"""`trading research ...` commands: the procedures of the research process."""

import argparse
import sys
from datetime import date

from trading.research.split import DEV_END, DEV_START, TRAIN_END


def add_research_commands(commands) -> None:
    research = commands.add_parser(
        "research",
        help="register, run and review hypotheses",
        description="The research process. See research/README.md.",
    )
    actions = research.add_subparsers(required=True, metavar="action")

    check = actions.add_parser("check", help="validate a hypothesis file and its registration")
    check.add_argument("hypothesis", help="hypothesis id, like H1001")
    check.set_defaults(command=_check)

    run = actions.add_parser(
        "run",
        help="run a registered hypothesis on a segment and write the run record",
        description="Runs the hypothesis's single primary test. Refuses when the hypothesis file "
        "is not committed, has changed since registration, or may not run on that segment yet.",
    )
    run.add_argument("hypothesis", help="hypothesis id, like H1001")
    run.add_argument("--segment", choices=("train", "dev", "test"), required=True)
    run.add_argument("--rerun-reason", help="why an earlier dev run is invalid (recorded)")
    run.set_defaults(command=_run)

    status = actions.add_parser("status", help="show where hypotheses stand on the claim ladder")
    status.add_argument("hypothesis", nargs="?", help="one hypothesis id (default: all)")
    status.set_defaults(command=_status)

    catalogue = actions.add_parser(
        "catalogue", help="recompute statuses, update hypothesis files, regenerate CATALOGUE.md"
    )
    catalogue.set_defaults(command=_catalogue)

    mde = actions.add_parser(
        "mde",
        help="minimum detectable effect, to judge a hypothesis testable before running it",
        description="The smallest true effect the train and dev segments can detect. Give the "
        "standard error's ingredients for the kind of estimate the hypothesis uses.",
    )
    mde.add_argument("kind", choices=("sharpe", "sharpe-difference", "mean"))
    mde.add_argument("--start", default="2019-07-01", help="first day of usable train data")
    mde.add_argument("--correlation", type=float, default=0.8, help="sharpe-difference: of the two return series")
    mde.add_argument("--deviation", type=float, help="mean: standard deviation of one observation")
    mde.add_argument("--per-year", type=float, default=365.0, help="mean: observations per year")
    mde.add_argument("--overlap", type=int, default=1, help="mean: periods each observation spans")
    mde.add_argument("--alpha", type=float, default=0.05)
    mde.add_argument("--power", type=float, default=0.80)
    mde.set_defaults(command=_mde)

    skeptic = actions.add_parser(
        "skeptic", help="write the Skeptic's verdict into a hypothesis file"
    )
    skeptic.add_argument("hypothesis")
    skeptic.add_argument(
        "--verdict",
        choices=("confirmed", "refuted", "audited"),
        required=True,
        help="confirmed or refuted for a supported finding; audited for a review of any other "
        "status (it records that the review happened and changes no status)",
    )
    skeptic.add_argument("--reason", required=True, help="one or two sentences; details go in the file body")
    skeptic.set_defaults(command=_skeptic)

    seal = actions.add_parser(
        "open-seal",
        help="open the test seal, once, for at most five confirmed finalists",
        description="A one-time, recorded act. Every finalist must be 'confirmed' and the "
        "finalist list, specifications and pass rules must already be committed.",
    )
    seal.add_argument("finalists", nargs="+", metavar="HYPOTHESIS")
    seal.set_defaults(command=_open_seal)


def _records():
    from trading.research.split import records_dir

    return records_dir()


def _check(args: argparse.Namespace, provider=None) -> int:
    from trading.research import registry

    try:
        hypothesis = registry.load(_records(), args.hypothesis)
        problems = registry.validate(hypothesis)
        if problems:
            print(f"{hypothesis.id}: " + "; ".join(problems), file=sys.stderr)
            return 1
        commit = registry.check_registered(hypothesis)
    except registry.RegistryError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"{hypothesis.id} is registered (commit {commit[:10]}, spec {hypothesis.spec_hash[:12]})")
    return 0


def _run(args: argparse.Namespace, provider=None) -> int:
    from trading.data.manifest import ManifestError
    from trading.research import harness, registry
    from trading.research.split import SealedError

    try:
        record = harness.run(args.hypothesis, args.segment, rerun_reason=args.rerun_reason)
    except (harness.HarnessError, registry.RegistryError, SealedError, ManifestError) as error:
        print(f"Refused: {error}", file=sys.stderr)
        return 1
    doubled = record["double_cost"]
    print(f"{record['run']} on {record['segment']}: estimate {record['estimate']:+.4f}, "
          f"p = {record['p_value']:.4f} (one-sided, {record['direction']}), n = {record['n']}")
    if doubled:
        print(f"  at double cost: estimate {doubled['estimate']:+.4f}, p = {doubled['p_value']:.4f}")
    print(f"  record: {record['path']}")
    print("  next: commit the record, then `uv run trading research catalogue`")
    return 0


def _status(args: argparse.Namespace, provider=None) -> int:
    from trading.research import ladder

    table = ladder.load_standings(_records())
    chosen = [table[args.hypothesis]] if args.hypothesis else list(table.values())
    for standing in chosen:
        print(f"{standing.hypothesis.id}  {standing.status:<14}  {standing.hypothesis.title}")
        for reason in standing.reasons:
            print(f"       {reason}")
    return 0


def _catalogue(args: argparse.Namespace, provider=None) -> int:
    from trading.research.catalogue import write_catalogue

    path, table = write_catalogue(_records())
    print(f"Wrote {path} ({len(table)} hypotheses)")
    return 0


def _mde(args: argparse.Namespace, provider=None) -> int:
    from trading import stats

    spans = {
        "train": (date.fromisoformat(args.start), TRAIN_END.date()),
        "dev": (DEV_START.date(), DEV_END.date()),
    }
    for name, (first, last) in spans.items():
        years = ((last - first).days + 1) / 365
        if args.kind == "sharpe":
            error = stats.sharpe_standard_error(years)
        elif args.kind == "sharpe-difference":
            error = stats.sharpe_difference_standard_error(years, args.correlation)
        else:
            if args.deviation is None:
                print("mean needs --deviation", file=sys.stderr)
                return 1
            error = stats.mean_standard_error(args.deviation, int(years * args.per_year), args.overlap)
        effect = stats.minimum_detectable_effect(error, args.alpha, args.power)
        print(f"{name}: {years:.2f} years, standard error {error:.4f}, minimum detectable effect "
              f"{effect:.4f} (one-sided alpha {args.alpha}, power {args.power})")
    return 0


def _skeptic(args: argparse.Namespace, provider=None) -> int:
    from trading.research import registry

    from trading.research import ladder

    hypothesis = registry.load(_records(), args.hypothesis)
    status = ladder.load_standings(_records())[hypothesis.id].status
    decided = status in (ladder.SUPPORTED, ladder.CONFIRMED, ladder.REFUTED)
    if decided == (args.verdict == "audited"):
        wanted = "confirmed or refuted" if decided else "audited"
        print(f"Refused: {hypothesis.id} is '{status}'; its review ends in {wanted}", file=sys.stderr)
        return 1
    verdict = {"verdict": args.verdict, "date": date.today().isoformat(), "reason": args.reason}
    registry.set_field(hypothesis, "skeptic", verdict)
    print(f"{hypothesis.id}: Skeptic verdict '{args.verdict}' written to {hypothesis.path.name}")
    return 0


def _open_seal(args: argparse.Namespace, provider=None) -> int:
    from trading.research import ladder, registry
    from trading.research.split import SealedError, open_seal

    records = _records()
    table = ladder.load_standings(records)
    not_confirmed = [
        name for name in args.finalists
        if name not in table or table[name].status != ladder.CONFIRMED
    ]
    if not_confirmed:
        print(f"Refused: not confirmed: {', '.join(not_confirmed)}", file=sys.stderr)
        return 1
    root = registry.repository_root(records)
    try:
        record = open_seal(args.finalists, registry.head_commit(root), records)
    except SealedError as error:
        print(f"Refused: {error}", file=sys.stderr)
        return 1
    print(f"Seal opened at {record['opened_at']} for {', '.join(record['finalists'])}. "
          "Commit research/SEAL.json now.")
    return 0
