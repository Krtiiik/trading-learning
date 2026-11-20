"""Signals shared by the time-series hypotheses H1002 to H1005.

Calendar dummies, a bar's own return in units of the coin's recent volatility, and the
volatility scale of the equal-weight universe. Row t of everything here uses bars labelled t or
earlier only.
"""

from collections.abc import Iterable

import numpy as np
import pandas as pd

from trading.research.market import Market


def calendar_dummy(
    market: Market, hours: Iterable[int] | None = None, weekdays: Iterable[int] | None = None
) -> pd.DataFrame:
    """1.0 for every coin on bars whose label falls on the given UTC hours and weekdays, else 0.0.

    A bar label is the bar's open. Weekdays count from Monday = 0. A condition left out is
    not applied.
    """
    on = np.ones(len(market.index), dtype=bool)
    if hours is not None:
        on &= np.isin(market.index.hour, list(hours))
    if weekdays is not None:
        on &= np.isin(market.index.dayofweek, list(weekdays))
    return market.frame(np.repeat(on[:, None].astype("float64"), len(market.symbols), axis=1))


def bar_return_zscore(market: Market, window: int, min_periods: int) -> pd.DataFrame:
    """Each bar's open-to-close return over the deviation of the coin's `window` bars before it.

    The deviation is taken on the full grid of bar labels, so the window always spans the same
    stretch of time and an exchange outage shortens it instead of reaching further back. The
    bar's own return is not part of its deviation. NaN without `min_periods` earlier returns.
    """
    change = market.frame(market.close / market.open - 1.0)
    step = "1h" if market.granularity == "1h" else "1D"
    on_grid = change.reindex(pd.date_range(market.index[0], market.index[-1], freq=step))
    deviation = on_grid.rolling(window, min_periods=min_periods).std().shift(1)
    return (on_grid / deviation.where(deviation > 0)).reindex(market.index)


def universe_return(market: Market) -> pd.Series:
    """The members' average close-to-close return at each bar; NaN while there is no member."""
    change = np.full(market.close.shape, np.nan)
    change[1:] = market.close[1:] / market.close[:-1] - 1.0
    change = np.where(market.member, change, np.nan)
    count = np.isfinite(change).sum(axis=1)
    mean = np.where(count > 0, np.nansum(change, axis=1) / np.maximum(count, 1), np.nan)
    return pd.Series(mean, index=market.index)


def volatility_scale(returns: pd.Series, short: int, long: int) -> pd.Series:
    """Exposure between 0 and 1: the usual volatility over the recent one, never above 1.

    Both are standard deviations of `returns` over trailing windows that end at the row itself.
    While either window is not full the exposure is 1: without a measurement nothing is scaled.
    """
    recent = returns.rolling(short, min_periods=short).std()
    usual = returns.rolling(long, min_periods=long).std()
    return (usual / recent).clip(upper=1.0).fillna(1.0)
