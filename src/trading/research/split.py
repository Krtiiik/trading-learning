"""The chronological split and the seal on its test segment. The boundaries live only here.

Earlier data may serve a later segment as lookback history; nothing may be fitted, tuned or
chosen using a later segment. Research code gets data only up to the end of the segment it is
working on, and nothing from the test segment until the seal has been opened, once, on record.
"""

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import pandas as pd

from trading.data.storage import PROJECT_ROOT

Segment = Literal["train", "dev", "test"]

TRAIN_END = pd.Timestamp("2022-12-31")
DEV_START = pd.Timestamp("2023-01-01")
DEV_END = pd.Timestamp("2024-12-31")
TEST_START = pd.Timestamp("2025-01-01")
"""Train runs up to 2022, dev covers 2023-2024, test is everything from 2025 on (UTC days)."""

UNKNOWN_FROM = pd.Timestamp("2026-07-01")
"""The model doing this research has no background knowledge from here on; reported separately."""

MAX_FINALISTS = 5
SEAL_FILE = "SEAL.json"


class SealedError(Exception):
    """Test-period data was requested while the seal is closed, or the seal was misused."""


@dataclass(frozen=True)
class Window:
    """A segment's days, both inclusive. `start` None means from the first bar; `end` None, to the last."""

    start: pd.Timestamp | None
    end: pd.Timestamp | None

    def mask(self, index: pd.DatetimeIndex) -> pd.Series:
        """Which bar labels fall inside the window (a label belongs to the day it opens on)."""
        days = (index.tz_localize(None) if index.tz is not None else index).normalize()
        inside = pd.Series(True, index=index)
        if self.start is not None:
            inside &= days >= self.start
        if self.end is not None:
            inside &= days <= self.end
        return inside


SEGMENTS: dict[str, Window] = {
    "train": Window(None, TRAIN_END),
    "dev": Window(DEV_START, DEV_END),
    "test": Window(TEST_START, None),
}


def window(segment: Segment) -> Window:
    if segment not in SEGMENTS:
        raise ValueError(f"unknown segment {segment!r}; choose from {', '.join(SEGMENTS)}")
    return SEGMENTS[segment]


def records_dir() -> Path:
    """Where research records live: `TRADING_RESEARCH_DIR` if set, else `research/` in the project."""
    override = os.environ.get("TRADING_RESEARCH_DIR")
    return Path(override) if override else PROJECT_ROOT / "research"


def seal_record(records: Path | None = None) -> dict | None:
    """The record written when the seal was opened, or None while it is closed."""
    path = (records or records_dir()) / SEAL_FILE
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def seal_is_open(records: Path | None = None) -> bool:
    return seal_record(records) is not None


def check_end(end: pd.Timestamp | None, records: Path | None = None) -> None:
    """Raise unless data up to `end` (a UTC day; None means everything) may be loaded."""
    if (end is None or end >= TEST_START) and not seal_is_open(records):
        raise SealedError(
            f"data from {TEST_START:%Y-%m-%d} on is sealed; ask for data ending "
            f"{DEV_END:%Y-%m-%d} or earlier. The seal is opened once, for the final test run, "
            "with `uv run trading research open-seal`."
        )


def open_seal(finalists: list[str], commit: str, records: Path | None = None) -> dict:
    """Open the seal for the given finalists. A one-time act: a second call raises."""
    records = records or records_dir()
    if seal_is_open(records):
        raise SealedError(f"the seal was already opened: see {records / SEAL_FILE}")
    if not 1 <= len(finalists) <= MAX_FINALISTS or len(set(finalists)) != len(finalists):
        raise SealedError(f"the seal opens for 1 to {MAX_FINALISTS} distinct finalists")
    record = {
        "opened_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "finalists": list(finalists),
    }
    records.mkdir(parents=True, exist_ok=True)
    (records / SEAL_FILE).write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record
