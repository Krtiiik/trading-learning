"""Local storage: one Parquet file per symbol, grouped into datasets."""

import os
from collections.abc import Iterable
from datetime import date
from pathlib import Path

import pandas as pd

from trading.data.bars import (
    BAR_COLUMNS,
    EXTRA_COLUMNS,
    Granularity,
    bar_columns,
    check_granularity,
    empty_bars,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def default_data_dir() -> Path:
    """`TRADING_DATA_DIR` if set, else `data/` in the project root."""
    override = os.environ.get("TRADING_DATA_DIR")
    return Path(override) if override else PROJECT_ROOT / "data"


class BarStore:
    """Bars on disk at `<root>[/<dataset>]/<granularity>/<SYMBOL>.parquet`.

    Without a `dataset` this is the original layout that holds the Yahoo ETF bars.
    """

    def __init__(self, root: Path | None = None, dataset: str | None = None) -> None:
        self.root = Path(root) if root is not None else default_data_dir()
        self.dataset = dataset

    def directory(self, granularity: Granularity) -> Path:
        base = self.root / self.dataset if self.dataset else self.root
        return base / check_granularity(granularity)

    def path(self, symbol: str, granularity: Granularity) -> Path:
        return self.directory(granularity) / f"{symbol.upper()}.parquet"

    def exists(self, symbol: str, granularity: Granularity) -> bool:
        return self.path(symbol, granularity).is_file()

    def read(self, symbol: str, granularity: Granularity) -> pd.DataFrame:
        """Stored bars, or an empty bars frame when nothing is stored yet."""
        path = self.path(symbol, granularity)
        if not path.is_file():
            return empty_bars()
        return pd.read_parquet(path)

    def write(self, symbol: str, granularity: Granularity, bars: pd.DataFrame) -> None:
        _write(self.path(symbol, granularity), bars[bar_columns(bars)])

    def symbols(self, granularity: Granularity) -> list[str]:
        return sorted(path.stem for path in self.directory(granularity).glob("*.parquet"))


class SeriesStore:
    """Per-symbol series that are not bars (funding rate, basis, open interest).

    Files live at `<root>/<dataset>/<SYMBOL>.parquet`, each indexed by tz-aware UTC time.
    """

    def __init__(self, dataset: str, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else default_data_dir()
        self.dataset = dataset

    @property
    def directory(self) -> Path:
        return self.root / self.dataset

    def path(self, symbol: str) -> Path:
        return self.directory / f"{symbol.upper()}.parquet"

    def exists(self, symbol: str) -> bool:
        return self.path(symbol).is_file()

    def read(self, symbol: str) -> pd.DataFrame:
        path = self.path(symbol)
        if not path.is_file():
            raise FileNotFoundError(f"no {self.dataset} series stored for {symbol.upper()}")
        return pd.read_parquet(path)

    def write(self, symbol: str, series: pd.DataFrame) -> None:
        _write(self.path(symbol), series)

    def symbols(self) -> list[str]:
        return sorted(path.stem for path in self.directory.glob("*.parquet"))


def _write(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write next to the target and swap, so an interrupted write never leaves a broken file.
    partial = path.with_suffix(".parquet.partial")
    frame.to_parquet(partial)
    partial.replace(path)


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
    return bars.loc[_bound(start, bars.index) : _bound(end, bars.index, closing=True)]


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
    if field not in BAR_COLUMNS and field not in EXTRA_COLUMNS:
        choices = ", ".join((*BAR_COLUMNS, *EXTRA_COLUMNS))
        raise ValueError(f"unknown field {field!r}; choose from {choices}")
    columns = {
        symbol.upper(): load_bars(symbol, granularity, start, end, store)[field]
        for symbol in symbols
    }
    return pd.DataFrame(columns).sort_index()


def _bound(
    value: date | str | None, index: pd.DatetimeIndex, closing: bool = False
) -> pd.Timestamp | None:
    if value is None:
        return None
    bound = pd.Timestamp(value)
    if index.tz is not None and bound.tz is None:
        bound = bound.tz_localize(index.tz)
        if closing and bound == bound.normalize():
            # An end given as a day includes that whole day of intraday bars.
            bound += pd.Timedelta(days=1) - pd.Timedelta(1, "ns")
    return bound
