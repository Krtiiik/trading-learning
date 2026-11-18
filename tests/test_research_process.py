"""The research process: registration, the harness, the claim ladder, the catalogue, the CLI."""

import json
import sys
import textwrap
import uuid
from pathlib import Path

import pytest

from trading.cli import main
from trading.research import harness, ladder, registry
from trading.research.catalogue import write_catalogue
from trading.research.harness import HarnessError, LookaheadError
from trading.research.registry import RegistryError
from trading.research.runs import load_runs
from trading.research.split import SealedError, open_seal

from conftest import git

HYPOTHESIS = """\
---
id: {id}
title: {title}
family: time-series
origin: {origin}
claim: {claim}
status: registered
motivation: Published trend evidence from before 2023.
sources:
  - "A paper (2012)"
prediction:
  direction: {direction}
  size: about 0.3
  unit: difference in annualised net Sharpe ratio
primary_test:
  experiment: {experiment}
  description: Momentum weights against the equal-weight universe.
  params: {params}
decision:
  train: one-sided p-value enters Benjamini-Hochberg at 10%
  dev:
    min_ratio: 0.5
    min_size: 0.1
power:
  mde_train: 0.9
data:
  - binance/spot/1d
{extra}---

# Notes

Free text.
"""

EXPERIMENT = """\
import pandas as pd

from trading.research.evaluate import Result, evaluate_strategy, rebalance_labels


def panel(data, params):
    market = data.market("1d")
    close = market.frame("close")
    rising = (close / close.shift(SHIFT) - 1) > 0
    members = market.frame(market.member_next)
    weights = (rising & members).astype(float).div(members.sum(axis=1).clip(lower=1), axis=0)
    return weights.loc[rebalance_labels(market, "week")]


def test(ctx, panel):
    if "p_value" in ctx.params:
        return Result(ctx.params["estimate"], ctx.params["p_value"], 10, {},
                      DOUBLE_COST, ctx.params["p_value"])
    return evaluate_strategy(ctx, panel, "1d", draws=200)
"""


class Lab:
    """A temporary repository with records, experiments and the fake crypto Store."""

    def __init__(self, repo: Path, data_root: Path) -> None:
        self.repo, self.records, self.data_root = repo, repo / "research", data_root
        self.modules: list[str] = []

    def experiment(self, shift: int = 7, double_cost: str = 'ctx.params["estimate"] / 2', header: str = "") -> str:
        name = f"exp_{uuid.uuid4().hex[:10]}"
        source = header + EXPERIMENT.replace("SHIFT", str(shift)).replace("DOUBLE_COST", double_cost)
        (self.repo / f"{name}.py").write_text(source, encoding="utf-8")
        self.modules.append(name)
        return name

    def hypothesis(self, id: str = "H1001", commit: bool = True, experiment: str | None = None, **fields) -> Path:
        values = {
            "id": id, "title": f"Momentum {id}", "origin": "literature", "claim": "trading",
            "direction": "positive", "params": "{}", "extra": "",
            "experiment": experiment or self.experiment(),
        } | fields
        path = self.records / "hypotheses" / f"{id}-momentum.md"
        path.write_text(HYPOTHESIS.format(**values), encoding="utf-8")
        if commit:
            self.commit(f"register {id}")
        return path

    def commit(self, message: str) -> None:
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", message)

    def run(self, id: str = "H1001", segment: str = "train", **options) -> dict:
        return harness.run(id, segment, self.records, self.data_root, **options)  # type: ignore[arg-type]

    def fixed(self, id: str, p_value: float, estimate: float = 0.5, **fields) -> Path:
        """A hypothesis whose test returns a fixed result, to steer it along the ladder."""
        params = json.dumps({"p_value": p_value, "estimate": estimate})
        return self.hypothesis(id, params=params, **fields)


@pytest.fixture
def lab(repo, crypto_root, monkeypatch):
    monkeypatch.syspath_prepend(str(repo))
    monkeypatch.setenv("TRADING_RESEARCH_DIR", str(repo / "research"))
    monkeypatch.setenv("TRADING_DATA_DIR", str(crypto_root))
    lab = Lab(repo, crypto_root)
    yield lab
    for name in lab.modules:
        sys.modules.pop(name, None)


# Registry


