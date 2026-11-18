"""Performance metrics. Annualisation follows from the granularity and the market's calendar."""

from functools import cache

import numpy as np
import pandas as pd

from trading.data.bars import Granularity, bar_length

ALWAYS_OPEN = "24/7"


@cache
def periods_per_year(granularity: Granularity, calendar: str = ALWAYS_OPEN) -> float:
    """How many bars of this granularity one year holds on the given calendar.

    A market that never closes has 365 days a year. For an exchange calendar the number of
    sessions is counted from the calendar itself (daily bars only).
    """
    if calendar == ALWAYS_OPEN:
        return pd.Timedelta(days=365) / bar_length(granularity)
    if granularity != "1d":
        raise NotImplementedError("intraday annualisation is only defined for the 24/7 calendar")
    import pandas_market_calendars as mcal

    sessions = mcal.get_calendar(calendar).valid_days("2000-01-01", "2019-12-31")
    return len(sessions) / 20


def sharpe_ratio(returns: np.ndarray, periods: float) -> float:
    """Annualised mean over standard deviation of per-bar returns (zero risk-free rate)."""
    returns = np.asarray(returns, dtype="float64")
    deviation = returns.std(ddof=1) if len(returns) > 1 else 0.0
    return float(returns.mean() / deviation * np.sqrt(periods)) if deviation > 0 else 0.0


def max_drawdown(returns: np.ndarray) -> float:
    """The largest peak-to-trough fall of the compounded equity curve, as a negative fraction."""
    equity = np.cumprod(1.0 + np.asarray(returns, dtype="float64"))
    if not len(equity):
        return 0.0
    peak = np.maximum.accumulate(np.maximum(equity, 1.0))
    return float(min((equity / peak - 1.0).min(), 0.0))


def summarize(
    returns: np.ndarray,
    periods: float,
    turnover: np.ndarray | None = None,
    cost: np.ndarray | None = None,
) -> dict[str, float]:
    """Headline numbers for a series of per-bar net returns."""
    returns = np.asarray(returns, dtype="float64")
    years = len(returns) / periods
    growth = float(np.prod(1.0 + returns))
    summary = {
        "bars": float(len(returns)),
        "years": years,
        "total_return": growth - 1.0,
        "cagr": growth ** (1 / years) - 1.0 if years > 0 and growth > 0 else float("nan"),
        "volatility": float(returns.std(ddof=1) * np.sqrt(periods)) if len(returns) > 1 else 0.0,
        "sharpe": sharpe_ratio(returns, periods),
        "max_drawdown": max_drawdown(returns),
    }
    if turnover is not None:
        # Buys plus sells, so half of it is the one-way turnover.
        summary["turnover_per_year"] = float(np.sum(turnover) / 2 / years) if years > 0 else 0.0
    if cost is not None:
        summary["cost_per_year"] = float(np.sum(cost) / years) if years > 0 else 0.0
    return summary
