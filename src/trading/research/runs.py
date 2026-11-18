"""Run records: one JSON file per run, written by the harness and read by everything else."""

import json
import re
from pathlib import Path
from typing import Any

from trading.research.registry import Hypothesis

_RUN_FILE = re.compile(r"^(H\d{4})-r(\d+)\.json$")


def runs_dir(records: Path) -> Path:
    return records / "runs"


def load_runs(records: Path) -> list[dict[str, Any]]:
    """Every run record, oldest first by hypothesis and run number."""
    found = []
    for path in runs_dir(records).glob("*/H*-r*.json"):
        if _RUN_FILE.match(path.name):
            record = json.loads(path.read_text(encoding="utf-8"))
            record["path"] = path
            found.append(record)
    return sorted(found, key=lambda record: (record["hypothesis"], record["number"]))


def next_number(records: Path, hypothesis_id: str) -> int:
    numbers = [
        int(match.group(2))
        for path in runs_dir(records).glob(f"*/{hypothesis_id}-r*.json")
        if (match := _RUN_FILE.match(path.name))
    ]
    return max(numbers, default=0) + 1


def of(runs: list[dict[str, Any]], hypothesis: Hypothesis, segment: str) -> list[dict[str, Any]]:
    """Runs of this hypothesis on a segment that tested its registered specification."""
    return [
        run
        for run in runs
        if run["hypothesis"] == hypothesis.id
        and run["segment"] == segment
        and run["spec_hash"] == hypothesis.spec_hash
    ]


def latest(runs: list[dict[str, Any]], hypothesis: Hypothesis, segment: str) -> dict[str, Any] | None:
    matching = of(runs, hypothesis, segment)
    return matching[-1] if matching else None
