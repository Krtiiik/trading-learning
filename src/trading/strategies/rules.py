"""Classic rule-based strategies as target weights.

Every function takes an adjusted-close panel and returns target weights indexed by
decision date: row t uses prices up to and including t only. The backtest engine
trades each row on the following day.
"""

import numpy as np
import pandas as pd


def fixed_mix(prices: pd.DataFrame, mix: dict[str, float]) -> pd.DataFrame:
    """Constant weights, from the first date on which every symbol in the mix has a bar."""
    listed = prices[list(mix)].notna().all(axis=1)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    for symbol, weight in mix.items():
        weights[symbol] = weight
    return weights[listed]


def equal_weight(prices: pd.DataFrame) -> pd.DataFrame:
    """1/N across every symbol that has a bar on the decision date."""
    listed = prices.notna()
    counts = listed.sum(axis=1)
    return listed.div(counts.where(counts > 0), axis=0).dropna(how="all")


def time_series_momentum(prices: pd.DataFrame, lookback: int = 252) -> pd.DataFrame:
    """Hold each symbol whose `lookback`-day return is positive, at 1/N of the eligible.

    N counts every symbol with enough history, so symbols in a downtrend leave their
    slice in cash instead of concentrating the rest.
    """
    momentum = prices / prices.shift(lookback) - 1.0
    eligible = momentum.notna()
    counts = eligible.sum(axis=1)
    weights = (momentum > 0).div(counts.where(counts > 0), axis=0)
    return weights.dropna(how="all")


def trend_filter(
    prices: pd.DataFrame, risky: str = "SPY", safe: str | None = "IEF", window: int = 200
) -> pd.DataFrame:
    """All in `risky` while it closes above its `window`-day average, else `safe` (or cash)."""
    average = prices[risky].rolling(window).mean()
    known = average.notna()
    if safe is not None:
        known &= prices[safe].notna()
    above = prices[risky] > average
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights[risky] = above.astype(float)
    if safe is not None:
        weights[safe] = (~above).astype(float)
    return weights[known]


def rsi(prices: pd.Series, window: int) -> pd.Series:
    """Wilder's relative strength index of a price series, 0 to 100."""
    change = prices.diff()
    gain = change.clip(lower=0.0).ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()
    loss = (-change.clip(upper=0.0)).ewm(
        alpha=1.0 / window, adjust=False, min_periods=window
    ).mean()
    return 100.0 - 100.0 / (1.0 + gain / loss)


def rsi_pullback(
    prices: pd.DataFrame,
    symbol: str = "SPY",
    rsi_window: int = 2,
    entry_below: float = 10.0,
    trend_window: int = 200,
    exit_window: int = 5,
) -> pd.DataFrame:
    """Connors-style mean reversion: buy an oversold dip in an uptrend, sell the bounce.

    Enter when RSI(`rsi_window`) is below `entry_below` while the close is above its
    `trend_window`-day average; exit when the close is above its `exit_window`-day average.
    """
    close = prices[symbol]
    enter = (rsi(close, rsi_window) < entry_below) & (close > close.rolling(trend_window).mean())
    leave = close > close.rolling(exit_window).mean()
    state = pd.Series(np.nan, index=close.index)
    state[leave] = 0.0
    state[enter] = 1.0
    state = state.ffill().fillna(0.0)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights[symbol] = state
    return weights[close.rolling(trend_window).mean().notna()]


def cross_sectional_reversal(
    prices: pd.DataFrame, lookback: int = 5, holdings: int = 5
) -> pd.DataFrame:
    """Hold, equally weighted, the `holdings` symbols with the lowest `lookback`-day return."""
    past = prices / prices.shift(lookback) - 1.0
    enough = past.notna().sum(axis=1) >= 2 * holdings
    rank = past.rank(axis=1, method="first")
    weights = (rank <= holdings).astype(float) / holdings
    return weights[enough]
