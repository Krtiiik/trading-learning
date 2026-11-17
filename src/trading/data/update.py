"""Bring stored bars up to date from a provider."""

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from trading.data.bars import Granularity
from trading.data.providers.base import Provider, ProviderError
from trading.data.storage import BarStore


@dataclass(frozen=True)
class UpdateResult:
    symbol: str
    mode: Literal["full", "incremental"]
    new_bars: int
    total_bars: int
    reason: str = ""
    """Why a full download happened, when it was not requested."""


def update_symbol(
    provider: Provider,
    store: BarStore,
    symbol: str,
    granularity: Granularity = "1d",
    full: bool = False,
) -> UpdateResult:
    """Fetch new bars for `symbol` and store them.

    Incrementally, this re-fetches from the last stored bar onward, so a bar stored while
    its session was still open gets replaced by its final values. If the provider's
    adjustment factor (adj_close / close) for that overlapping bar has changed, a new
    dividend or split has re-adjusted the whole history, so everything is downloaded again.
    """
    symbol = symbol.upper()
    stored = store.read(symbol, granularity)

    if full or stored.empty:
        reason = "" if full else "nothing stored yet"
        return _full(provider, store, symbol, granularity, len(stored), reason)

    last = stored.index[-1]
    fetched = provider.fetch(symbol, granularity, start=last.date())
    if fetched.empty:
        return UpdateResult(symbol, "incremental", 0, len(stored))
    if last in fetched.index and _factor_changed(stored.loc[last], fetched.loc[last]):
        return _full(provider, store, symbol, granularity, len(stored), "adjustments changed")

    merged = pd.concat([stored.drop(fetched.index, errors="ignore"), fetched]).sort_index()
    store.write(symbol, granularity, merged)
    return UpdateResult(symbol, "incremental", len(merged) - len(stored), len(merged))


def _full(
    provider: Provider,
    store: BarStore,
    symbol: str,
    granularity: Granularity,
    previously_stored: int,
    reason: str,
) -> UpdateResult:
    bars = provider.fetch(symbol, granularity)
    if bars.empty:
        raise ProviderError(f"{provider.name} returned no bars for {symbol}")
    store.write(symbol, granularity, bars)
    return UpdateResult(symbol, "full", len(bars) - previously_stored, len(bars), reason)


def _factor_changed(stored: pd.Series, fetched: pd.Series) -> bool:
    stored_factor = stored["adj_close"] / stored["close"]
    fetched_factor = fetched["adj_close"] / fetched["close"]
    return not np.isclose(stored_factor, fetched_factor, rtol=1e-6)
