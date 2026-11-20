"""Backtesting: a vectorised engine, the cost model, benchmarks and performance metrics."""

from trading.backtest.costs import DOUBLE_COST, FEE, SLIPPAGE, cost_per_side
from trading.backtest.engine import BacktestResult, run_backtest
from trading.backtest.metrics import max_drawdown, periods_per_year, sharpe_ratio, summarize

__all__ = [
    "DOUBLE_COST",
    "FEE",
    "SLIPPAGE",
    "BacktestResult",
    "cost_per_side",
    "max_drawdown",
    "periods_per_year",
    "run_backtest",
    "sharpe_ratio",
    "summarize",
]
