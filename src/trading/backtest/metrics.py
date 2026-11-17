"""Performance summary of a backtest: dollars, growth, risk and trading activity."""

import numpy as np
import pandas as pd

from trading.backtest.engine import BacktestResult

TRADING_DAYS = 252


def cagr(equity: pd.Series, initial_cash: float) -> float:
    """Compound annual growth rate over the calendar span of `equity`."""
    years = _years(equity.index)
    return float((equity.iloc[-1] / initial_cash) ** (1.0 / years) - 1.0)


def sharpe(returns: pd.Series) -> float:
    """Annualised mean over standard deviation of daily returns, risk-free rate zero."""
    deviation = returns.std(ddof=1)
    if not deviation > 0:
        return float("nan")
    return float(returns.mean() / deviation * np.sqrt(TRADING_DAYS))


def max_drawdown(equity: pd.Series, initial_cash: float | None = None) -> float:
    """Largest peak-to-trough loss as a negative fraction (0 when equity never falls)."""
    curve = equity.to_numpy(dtype=float)
    if initial_cash is not None:
        curve = np.concatenate([[initial_cash], curve])
    peaks = np.maximum.accumulate(curve)
    return float((curve / peaks - 1.0).min())


def annual_turnover(result: BacktestResult) -> float:
    """One-way turnover per year: half of traded dollars over average equity."""
    years = _years(result.equity.index)
    return float(result.traded.sum() / 2.0 / result.equity.mean() / years)


def summarize(result: BacktestResult) -> dict[str, float]:
    """The headline numbers of a backtest."""
    equity = result.equity
    returns = result.returns
    years = _years(equity.index)
    pnl = float(equity.iloc[-1] - result.initial_cash)
    return {
        "years": years,
        "final_equity": float(equity.iloc[-1]),
        "net_pnl": pnl,
        "pnl_per_year": pnl / years,
        "cagr": cagr(equity, result.initial_cash),
        "vol": float(returns.std(ddof=1) * np.sqrt(TRADING_DAYS)),
        "sharpe": sharpe(returns),
        "max_drawdown": max_drawdown(equity, result.initial_cash),
        "turnover": annual_turnover(result),
        "costs": float(result.costs.sum()),
    }


def _years(index: pd.Index) -> float:
    """Length of the period in years, counting each trading day as 1/252 of a year."""
    return len(index) / TRADING_DAYS
