"""E05: does blending trend with the capped mix help, and is any of it beyond noise?

Three pre-specified configurations, then a paired block bootstrap of Sharpe differences.

Run: uv run python research/e05_blend_and_significance.py
"""

import pandas as pd

from common import (
    blend,
    evaluate,
    format_table,
    research_market,
    research_prices,
    results_table,
    sharpe_difference_bootstrap,
    sub_periods,
)
from e01_baselines import EDGES
from trading.strategies import rules

market = research_market()
prices = research_prices()

mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
capped = rules.volatility_cap(mix, prices, 0.08, 20)
trend = rules.inverse_vol_trend(prices, 252, 60)

# Trend with idle cash parked in IEF while IEF's own 12-month return is positive.
idle = 1.0 - trend.sum(axis=1)
ief_up = (prices["IEF"] / prices["IEF"].shift(252) - 1.0).reindex(trend.index) > 0
parked = trend.copy()
parked["IEF"] = parked["IEF"] + idle.where(ief_up, 0.0)

results = {
    "SPY buy & hold": evaluate(market, rules.fixed_mix(prices, {"SPY": 1.0})),
    "60/40 SPY/IEF": evaluate(market, mix),
    "InvVol trend + band": evaluate(market, trend, rebalance_band=0.05),
    "Capped 60/40": evaluate(market, capped, rebalance_band=0.05),
    "Blend 50/50 trend + capped": evaluate(
        market, blend([(0.5, trend), (0.5, capped)]), rebalance_band=0.05
    ),
    "Trend, idle cash in IEF": evaluate(market, parked, rebalance_band=0.05),
    "Trend-parked, cap 8%": evaluate(
        market, rules.volatility_cap(parked, prices, 0.08, 20), rebalance_band=0.05
    ),
}
print(format_table(results_table(results)))
print()
for name, result in results.items():
    parts = sub_periods(result, EDGES)
    print(f"{name:<28}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))

returns = pd.DataFrame({name: result.returns for name, result in results.items()})
print("\ncorrelation of daily returns")
print(returns.corr().round(2).to_string())

print("\npaired block bootstrap of Sharpe differences (20-day blocks, 2000 draws)")
pairs = [
    ("Capped 60/40", "60/40 SPY/IEF"),
    ("Capped 60/40", "SPY buy & hold"),
    ("InvVol trend + band", "60/40 SPY/IEF"),
    ("Blend 50/50 trend + capped", "60/40 SPY/IEF"),
    ("Blend 50/50 trend + capped", "Capped 60/40"),
    ("Trend, idle cash in IEF", "60/40 SPY/IEF"),
]
for a, b in pairs:
    stats = sharpe_difference_bootstrap(returns[a], returns[b])
    print(
        f"  {a} - {b}: {stats['difference']:+.2f}  "
        f"90% [{stats['p05']:+.2f}, {stats['p95']:+.2f}]  P(diff<=0)={stats['share_not_better']:.2f}"
    )