def test_a_committed_hypothesis_is_registered(lab):
    path = lab.hypothesis()

    hypothesis = registry.load(lab.records, "H1001")

    assert registry.validate(hypothesis) == []
    assert len(registry.check_registered(hypothesis)) == 40
    assert hypothesis.path == path and hypothesis.family == "time-series"
    assert hypothesis.dev_rule == {"min_ratio": 0.5, "min_size": 0.1}


def test_an_uncommitted_hypothesis_is_not_registered(lab):
    lab.hypothesis(commit=False)

    with pytest.raises(RegistryError, match="not registered: commit"):
        registry.check_registered(registry.load(lab.records, "H1001"))


def test_changing_the_prediction_after_registration_is_refused(lab):
    path = lab.hypothesis()
    path.write_text(path.read_text().replace("min_size: 0.1", "min_size: 0.01"))
    lab.commit("quietly loosen the rule")

    with pytest.raises(RegistryError, match="changed since it was registered"):
        registry.check_registered(registry.load(lab.records, "H1001"))


def test_status_and_skeptic_verdict_may_change_without_touching_the_registration(lab):
    lab.hypothesis()
    before = registry.load(lab.records, "H1001")

    after = registry.set_field(before, "status", "candidate")
    after = registry.set_field(after, "skeptic", {"verdict": "refuted", "reason": "placebo: also works"})

    assert after.spec_hash == before.spec_hash
    assert after.meta["status"] == "candidate" and after.skeptic["verdict"] == "refuted"
    assert after.body == before.body and after.meta["decision"] == before.meta["decision"]
    assert registry.check_registered(after)
    with pytest.raises(RegistryError, match="frozen"):
        registry.set_field(after, "prediction", {"direction": "negative"})


@pytest.mark.parametrize(
    ("change", "problem"),
    [
        (("family: time-series", "family: astrology"), "family must be one of"),
        (("  direction: positive", "  direction: sideways"), "prediction.direction"),
        (("    min_size: 0.1\n", ""), "min_size must be a number"),
        (("    min_ratio: 0.5\n", ""), "min_ratio must be a number"),
        (("motivation: Published trend evidence from before 2023.\n", ""), "missing front-matter fields: motivation"),
        (("id: H1001", "id: H1002"), "file name must start with H1002-"),
    ],
)
def test_a_malformed_hypothesis_file_is_reported(lab, change, problem):
    path = lab.hypothesis(commit=False)
    path.write_text(path.read_text().replace(*change))

    problems = registry.validate(registry.parse(path.read_text(), path))

    assert any(problem in found for found in problems)


# Harness


def test_a_run_writes_its_own_record(lab):
    lab.hypothesis()

    record = lab.run("H1001", "train")

    stored = json.loads(record["path"].read_text())
    assert record["path"].parent.parent == lab.records / "runs"
    assert record["path"].name == "H1001-r01.json"
    assert stored["hypothesis"] == "H1001" and stored["segment"] == "train" and stored["number"] == 1
    assert stored["commit"] == git(lab.repo, "rev-parse", "HEAD").strip()
    assert stored["spec_hash"] == registry.load(lab.records, "H1001").spec_hash
    assert sorted(stored["data"]) == ["binance/spot/1d", "binance/universe"]
    assert stored["seed"] == 1001 and stored["params"] == {}
    assert 0 <= stored["p_value"] <= 1 and stored["double_cost"]["estimate"] is not None
    assert stored["lookahead_check"]["passed"] and len(stored["lookahead_check"]["cuts"]) == 3
    assert stored["metrics"]["window"]["last"].startswith("2022-12-31")
    assert stored["duration_seconds"] > 0 and stored["rerun_reason"] is None


def test_a_run_is_reproducible(lab):
    lab.hypothesis()

    first, second = lab.run(), lab.run()

    assert second["run"] == "H1001-r02"
    assert (first["estimate"], first["p_value"]) == (second["estimate"], second["p_value"])


def test_replay_repeats_the_train_run_without_recording_and_takes_other_parameters(lab):
    lab.hypothesis()
    recorded = lab.run("H1001", "train")

    same = harness.replay("H1001", lab.records, lab.data_root)
    fixed = harness.replay("H1001", lab.records, lab.data_root, p_value=0.2, estimate=9.0)

    assert same.estimate == recorded["estimate"] and same.p_value == recorded["p_value"]
    assert (fixed.estimate, fixed.p_value) == (9.0, 0.2)
    assert len(load_runs(lab.records)) == 1


