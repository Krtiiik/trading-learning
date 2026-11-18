"""The harness: the only way a hypothesis is tested, and the only writer of run records.

`run` refuses a hypothesis that is not committed or has changed since registration, hands the
experiment data that ends where the segment ends, proves mechanically that the experiment's
panel does not look ahead, and writes the run record itself. Nothing depends on an agent
remembering to log.

An experiment is a module with two functions:

    panel(data, params) -> DataFrame   target weights or a predictor; row t uses bars <= t only
    test(ctx, panel)    -> Result      the single primary test, usually one call to evaluate_*
"""

import ast
import importlib
import json
import math
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pandas as pd

from trading.research import ladder, registry
from trading.research.evaluate import Context, Result
from trading.research.market import ResearchData
from trading.research.registry import Hypothesis, RegistryError
from trading.research.runs import load_runs, next_number, of, runs_dir
from trading.research.split import DEV_END, TRAIN_END, SealedError, Segment, records_dir, seal_record, window

HARNESS_VERSION = 1
EVERYTHING = pd.Timestamp("2200-01-01")
"""The data end for a test run: no limit (allowed only once the seal is open)."""
LOOKAHEAD_CUTS = (0.45, 0.75, 0.97)
"""Where along the panel's rows the look-ahead check cuts the data and recomputes."""

FORBIDDEN_IMPORTS = ("trading.data", "pyarrow")
"""Experiments get data from the harness; reading the Store directly would bypass the seal."""


class HarnessError(Exception):
    """A run was refused: the reason is in the message."""


class LookaheadError(HarnessError):
    """An experiment's panel changed for past bars when later data was removed."""


def run(
    hypothesis_id: str,
    segment: Segment,
    records: Path | None = None,
    data_root: Path | None = None,
    rerun_reason: str | None = None,
) -> dict[str, Any]:
    """Run a hypothesis's primary test on a segment and write the run record. Returns the record."""
    records = records or records_dir()
    started = time.perf_counter()
    hypothesis = registry.load(records, hypothesis_id)
    registered_in = registry.check_registered(hypothesis)
    root = registry.repository_root(hypothesis.path)
    previous = load_runs(records)
    _check_allowed(hypothesis, segment, records, previous, rerun_reason)

    module = _load_experiment(hypothesis)
    _check_committed(root, module)
    end = {"train": TRAIN_END, "dev": DEV_END}.get(segment, EVERYTHING)
    data = ResearchData(end, **({"root": data_root} if data_root else {}), records=records)
    params = hypothesis.params
    seed = int(hypothesis.id[1:])

    panel = module.panel(data, params)
    if not isinstance(panel, pd.DataFrame) or panel.empty:
        raise HarnessError(f"{hypothesis.experiment}.panel must return a non-empty DataFrame")
    cuts = _check_no_lookahead(module, data, params, panel)
    ctx = Context(hypothesis, segment, window(segment), data, params, seed)
    result = module.test(ctx, panel)
    _check_result(hypothesis, result)
    _check_committed(root, module)  # again: modules imported while the experiment ran

    number = next_number(records, hypothesis.id)
    now = datetime.now(UTC)
    record = {
        "run": f"{hypothesis.id}-r{number:02d}",
        "hypothesis": hypothesis.id,
        "number": number,
        "segment": segment,
        "spec_hash": hypothesis.spec_hash,
        "registered_in": registered_in,
        "commit": registry.head_commit(root),
        "experiment": hypothesis.experiment,
        "params": params,
        "seed": seed,
        "direction": hypothesis.direction,
        "claim": hypothesis.claim,
        "estimate": result.estimate,
        "p_value": result.p_value,
        "n": result.n,
        "double_cost": (
            {"estimate": result.double_cost_estimate, "p_value": result.double_cost_p_value}
            if result.double_cost_estimate is not None
            else None
        ),
        "metrics": result.metrics,
        "data": dict(sorted(data.used.items())),
        "lookahead_check": {"passed": True, "cuts": cuts},
        "rerun_reason": rerun_reason,
        "started_at": now.isoformat(timespec="seconds"),
        "duration_seconds": round(time.perf_counter() - started, 3),
        "harness_version": HARNESS_VERSION,
        "python": platform.python_version(),
    }
    path = runs_dir(records) / f"{now:%Y-%m-%d}" / f"{record['run']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_plain(record), indent=1) + "\n", encoding="utf-8", newline="\n")
    return record | {"path": path}


def replay(
    hypothesis_id: str,
    records: Path | None = None,
    data_root: Path | None = None,
    **overrides: Any,
) -> Result:
    """Re-run a hypothesis's experiment on train, optionally with changed parameters.

    For Skeptic reviews and debugging: nothing is recorded and the result is not evidence.
    Train only, on purpose; the dev result of a hypothesis exists once, in its run record.
    """
    records = records or records_dir()
    hypothesis = registry.load(records, hypothesis_id)
    module = _load_experiment(hypothesis)
    data = ResearchData(TRAIN_END, **({"root": data_root} if data_root else {}), records=records)
    params = hypothesis.params | overrides
    ctx = Context(hypothesis, "train", window("train"), data, params, int(hypothesis.id[1:]))
    return module.test(ctx, module.panel(data, params))


