"""Research's only door to market data: panels cut off at a given day, behind the test seal.

Experiments never read the Store themselves. They receive a `ResearchData` that ends where
their segment ends, so later data is simply not there, and that remembers which datasets were
touched so the run record can name them.
"""

import json
from dataclasses import dataclass, field, replace
from functools import cached_property
from pathlib import Path

import numpy as np
import pandas as pd

from trading.backtest.costs import cost_per_side
from trading.data.bars import Granularity, bar_length, check_granularity
from trading.data.manifest import dataset_id
from trading.data.pit_universe import UNIVERSE_DATASET, membership_panel
from trading.data.rebuild import FUNDING, OPEN_INTEREST, PREMIUM, SPOT, read_universe
from trading.data.storage import BarStore, SeriesStore, default_data_dir
from trading.research.split import check_end

FIELDS = ("open", "high", "low", "close", "volume", "quote_volume")
PANELS = ("member", "tier", "member_next")
SERIES = {"funding": FUNDING, "premium": PREMIUM, "open_interest": OPEN_INTEREST}


@dataclass(frozen=True)
class Market:
    """Spot bars of every coin that has been a universe member so far, as bars x coins arrays.

    NaN where a coin has no bar. `member` is the point-in-time universe and `tier` the
    liquidity tier in force at each bar label; both were decided before that bar opened.
    `member_next` is the membership in force when the bar closes, which is what a decision
    taken at that close should use (it differs from `member` on the last bar of a month).
    """

    granularity: Granularity
    index: pd.DatetimeIndex
    symbols: tuple[str, ...]
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray
    quote_volume: np.ndarray
    member: np.ndarray
    tier: np.ndarray
    member_next: np.ndarray

    @cached_property
    def cost(self) -> np.ndarray:
        """Per-side trading cost (fee plus slippage for the coin's tier) at each bar."""
        return cost_per_side(self.tier)

    def frame(self, values: np.ndarray | str) -> pd.DataFrame:
        """A panel as a DataFrame: pass a field name or any bars x coins array."""
        array = getattr(self, values) if isinstance(values, str) else values
        return pd.DataFrame(array, index=self.index, columns=list(self.symbols))

    def column(self, symbol: str) -> int:
        return self.symbols.index(symbol.upper())

    def truncate(self, last: pd.Timestamp) -> "Market":
        """The same market with every bar labelled after `last` removed."""
        rows = int(self.index.searchsorted(_like(last, self.index), side="right"))
        arrays = {name: getattr(self, name)[:rows] for name in (*FIELDS, *PANELS)}
        return replace(self, index=self.index[:rows], **arrays)


@dataclass
class ResearchData:
    """Market data up to the end of day `end` (UTC), and a note of every dataset touched."""

    end: pd.Timestamp
    root: Path = field(default_factory=default_data_dir)
    records: Path | None = None
    last_label: pd.Timestamp | None = None
    """When set, bars labelled after this instant are also removed (the look-ahead check)."""
    used: dict[str, str] = field(default_factory=dict)
    """Dataset name -> manifest id, for everything loaded through this object."""

    def __post_init__(self) -> None:
        check_end(self.end, self.records)
        self._markets: dict[str, Market] = {}

    def market(self, granularity: Granularity) -> Market:
        if granularity not in self._markets:
            market = load_market(granularity, self.end, self.root, self.records, self.used)
            if self.last_label is not None:
                market = market.truncate(self.last_label)
            self._markets[granularity] = market
        return self._markets[granularity]

    def series(self, name: str, granularity: Granularity, column: str | None = None) -> np.ndarray:
        """A perpetual-futures series aligned to `market(granularity)`: bars x coins.

        `funding`: the funding rates paid during each bar, summed. `premium` (the basis) and
        `open_interest`: the last hourly value inside each bar. Every value is knowable at the
        close of its bar. NaN where the coin has no contract or no data.
        """
        market = self.market(granularity)
        dataset = SERIES[name]
        self.used[dataset] = dataset_id(self.root, dataset)
        store = SeriesStore(dataset, self.root)
        stored = set(store.symbols())
        column = column or {"funding": "rate", "premium": "close", "open_interest": "open_interest"}[name]
        panel = np.full((len(market.index), len(market.symbols)), np.nan)
        for number, symbol in enumerate(market.symbols):
            if symbol in stored:
                values = store.read(symbol)[column]
                panel[:, number] = _align(values, market, how="sum" if name == "funding" else "last")
        return panel

    def truncated(self, last_label: pd.Timestamp) -> "ResearchData":
        """A copy that additionally ends at the bar labelled `last_label`."""
        return ResearchData(self.end, self.root, self.records, last_label, self.used)