def test_the_harness_refuses_an_unregistered_hypothesis(lab):
    lab.hypothesis(commit=False)

    with pytest.raises(RegistryError, match="not registered"):
        lab.run()
    assert load_runs(lab.records) == []


def test_the_harness_refuses_a_hypothesis_changed_after_registration(lab):
    path = lab.hypothesis()
    path.write_text(path.read_text().replace("about 0.3", "about 0.03"))

    with pytest.raises(RegistryError, match="changed since it was registered"):
        lab.run()


def test_the_harness_refuses_uncommitted_experiment_code(lab):
    name = lab.experiment()
    lab.hypothesis(experiment=name)
    with (lab.repo / f"{name}.py").open("a") as file:
        file.write("\n# tweak after the fact\n")

    with pytest.raises(HarnessError, match=f"commit first: {name}.py"):
        lab.run()


def test_an_experiment_may_not_read_the_store_itself(lab):
    lab.hypothesis(experiment=lab.experiment(header="from trading.data.storage import load_bars\n"))

    with pytest.raises(HarnessError, match="never from the Store"):
        lab.run()


def test_an_experiment_that_looks_ahead_is_caught_and_nothing_is_recorded(lab):
    lab.hypothesis(experiment=lab.experiment(shift=-1))  # compares with tomorrow's close

    with pytest.raises(LookaheadError, match="looks ahead"):
        lab.run()
    assert load_runs(lab.records) == []


def test_a_trading_claim_must_report_double_cost(lab):
    lab.fixed("H1001", 0.01, experiment=lab.experiment(double_cost="None"))

    with pytest.raises(HarnessError, match="double cost"):
        lab.run()


def test_dev_is_only_for_candidates_and_only_once(lab):
    lab.fixed("H1001", p_value=0.01)
    lab.fixed("H1002", p_value=0.40)
    with pytest.raises(HarnessError, match="not a candidate"):
        lab.run("H1001", "dev")
    lab.run("H1001", "train")
    lab.run("H1002", "train")

    lab.run("H1001", "dev")

    with pytest.raises(HarnessError, match="'rejected', not a candidate"):
        lab.run("H1002", "dev")
    with pytest.raises(HarnessError, match="already ran on dev"):
        lab.run("H1001", "dev")
    again = lab.run("H1001", "dev", rerun_reason="first run used a store with a missing month")
    assert again["rerun_reason"].startswith("first run used")


def test_an_exploration_hypothesis_skips_train_and_goes_straight_to_dev(lab):
    lab.fixed("H1001", p_value=0.01, origin="exploration")

    with pytest.raises(HarnessError, match="cannot be tested on it"):
        lab.run("H1001", "train")

    assert lab.run("H1001", "dev")["segment"] == "dev"


def test_the_test_segment_is_sealed_until_opened_for_a_finalist_and_then_runs_once(lab):
    lab.fixed("H1001", p_value=0.01)
    lab.fixed("H1002", p_value=0.01)
    lab.run("H1001", "train")
    with pytest.raises(SealedError, match="sealed"):
        lab.run("H1001", "test")

    open_seal(["H1001"], "abc123", lab.records)
    record = lab.run("H1001", "test")

    assert record["segment"] == "test"
    with pytest.raises(SealedError, match="already had its one test run"):
        lab.run("H1001", "test")
    with pytest.raises(SealedError, match="not one of the finalists"):
        lab.run("H1002", "test")


def test_a_real_test_run_sees_the_test_period_only_after_the_seal_opens(lab):
    lab.hypothesis()
    open_seal(["H1001"], "abc123", lab.records)

    record = lab.run("H1001", "test")

    assert record["metrics"]["window"]["first"].startswith("2025-01-01")
    assert record["metrics"]["window"]["last"].startswith("2025-03-31")


def test_a_model_runs_only_on_predictors_that_reached_candidate(lab):
    lab.fixed("H1001", p_value=0.40)
    lab.fixed("H1002", p_value=0.01, extra="predictors:\n  - H1001\n")
    lab.run("H1001", "train")

    with pytest.raises(HarnessError, match="has not reached 'candidate'"):
        lab.run("H1002", "train")


# Claim ladder


