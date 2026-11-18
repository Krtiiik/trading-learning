"""Rebuild the crypto part of the Store from nothing, one dataset after another.

Order matters: daily bars for every USDT pair come first, because the point-in-time universe
is ranked from them; hourly bars and the perpetual-futures series are then fetched only for
pairs that were ever universe members. Every dataset ends with a manifest.
"""

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from trading.data.manifest import Manifest, build_manifest
from trading.data.pit_universe import (
    QUOTE,
    UNIVERSE_DATASET,
    UNIVERSE_FILE,
    UniverseRules,
    build_universe,
)
from trading.data.providers.base import ProviderError
from trading.data.providers.binance import (
    ArchiveFile,
    BinanceArchive,
    perp_symbol_for,
    spot_symbols,
)
from trading.data.storage import BarStore, SeriesStore, default_data_dir

SPOT = "binance/spot"
FUNDING = "binance/funding"
PREMIUM = "binance/premium/1h"
OPEN_INTEREST = "binance/open_interest/1h"

STEPS = ("spot-1d", "universe", "spot-1h", "funding", "premium", "open-interest")
DEFAULT_STEPS = STEPS[:5]
"""Open interest is left out by default: it is roughly 1,500 small files per coin."""

Sources = dict[str, list[tuple[str, str]]]


def rebuild(
    root: Path | None = None,
    provider: BinanceArchive | None = None,
    steps: Iterable[str] = DEFAULT_STEPS,
    rules: UniverseRules = UniverseRules(),
    log: Callable[[str], None] = print,
    workers: int = 6,
) -> dict[str, Manifest]:
    """Run the given rebuild steps in their fixed order; returns the manifests written."""
    root = Path(root) if root is not None else default_data_dir()
    provider = provider or BinanceArchive(raw_dir=root / "raw" / "binance")
    steps = [step for step in STEPS if step in set(steps)]
    manifests: dict[str, Manifest] = {}

    def finish(dataset: str, sources: Sources | None = None) -> None:
        if sources is not None:
            # A rebuild leaves nothing behind from an earlier one.
            for stale in (root / dataset).glob("*.parquet"):
                if stale.name not in sources:
                    stale.unlink()
        manifests[dataset] = build_manifest(root, dataset, provider.name, sources)
        log(f"{dataset}: {len(manifests[dataset].files)} files, id {manifests[dataset].short_id}")

    if "spot-1d" in steps:
        symbols = spot_symbols(provider.list_symbols("spot", "klines"), QUOTE)
        log(f"spot 1d: fetching {len(symbols)} {QUOTE} pairs")
        finish(f"{SPOT}/1d", _fetch_bars(provider, root, symbols, "1d", workers, log))

    if "universe" in steps:
        universe = write_universe(root, rules)
        dates = universe["date"]
        log(
            f"universe: {dates.nunique()} reconstitutions {dates.min():%Y-%m} to "
            f"{dates.max():%Y-%m}, {universe['symbol'].nunique()} pairs were ever members"
        )
        finish(UNIVERSE_DATASET)

    members = _members(root) if set(steps) & {"spot-1h", "funding", "premium", "open-interest"} else []

    if "spot-1h" in steps:
        log(f"spot 1h: fetching {len(members)} pairs that were ever universe members")
        finish(f"{SPOT}/1h", _fetch_bars(provider, root, members, "1h", workers, log))

    perps: dict[str, str] = {}
    if set(steps) & {"funding", "premium", "open-interest"}:
        available = provider.perp_symbols()
        perps = {s: p for s in members if (p := perp_symbol_for(s, available)) is not None}
        log(f"perpetuals: {len(perps)} of {len(members)} members have a contract")

    series_steps = (
        ("funding", FUNDING, provider.fetch_funding),
        ("premium", PREMIUM, provider.fetch_premium),
        ("open-interest", OPEN_INTEREST, provider.fetch_open_interest),
    )
    for step, dataset, fetch in series_steps:
        if step in steps:
            log(f"{step}: fetching {len(perps)} series")
            finish(dataset, _fetch_series(SeriesStore(dataset, root), perps, fetch, workers, log))
    return manifests


def write_universe(root: Path, rules: UniverseRules = UniverseRules()) -> pd.DataFrame:
    """Rank the stored daily bars into the point-in-time universe and store the table."""
    store = BarStore(root, SPOT)
    bars = {symbol: store.read(symbol, "1d") for symbol in store.symbols("1d")}
    quote_volume = pd.DataFrame({symbol: frame["quote_volume"] for symbol, frame in bars.items()})
    close = pd.DataFrame({symbol: frame["close"] for symbol, frame in bars.items()})
    universe = build_universe(quote_volume, close, rules)
    path = root / UNIVERSE_DATASET / UNIVERSE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    universe.to_parquet(path)
    return universe


def read_universe(root: Path | None = None) -> pd.DataFrame:
    root = Path(root) if root is not None else default_data_dir()
    path = root / UNIVERSE_DATASET / UNIVERSE_FILE
    if not path.is_file():
        raise FileNotFoundError(f"no point-in-time universe in {path.parent}; run `uv run trading rebuild`")
    return pd.read_parquet(path)


def _members(root: Path) -> list[str]:
    return sorted(read_universe(root)["symbol"].unique())


def _checksums(files: list[ArchiveFile]) -> list[tuple[str, str]]:
    return [(file.key, file.etag) for file in files]


def _fetch_bars(
    provider: BinanceArchive,
    root: Path,
    symbols: list[str],
    granularity: str,
    workers: int,
    log: Callable[[str], None],
) -> Sources:
    store = BarStore(root, SPOT)

    def one(symbol: str) -> tuple[str, list[ArchiveFile]] | None:
        try:
            bars, files = provider.fetch_with_sources(symbol, granularity)  # type: ignore[arg-type]
        except ProviderError as error:
            log(f"  {symbol}: FAILED {error}")
            return None
        if bars.empty:
            return None
        store.write(symbol, granularity, bars)  # type: ignore[arg-type]
        return f"{symbol}.parquet", files

    return _run(one, symbols, workers)


def _fetch_series(
    store: SeriesStore,
    perps: dict[str, str],
    fetch: Callable[[str], tuple[pd.DataFrame, list[ArchiveFile]]],
    workers: int,
    log: Callable[[str], None],
) -> Sources:
    def one(symbol: str) -> tuple[str, list[ArchiveFile]] | None:
        try:
            series, files = fetch(perps[symbol])
        except ProviderError as error:
            log(f"  {symbol}: FAILED {error}")
            return None
        if series.empty:
            return None
        # Stored under the spot symbol: research joins these series to spot bars.
        store.write(symbol, series)
        return f"{symbol}.parquet", files

    return _run(one, sorted(perps), workers)


def _run(
    one: Callable[[str], tuple[str, list[ArchiveFile]] | None], symbols: list[str], workers: int
) -> Sources:
    with ThreadPoolExecutor(workers) as pool:
        done = [result for result in pool.map(one, symbols) if result is not None]
    return {name: _checksums(files) for name, files in done}