def load_market(
    granularity: Granularity,
    end: pd.Timestamp,
    root: Path | None = None,
    records: Path | None = None,
    used: dict[str, str] | None = None,
) -> Market:
    """Spot panels up to the end of day `end`. Raises `SealedError` for a sealed `end`.

    Only coins that were universe members at some reconstitution on or before `end` appear:
    a column for a coin that only becomes a member later would itself leak the future.
    """
    check_end(end, records)
    root = Path(root) if root is not None else default_data_dir()
    granularity = check_granularity(granularity)
    spot = f"{SPOT}/{granularity}"
    ids = {spot: dataset_id(root, spot), UNIVERSE_DATASET: dataset_id(root, UNIVERSE_DATASET)}
    if used is not None:
        used.update(ids)
    cache = _cache(root, granularity, ids[spot], ids[UNIVERSE_DATASET])
    meta = json.loads((cache / "meta.json").read_text(encoding="utf-8"))
    labels = pd.DatetimeIndex(np.load(cache / "index.npy"), name="date")
    index = labels.tz_localize("UTC") if granularity != "1d" else labels
    rows = int(labels.searchsorted(end + pd.Timedelta(days=1), side="left"))

    universe = read_universe(root)
    universe = universe[universe["date"] <= end]
    seen = set(universe["symbol"])
    columns = [number for number, symbol in enumerate(meta["symbols"]) if symbol in seen]
    symbols = [meta["symbols"][number] for number in columns]
    arrays = {
        name: np.load(cache / f"{name}.npy", mmap_mode="r")[:rows][:, columns] for name in FIELDS
    }
    member, tier = membership_panel(universe, index[:rows], symbols)
    closes = index[:rows] + bar_length(granularity)
    member_next, _ = membership_panel(universe, closes, symbols)
    return Market(
        granularity,
        index[:rows],
        tuple(symbols),
        member=member,
        tier=tier,
        member_next=member_next,
        **arrays,
    )


def _cache(root: Path, granularity: Granularity, spot_id: str, universe_id: str) -> Path:
    """Directory of whole-history panels for these dataset versions, built on first use."""
    base = root / "cache" / "market"
    cache = base / f"{granularity}-{spot_id[:12]}-{universe_id[:12]}"
    if (cache / "meta.json").is_file():
        return cache
    store = BarStore(root, SPOT)
    symbols = sorted(read_universe(root)["symbol"].unique())
    bars = {symbol: store.read(symbol, granularity) for symbol in symbols}
    index = pd.DatetimeIndex(sorted(set().union(*(frame.index for frame in bars.values()))))
    cache.mkdir(parents=True, exist_ok=True)
    for name in FIELDS:
        panel = np.full((len(index), len(symbols)), np.nan)
        for number, symbol in enumerate(symbols):
            panel[index.get_indexer(bars[symbol].index), number] = bars[symbol][name].to_numpy()
        np.save(cache / f"{name}.npy", panel)
    np.save(cache / "index.npy", index.tz_localize(None).to_numpy("datetime64[ns]"))
    (cache / "meta.json").write_text(json.dumps({"symbols": symbols}), encoding="utf-8")
    for stale in base.glob(f"{granularity}-*"):
        if stale != cache:
            for file in stale.iterdir():
                file.unlink()
            stale.rmdir()
    return cache


def _align(values: pd.Series, market: Market, how: str) -> np.ndarray:
    """Put a UTC-stamped series onto the market's bars: sum or last value inside each bar.

    A value stamped exactly at a bar's close belongs to that bar (it is known at the close).
    """
    opens = market.index if market.index.tz is not None else market.index.tz_localize("UTC")
    length = bar_length(market.granularity)
    stamps = values.index if values.index.tz is not None else values.index.tz_localize("UTC")
    if values.index.name == "date":
        stamps = stamps + pd.Timedelta(hours=1)  # hourly bars: knowable at their own close
    # A stamp s belongs to the bar with open < s <= open + length.
    position = opens.searchsorted(stamps, side="left") - 1
    valid = (position >= 0) & (stamps <= opens[np.maximum(position, 0)] + length)
    grouped = pd.Series(values.to_numpy()[valid]).groupby(position[valid])
    result = grouped.sum(min_count=1) if how == "sum" else grouped.last()
    out = np.full(len(opens), np.nan)
    out[result.index.to_numpy()] = result.to_numpy()
    return out


def _like(stamp: pd.Timestamp, index: pd.DatetimeIndex) -> pd.Timestamp:
    stamp = pd.Timestamp(stamp)
    if index.tz is not None and stamp.tz is None:
        return stamp.tz_localize(index.tz)
    if index.tz is None and stamp.tz is not None:
        return stamp.tz_convert("UTC").tz_localize(None)
    return stamp
