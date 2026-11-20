"""E04: is the volatility-capped 60/40 result a plateau or one lucky setting?

A deliberately small sensitivity check around the E03 configuration (target 8%, 20-day
window, 5% band), plus the same cap on other passive mixes. Not a search for a better
setting: the E03 configuration stays the candidate whatever this shows.

Run: uv run python research/e04_volcap_sensitivity.py
"""

from common import evaluate, format_table, research_market, research_prices, results_table, sub_periods
from e01_baselines import EDGES
from trading.strategies import rules

market = research_market()
prices = research_prices()
mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})

print("\n### 60/40 with cap: target x window (band 5%, 5 bps)\n")
grid = {}
for target in (0.06, 0.08, 0.10):
    for window in (20, 60):
        capped = rules.volatility_cap(mix, prices, target, window)
        grid[f"60/40 cap {target:.0%} w{window}"] = evaluate(market, capped, rebalance_band=0.05)
print(format_table(results_table(grid)))

print("\n### 60/40 cap 8% w20: band and fill (5 bps)\n")
capped = rules.volatility_cap(mix, prices, 0.08, 20)
variants = {
    "band 0%": evaluate(market, capped),
    "band 2%": evaluate(market, capped, rebalance_band=0.02),
    "band 5%": evaluate(market, capped, rebalance_band=0.05),
    "band 10%": evaluate(market, capped, rebalance_band=0.10),
    "band 5%, close fill": evaluate(market, capped, rebalance_band=0.05, fill="close"),
    "band 5%, 10 bps": evaluate(market, capped, rebalance_band=0.05, cost_bps=10.0),
}
print(format_table(results_table(variants)))

print("\n### Same cap (8%, w20, band 5%) on other passive mixes, with the uncapped mix\n")
mixes = {
    "60/40 SPY/IEF": {"SPY": 0.6, "IEF": 0.4},
    "60/40 SPY/TLT": {"SPY": 0.6, "TLT": 0.4},
    "40/60 SPY/IEF": {"SPY": 0.4, "IEF": 0.6},
    "SPY/IEF/GLD thirds": {"SPY": 1 / 3, "IEF": 1 / 3, "GLD": 1 / 3},
    "SPY/EFA/IEF/LQD/GLD/VNQ": {s: 1 / 6 for s in ("SPY", "EFA", "IEF", "LQD", "GLD", "VNQ")},
}
other = {}
for name, weights in mixes.items():
    base = rules.fixed_mix(prices, weights)
    other[name] = evaluate(market, base)
    other[name + " cap"] = evaluate(market, rules.volatility_cap(base, prices, 0.08, 20), rebalance_band=0.05)
print(format_table(results_table(other)))
print()
for name, result in other.items():
    parts = sub_periods(result, EDGES)
    print(f"{name:<30}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))

print("\n### Yearly returns: 60/40 vs capped 60/40 (5 bps)\n")
plain = evaluate(market, mix).returns
cap = grid["60/40 cap 8% w20"].returns
yearly = lambda r: (1 + r).groupby(r.index.year).prod() - 1
table = yearly(plain).to_frame("60/40").join(yearly(cap).rename("capped"))
print((table * 100).round(1).T.to_string())
