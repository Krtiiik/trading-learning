"""Command line entry point: `uv run trading ...`."""

import argparse
import sys
from pathlib import Path

from trading.data.bars import GRANULARITIES
from trading.data.manifest import ManifestError, build_manifest, read_manifest, verify_manifest
from trading.data.providers import Provider, ProviderError, YahooProvider
from trading.data.storage import BarStore, default_data_dir
from trading.data.universe import load_universe
from trading.data.update import update_symbol
from trading.data.validation import validate_crypto, validate_daily


def main(argv: list[str] | None = None, provider: Provider | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")  # some Binance symbols are not Latin-1
    parser = _parser()
    args = parser.parse_args(argv)
    return args.command(args, provider)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trading", description=__doc__)
    commands = parser.add_subparsers(required=True, metavar="command")

    fetch = commands.add_parser(
        "fetch",
        help="download ETF bars into the local store",
        description="Download bars for the universe (or the given symbols) and check them. "
        "Symbols already stored get only the bars since their last stored bar.",
    )
    fetch.add_argument("--symbols", nargs="+", metavar="SYMBOL", help="instead of the universe")
    fetch.add_argument(
        "--universe", type=Path, help="TOML file listing symbols (default: universe.toml)"
    )
    fetch.add_argument("--granularity", choices=GRANULARITIES, default="1d")
    fetch.add_argument(
        "--full", action="store_true", help="re-download the whole history of each symbol"
    )
    fetch.add_argument("--data-dir", type=Path, help="store root (default: data/)")
    fetch.set_defaults(command=_fetch)

    from trading.data.rebuild import DEFAULT_STEPS, STEPS

    rebuild = commands.add_parser(
        "rebuild",
        help="rebuild the crypto datasets of the store from the Binance public archive",
        description="Download and rebuild the crypto datasets from nothing: daily bars for every "
        "USDT pair, the point-in-time universe, then hourly bars and perpetual-futures series "
        "for pairs that were ever universe members. Downloads are cached under data/raw/.",
    )
    rebuild.add_argument(
        "--steps",
        nargs="+",
        choices=STEPS,
        default=list(DEFAULT_STEPS),
        help=f"which steps to run, in their fixed order (default: {' '.join(DEFAULT_STEPS)})",
    )
    rebuild.add_argument("--data-dir", type=Path, help="store root (default: data/)")
    rebuild.set_defaults(command=_rebuild)

    verify = commands.add_parser(
        "verify",
        help="check stored datasets against their manifests",
        description="Compare each dataset's files with its manifest. Without --deep only names, "
        "sizes and modification times are compared; --deep re-hashes the contents.",
    )
    verify.add_argument("datasets", nargs="*", help="dataset names (default: every manifest found)")
    verify.add_argument("--deep", action="store_true", help="re-hash file contents")
    verify.add_argument(
        "--quality",
        action="store_true",
        help="also run the sanity checks on the crypto spot bars and summarise what they find",
    )
    verify.add_argument("--data-dir", type=Path, help="store root (default: data/)")
    verify.set_defaults(command=_verify)

    from trading.research.cli import add_research_commands

    add_research_commands(commands)
    return parser


def _fetch(args: argparse.Namespace, provider: Provider | None) -> int:
    provider = provider or YahooProvider()
    symbols = [symbol.upper() for symbol in args.symbols] if args.symbols else load_universe(
        args.universe
    )
    store = BarStore(args.data_dir)
    width = max(len(symbol) for symbol in symbols)
    failed: list[str] = []

    plural = "" if len(symbols) == 1 else "s"
    print(f"Fetching {args.granularity} bars for {len(symbols)} symbol{plural} into {store.root}")
    for symbol in symbols:
        try:
            result = update_symbol(provider, store, symbol, args.granularity, full=args.full)
        except ProviderError as error:
            failed.append(symbol)
            print(f"{symbol:<{width}}  FAILED  {error}", file=sys.stderr)
            continue

        reason = f" ({result.reason})" if result.reason else ""
        print(
            f"{symbol:<{width}}  {result.mode:<11}  {result.total_bars:>6} bars"
            f"  {result.new_bars:+d}{reason}"
        )
        for issue in validate_daily(store.read(symbol, args.granularity)):
            print(f"{'':<{width}}  warning: {issue}")

    if store.symbols(args.granularity):
        manifest = build_manifest(store.root, args.granularity, provider.name)
        print(f"Dataset {manifest.dataset}: {len(manifest.files)} files, id {manifest.short_id}")
    if failed:
        print(f"Failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


def _rebuild(args: argparse.Namespace, provider: Provider | None) -> int:
    from trading.data.rebuild import rebuild

    rebuild(args.data_dir, provider, steps=args.steps)  # type: ignore[arg-type]
    return 0


def _verify(args: argparse.Namespace, provider: Provider | None) -> int:
    root = Path(args.data_dir) if args.data_dir else default_data_dir()
    datasets = args.datasets or sorted(
        path.parent.relative_to(root).as_posix() for path in root.rglob("MANIFEST.json")
    )
    if not datasets:
        print(f"No manifests under {root}; run `uv run trading rebuild`", file=sys.stderr)
        return 1
    stale = 0
    for dataset in datasets:
        try:
            problems = verify_manifest(root, dataset, deep=args.deep)
            manifest = read_manifest(root, dataset)
        except ManifestError as error:
            print(f"{dataset}: {error}", file=sys.stderr)
            stale += 1
            continue
        state = "ok" if not problems else f"{len(problems)} problems"
        print(f"{dataset}: {len(manifest.files)} files, id {manifest.short_id}, {state}")
        for problem in problems[:10]:
            print(f"  {problem}")
        stale += bool(problems)
        if args.quality and dataset.startswith("binance/spot/"):
            _quality(root, dataset.rsplit("/", 1)[1])
    return 1 if stale else 0


def _quality(root: Path, granularity: str) -> None:
    """Which sanity checks fire on the crypto spot bars, and for which symbols (no dates)."""
    store = BarStore(root, "binance/spot")
    found: dict[str, list[str]] = {}
    for symbol in store.symbols(granularity):  # type: ignore[arg-type]
        for issue in validate_crypto(store.read(symbol, granularity), granularity):  # type: ignore[arg-type]
            found.setdefault(issue.check, []).append(f"{symbol} ({len(issue.dates)})")
    for check, symbols in sorted(found.items()):
        shown = ", ".join(symbols[:12]) + (f", +{len(symbols) - 12} more" if len(symbols) > 12 else "")
        print(f"  {check}: {len(symbols)} symbols: {shown}")
    if not found:
        print("  no issues")