def hypothesis_stub(id: str, origin: str = "literature", direction: str = "positive", skeptic=None, **dev):
    meta = {
        "id": id, "title": id, "family": "time-series", "origin": origin, "claim": "predictive",
        "prediction": {"direction": direction},
        "decision": {"dev": {"min_ratio": 0.5, "min_size": 0.1} | dev},
        "skeptic": skeptic,
    }
    return registry.Hypothesis(Path(f"{id}-x.md"), meta, "")


def run_stub(hypothesis, segment: str, p_value: float, estimate: float, number: int = 1) -> dict:
    return {
        "hypothesis": hypothesis.id, "segment": segment, "p_value": p_value, "estimate": estimate,
        "spec_hash": hypothesis.spec_hash, "number": number,
    }


def test_false_discovery_control_counts_every_registered_hypothesis():
    tested = hypothesis_stub("H0001")
    few = [tested, hypothesis_stub("H0002"), hypothesis_stub("H0003")]
    many = few + [hypothesis_stub(f"H01{n:02d}") for n in range(10)]
    runs = [run_stub(tested, "train", 0.02, 0.5)]

    # Three hypotheses: q = 0.02 * 3 = 0.06 passes. Thirteen: q = 0.26 does not.
    assert ladder.standings(few, runs)["H0001"].status == ladder.CANDIDATE
    assert ladder.standings(few, runs)["H0001"].q_value == pytest.approx(0.06)
    assert ladder.standings(many, runs)["H0001"].status == ladder.REJECTED
    assert ladder.standings(few, runs)["H0002"].status == ladder.REGISTERED


@pytest.mark.parametrize(
    ("dev_estimate", "status"),
    [(0.30, ladder.SUPPORTED), (0.24, ladder.NOT_REPLICATED), (-0.40, ladder.NOT_REPLICATED)],
)
def test_dev_must_keep_the_sign_and_half_the_train_size(dev_estimate, status):
    hypothesis = hypothesis_stub("H0001")
    runs = [run_stub(hypothesis, "train", 0.001, 0.5), run_stub(hypothesis, "dev", 0.2, dev_estimate, 2)]

    assert ladder.standings([hypothesis], runs)["H0001"].status == status


def test_dev_must_also_reach_the_declared_minimum_size():
    hypothesis = hypothesis_stub("H0001", min_size=0.2)
    runs = [run_stub(hypothesis, "train", 0.001, 0.3), run_stub(hypothesis, "dev", 0.2, 0.18, 2)]

    # Half of the train estimate (0.15) is met, the declared floor (0.2) is not.
    assert ladder.standings([hypothesis], runs)["H0001"].status == ladder.NOT_REPLICATED


def test_a_negative_prediction_is_judged_in_its_own_direction():
    hypothesis = hypothesis_stub("H0001", direction="negative")
    runs = [run_stub(hypothesis, "train", 0.001, -0.5), run_stub(hypothesis, "dev", 0.1, -0.3, 2)]

    assert ladder.standings([hypothesis], runs)["H0001"].status == ladder.SUPPORTED


def test_exploration_hypotheses_are_controlled_on_their_dev_p_values():
    strong, weak, idle = (hypothesis_stub(f"H000{n}", origin="exploration") for n in (1, 2, 3))
    runs = [run_stub(strong, "dev", 0.01, 0.5), run_stub(weak, "dev", 0.08, 0.5)]

    table = ladder.standings([strong, weak, idle], runs)

    # Three exploration hypotheses: 0.01 * 3 = 0.03 passes; 0.08 * 3 / 2 = 0.12 does not.
    assert table["H0001"].status == ladder.SUPPORTED and table["H0001"].q_value == pytest.approx(0.03)
    assert table["H0002"].status == ladder.NOT_REPLICATED
    assert table["H0003"].status == ladder.REGISTERED


def test_the_skeptic_decides_only_what_is_supported():
    confirmed = hypothesis_stub("H0001", skeptic={"verdict": "confirmed"})
    refuted = hypothesis_stub("H0002", skeptic={"verdict": "refuted"})
    rejected = hypothesis_stub("H0003", skeptic={"verdict": "confirmed"})
    runs = [
        run_stub(confirmed, "train", 0.001, 0.5), run_stub(confirmed, "dev", 0.1, 0.4, 2),
        run_stub(refuted, "train", 0.001, 0.5), run_stub(refuted, "dev", 0.1, 0.4, 2),
        run_stub(rejected, "train", 0.6, 0.0),
    ]

    table = ladder.standings([confirmed, refuted, rejected], runs)

    assert [table[name].status for name in ("H0001", "H0002", "H0003")] == [
        ladder.CONFIRMED, ladder.REFUTED, ladder.REJECTED,
    ]


