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


def inverse_vol_trend(
    prices: pd.DataFrame, lookback: int = 252, vol_window: int = 60
) -> pd.DataFrame:
    """Time-series momentum with inverse-volatility sizing.

    Each symbol with enough history gets a slice proportional to 1 / its
    `vol_window`-day volatility; the slice is held only while the symbol's
    `lookback`-day return is positive, otherwise it stays in cash.
    """
    volatility = prices.pct_change(fill_method=None).rolling(vol_window).std()
    momentum = prices / prices.shift(lookback) - 1.0
    eligible = momentum.notna() & (volatility > 0)
    inverse = (1.0 / volatility).where(eligible)
    share = inverse.div(inverse.sum(axis=1), axis=0)
    weights = share.where(momentum > 0, 0.0).fillna(0.0)
    return weights[eligible.any(axis=1)]


def volatility_cap(
    weights: pd.DataFrame, prices: pd.DataFrame, target_vol: float = 0.10, window: int = 60
) -> pd.DataFrame:
    """Scale each day's weights down so the portfolio's expected volatility is at most
    `target_vol` a year, using the covariance of the last `window` daily returns.

    Never scales up (no leverage); the freed weight stays in cash.
    """
    returns = prices.pct_change(fill_method=None)
    scaled = weights.copy()
    for date, row in weights.iterrows():
        held = row[row > 0]
        if held.empty:
            continue
        history = returns.loc[:date, held.index].tail(window).dropna()
        if len(history) < window // 2:
            continue
        variance = float(held.to_numpy() @ history.cov().to_numpy() @ held.to_numpy())
        expected = np.sqrt(max(variance, 0.0) * 252)
        if expected > target_vol:
            scaled.loc[date] = row * (target_vol / expected)
    return scaled


def turn_of_month(
    prices: pd.DataFrame,
    sessions: pd.DatetimeIndex,
    symbol: str = "SPY",
    days_before: int = 1,
    days_after: int = 3,
) -> pd.DataFrame:
    """Hold `symbol` over the last `days_before` and first `days_after` sessions of each month.

    `sessions` is the exchange calendar, which must extend past the last price date:
    it is known in advance, so deciding on day t whether day t+1 is in the window is
    not look-ahead. The row for t is the position to hold during t+1.
    """
    month = sessions.to_period("M")
    position = pd.Series(np.arange(len(sessions)), index=sessions)
    from_start = position.groupby(month).rank()
    from_end = position.groupby(month).rank(ascending=False)
    in_window = (from_end <= days_before) | (from_start <= days_after)
    next_in_window = in_window.shift(-1)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights[symbol] = next_in_window.reindex(prices.index).astype(float)
    return weights[prices[symbol].notna() & weights[symbol].notna()]


def relative_momentum(
    prices: pd.DataFrame,
    candidates: list[str],
    lookback: int = 252,
    holdings: int = 1,
    fallback: str | None = None,
) -> pd.DataFrame:
    """Hold the `holdings` candidates with the highest `lookback`-day return, equally.

    A slot is only filled while its candidate's own return is positive (dual momentum);
    otherwise the slot goes to `fallback`, or stays in cash when there is none or the
    fallback has no bar yet.
    """
    momentum = (prices[candidates] / prices[candidates].shift(lookback) - 1.0)
    enough = momentum.notna().sum(axis=1) >= holdings
    rank = momentum.rank(axis=1, ascending=False, method="first")
    chosen = (rank <= holdings) & (momentum > 0)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights[candidates] = chosen.astype(float) / holdings
    if fallback is not None:
        idle = 1.0 - weights.sum(axis=1)
        weights[fallback] = weights[fallback] + idle.where(prices[fallback].notna(), 0.0)
    return weights[enough]


def trend_switched_mix(
    prices: pd.DataFrame,
    risky: str = "SPY",
    safe: str = "IEF",
    risky_weight: float = 0.6,
    lookback: int = 252,
) -> pd.DataFrame:
    """A fixed risky/safe mix whose risky leg sits in cash while its trend is down.

    `risky` gets `risky_weight` only while its `lookback`-day return is positive;
    `safe` always gets the remainder. Rows start once the trend is known.
    """
    past = prices[risky].shift(lookback)
    up = prices[risky] / past - 1.0 > 0
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights[risky] = up.astype(float) * risky_weight
    weights[safe] = 1.0 - risky_weight
    return weights[past.notna() & prices[safe].notna()]
