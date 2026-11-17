"""Backtesting: simulate daily-rebalanced target weights against stored bars, after costs."""

from trading.backtest.costs import rebalance, trade_cost
from trading.backtest.engine import BacktestResult, run_backtest
from trading.backtest.market import Market
from trading.backtest.metrics import (
    annual_turnover,
    cagr,
    max_drawdown,
    sharpe,
    summarize,
)

__all__ = [
    "BacktestResult",
    "Market",
    "annual_turnover",
    "cagr",
    "max_drawdown",
    "rebalance",
    "run_backtest",
    "sharpe",
    "summarize",
    "trade_cost",
]