def _check_allowed(
    hypothesis: Hypothesis,
    segment: Segment,
    records: Path,
    previous: list[dict[str, Any]],
    rerun_reason: str | None,
) -> None:
    """The ladder's rules about which segment a hypothesis may be run on, and how often."""
    table = ladder.standings(registry.load_all(records), previous)
    for predictor in hypothesis.predictors:
        if predictor not in table or table[predictor].status not in ladder.AT_LEAST_CANDIDATE:
            raise HarnessError(
                f"{hypothesis.id} is a model on {predictor}, which has not reached 'candidate'; "
                "models are allowed only on predictors that have"
            )
    earlier = of(previous, hypothesis, segment)
    if segment == "train":
        if hypothesis.origin == "exploration":
            raise HarnessError(
                f"{hypothesis.id} came from exploring train data and cannot be tested on it; "
                "its evidence is the dev run"
            )
    elif segment == "dev":
        status = table[hypothesis.id].status
        if hypothesis.origin == "literature" and status not in ladder.AT_LEAST_CANDIDATE:
            raise HarnessError(
                f"{hypothesis.id} is '{status}', not a candidate: dev is for replicating "
                "hypotheses that passed false-discovery control on train"
            )
    else:
        seal = seal_record(records)
        if seal is None:
            raise SealedError("the test segment is sealed; see `trading research open-seal`")
        if hypothesis.id not in seal["finalists"]:
            raise SealedError(f"{hypothesis.id} is not one of the finalists the seal was opened for")
        if earlier:
            raise SealedError(f"{hypothesis.id} already had its one test run ({earlier[-1]['run']})")
    if earlier and segment == "dev" and not rerun_reason:
        raise HarnessError(
            f"{hypothesis.id} already ran on dev ({earlier[-1]['run']}); dev is evaluated once per "
            "registered specification. If that run was invalid (a bug, wrong data), run again "
            "with --rerun-reason saying why; the reason is recorded."
        )


def _load_experiment(hypothesis: Hypothesis) -> ModuleType:
    try:
        module = importlib.import_module(hypothesis.experiment)
    except ImportError as error:
        raise HarnessError(f"cannot import experiment {hypothesis.experiment}: {error}") from error
    for name in ("panel", "test"):
        if not callable(getattr(module, name, None)):
            raise HarnessError(f"{hypothesis.experiment} must define {name}()")
    source = Path(module.__file__ or "").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        imported: list[str] = []
        if isinstance(node, ast.Import):
            imported = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported = [node.module, *(f"{node.module}.{alias.name}" for alias in node.names)]
        for name in imported:
            if any(name == bad or name.startswith(bad + ".") for bad in FORBIDDEN_IMPORTS):
                raise HarnessError(
                    f"{hypothesis.experiment} imports {name}: experiments take data from the "
                    "harness (the `data` argument), never from the Store"
                )
    return module


def _check_committed(root: Path, experiment: ModuleType) -> None:
    """Every project module the run uses must be committed, so the record's commit reproduces it."""
    loaded = [
        Path(module.__file__)
        for module in list(sys.modules.values())
        if getattr(module, "__file__", None)
        and Path(module.__file__).suffix == ".py"
        and Path(module.__file__).resolve().is_relative_to(root.resolve())
    ]
    dirty = registry.uncommitted(root, [*loaded, Path(experiment.__file__ or "")])
    if dirty:
        raise HarnessError(
            "uncommitted code would make this run unreproducible; commit first: " + ", ".join(dirty)
        )


def _check_no_lookahead(
    module: ModuleType, data: ResearchData, params: dict[str, Any], panel: pd.DataFrame
) -> list[str]:
    """Recompute the panel with later bars removed: rows up to the cut must not change."""
    cuts = []
    for share in LOOKAHEAD_CUTS:
        cut = panel.index[min(int(len(panel) * share), len(panel) - 1)]
        again = module.panel(data.truncated(cut), params)
        expected = panel.loc[:cut]
        again = again.loc[:cut]
        same = (
            expected.index.equals(again.index)
            and set(expected.columns) == set(again.columns)
            and np.allclose(
                expected.to_numpy("float64"),
                again[expected.columns].to_numpy("float64"),
                rtol=1e-9,
                atol=1e-12,
                equal_nan=True,
            )
        )
        if not same:
            raise LookaheadError(
                f"{module.__name__}.panel looks ahead: with bars after {cut} removed, its rows "
                f"up to {cut} change. Nothing was recorded."
            )
        cuts.append(str(cut))
    return cuts


def _check_result(hypothesis: Hypothesis, result: Any) -> None:
    if not isinstance(result, Result):
        raise HarnessError(f"{hypothesis.experiment}.test must return a Result")
    if not math.isfinite(result.estimate) or not 0.0 <= result.p_value <= 1.0:
        raise HarnessError(f"{hypothesis.id}: the test returned no usable estimate and p-value")
    if hypothesis.claim == "trading" and result.double_cost_estimate is None:
        raise HarnessError(f"{hypothesis.id} is a trading claim: the test must report double cost")


def _plain(value: Any) -> Any:
    """Make a record JSON-serialisable: numpy numbers and non-finite floats included."""
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, pd.Timestamp | Path):
        return str(value)
    return value
