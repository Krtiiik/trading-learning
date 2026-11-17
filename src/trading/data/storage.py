"""Local bar storage: one Parquet file per symbol and granularity."""

import os
from collections.abc import Iterable
from datetime import date
from pathlib import Path

import pandas as pd

from trading.data.bars import BAR_COLUMNS, Granularity, check_granularity, empty_bars

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def default_data_dir() -> Path:
    """`TRADING_DATA_DIR` if set, else `data/` in the project root."""
    override = os.environ.get("TRADING_DATA_DIR")
    return Path(override) if override else PROJECT_ROOT / "data"


class BarStore:
    """Bars on disk at `<root>/<granularity>/<SYMBOL>.parquet`."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else default_data_dir()

    def path(self, symbol: str, granularity: Granularity) -> Path:
        return self.root / check_granularity(granularity) / f"{symbol.upper()}.parquet"

    def exists(self, symbol: str, granularity: Granularity) -> bool:
        return self.path(symbol, granularity).is_file()

    def read(self, symbol: str, granularity: Granularity) -> pd.DataFrame:
        """Stored bars, or an empty bars frame when nothing is stored yet."""
        path = self.path(symbol, granularity)
        if not path.is_file():
            return empty_bars()
        return pd.read_parquet(path)

    def write(self, symbol: str, granularity: Granularity, bars: pd.DataFrame) -> None:
        path = self.path(symbol, granularity)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write next to the target and swap, so an interrupted write never leaves a broken file.
        partial = path.with_suffix(".parquet.partial")
        bars[list(BAR_COLUMNS)].to_parquet(partial)
        partial.replace(path)

    def symbols(self, granularity: Granularity) -> list[str]:
        directory = self.root / check_granularity(granularity)
        return sorted(path.stem for path in directory.glob("*.parquet"))


def load_bars(
    symbol: str,
    granularity: Granularity = "1d",
    start: date | str | None = None,
    end: date | str | None = None,
    store: BarStore | None = None,
) -> pd.DataFrame:
    """Stored bars for one symbol between `start` and `end` (inclusive)."""
    store = store or BarStore()
    if not store.exists(symbol, granularity):
        raise FileNotFoundError(
            f"no {granularity} bars stored for {symbol.upper()} in {store.root}; "
            f"run `uv run trading fetch --symbols {symbol.upper()}` first"
        )
    bars = store.read(symbol, granularity)
    return bars.loc[_bound(start) : _bound(end)]


def load_panel(
    symbols: Iterable[str],
    field: str = "adj_close",
    granularity: Granularity = "1d",
    start: date | str | None = None,
    end: date | str | None = None,
    store: BarStore | None = None,
) -> pd.DataFrame:
    """One bar field for several symbols side by side: index `date`, one column per symbol.

    Dates on which a symbol has no bar (e.g. before its inception) are NaN.
    """
    if field not in BAR_COLUMNS:
        raise ValueError(f"unknown field {field!r}; choose from {', '.join(BAR_COLUMNS)}")
    columns = {
        symbol.upper(): load_bars(symbol, granularity, start, end, store)[field]
        for symbol in symbols
    }
    return pd.DataFrame(columns).sort_index()


def _bound(value: date | str | None) -> pd.Timestamp | None:
    return None if value is None else pd.Timestamp(value)
