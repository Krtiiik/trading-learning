"""Signals shared by the cross-sectional hypotheses H2001 to H2004, on daily bars.

Each function returns a bars x coins frame for every coin of the market, member or not; the
predictive tests keep universe members only. Row t uses bars labelled t or earlier, and a value
is NaN unless the coin has a bar on every day of the lookback: a signal is never carried forward.
"""

import numpy as np
import pandas as pd

from trading.research.market import Market


def past_return(market: Market, days: int) -> pd.DataFrame:
    """The close of bar t over the close `days` bars earlier, minus one."""
    close = market.frame("close")
    return close / close.shift(days) - 1.0


def volatility(market: Market, days: int) -> pd.DataFrame:
    """Standard deviation of the last `days` daily close-to-close returns, bar t's included."""
    return past_return(market, 1).rolling(days, min_periods=days).std()


def log_mean_quote_volume(market: Market, days: int) -> pd.DataFrame:
    """Log of the mean daily quote volume (in USDT) over the last `days` bars, bar t's included."""
    mean = market.frame("quote_volume").rolling(days, min_periods=days).mean()
    return np.log(mean.where(mean > 0))
