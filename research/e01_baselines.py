"""E01: baselines on the pre-holdout window, parameters fixed from the literature.

Run: uv run python research/e01_baselines.py
"""

from common import (
    EVAL_START,
    evaluate,
    format_table,
    research_market,
    research_prices,
    results_table,
    sub_periods,
)
from trading.strategies import rules

market = research_market()
prices = research_prices()

BASELINES = {
    "SPY buy & hold": rules.fixed_mix(prices, {"SPY": 1.0}),
    "Equal weight (1/N)": rules.equal_weight(prices),
    "60/40 SPY/IEF": rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4}),
    "TSMOM 12m, 1/N": rules.time_series_momentum(prices, lookback=252),
    "SPY>SMA200 else IEF": rules.trend_filter(prices, "SPY", "IEF", 200),
    "SPY>SMA200 else cash": rules.trend_filter(prices, "SPY", None, 200),
    "RSI2 pullback SPY": rules.rsi_pullback(prices, "SPY"),
    "XS 5d reversal, 5 worst": rules.cross_sectional_reversal(prices, 5, 5),
}

EDGES = [EVAL_START, "2010-01-01", "2015-01-01", "2020-01-01", "2024-11-16"]

if __name__ == "__main__":
    for cost in (5.0, 2.0, 0.0):
        results = {name: evaluate(market, targets, cost_bps=cost) for name, targets in BASELINES.items()}
        print(f"\n### {EVAL_START} .. seal, fill at next open, {cost:g} bps per side\n")
        print(format_table(results_table(results)))

    results = {name: evaluate(market, targets) for name, targets in BASELINES.items()}
    print("\n### Sharpe by sub-period (5 bps)\n")
    for name, result in results.items():
        parts = sub_periods(result, EDGES)
        print(f"{name:<26}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))

    close_fill = {name: evaluate(market, targets, fill="close") for name, targets in BASELINES.items()}
    print("\n### Fill at next close instead of next open (5 bps)\n")
    print(format_table(results_table(close_fill)))