def test_runs_of_an_earlier_specification_do_not_count():
    hypothesis = hypothesis_stub("H0001")
    stale = run_stub(hypothesis, "train", 0.001, 0.5) | {"spec_hash": "something else"}

    assert ladder.standings([hypothesis], [stale])["H0001"].status == ladder.REGISTERED


def test_the_latest_run_of_a_segment_is_the_one_that_counts():
    hypothesis = hypothesis_stub("H0001")
    runs = [run_stub(hypothesis, "train", 0.9, 0.0, 1), run_stub(hypothesis, "train", 0.01, 0.5, 2)]

    assert ladder.standings([hypothesis], runs)["H0001"].status == ladder.CANDIDATE


# Catalogue


def test_catalogue_is_generated_from_the_records_and_updates_each_status(lab):
    lab.fixed("H1001", p_value=0.01)
    lab.fixed("H1002", p_value=0.70)
    lab.hypothesis("H1003")
    lab.run("H1001", "train")
    lab.run("H1002", "train")
    lab.run("H1001", "dev")

    path, table = write_catalogue(lab.records)

    text = path.read_text(encoding="utf-8")
    assert "**3 hypotheses**: 1 supported, 1 registered, 1 rejected." in text
    assert "| [H1001](hypotheses/H1001-momentum.md) | Momentum H1001 | literature | trading | **supported** | 0.5000 | 0.0100 | 0.0300 | 0.5000 | 0.0100 | 0.2500 |" in text
    assert "Test seal: closed" in text and "## Derivatives\n\nNo hypotheses yet." in text
    assert registry.load(lab.records, "H1001").meta["status"] == "supported"
    assert registry.load(lab.records, "H1002").meta["status"] == "rejected"
    assert registry.check_registered(registry.load(lab.records, "H1001"))
    assert write_catalogue(lab.records)[0].read_text(encoding="utf-8") == text


# Command line


def test_research_commands_walk_a_hypothesis_up_the_ladder(lab, capsys):
    lab.fixed("H1001", p_value=0.01)

    assert main(["research", "check", "H1001"]) == 0
    assert main(["research", "run", "H1001", "--segment", "train"]) == 0
    assert "H1001-r01 on train: estimate +0.5000, p = 0.0100" in capsys.readouterr().out
    assert main(["research", "run", "H1001", "--segment", "dev"]) == 0
    assert main(["research", "skeptic", "H1001", "--verdict", "confirmed", "--reason", "survived every attack"]) == 0
    assert main(["research", "catalogue"]) == 0
    assert main(["research", "status"]) == 0
    assert "H1001  confirmed" in capsys.readouterr().out
    assert registry.load(lab.records, "H1001").meta["status"] == "confirmed"


def test_run_command_explains_a_refusal(lab, capsys):
    lab.hypothesis(commit=False)

    assert main(["research", "run", "H1001", "--segment", "train"]) == 1
    assert "Refused: H1001 is not registered" in capsys.readouterr().err


def test_seal_opens_from_the_command_line_only_for_confirmed_finalists(lab, capsys):
    lab.fixed("H1001", p_value=0.01)
    lab.run("H1001", "train")

    assert main(["research", "open-seal", "H1001"]) == 1
    assert "not confirmed: H1001" in capsys.readouterr().err

    lab.run("H1001", "dev")
    main(["research", "skeptic", "H1001", "--verdict", "confirmed", "--reason", "holds"])
    assert main(["research", "open-seal", "H1001"]) == 0
    assert json.loads((lab.records / "SEAL.json").read_text())["finalists"] == ["H1001"]
    assert main(["research", "open-seal", "H1001"]) == 1


def test_mde_command_reports_what_each_segment_can_detect(capsys):
    assert main(["research", "mde", "sharpe-difference", "--correlation", "0.8", "--start", "2019-07-01"]) == 0

    output = capsys.readouterr().out
    assert "train: 3.51 years" in output and "dev: 2.00 years" in output
    assert "minimum detectable effect 1.1112" in output  # dev: (1.645 + 0.842) * sqrt(0.4 / 2.003)
