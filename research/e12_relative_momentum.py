"""E12: relative momentum, two textbook configurations, each run once.

- Sector rotation (Faber): the 3 SPDR sectors with the highest 12-month return, a third
  each, a slot only while that sector's own 12-month return is positive, else cash.
- Dual momentum (Antonacci's GEM): SPY or EFA, whichever has the higher 12-month return,
  if that return is positive; otherwise IEF.
Both are checked daily with a 5% no-trade band.

Run: uv run python research/e12_relative_momentum.py
"""

from common import evaluate, format_table, research_market, research_prices, results_table, sub_periods
from e01_baselines import EDGES
from trading.strategies import rules

SECTORS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]

market = research_market()
prices = research_prices()
results = {
    "Sector top-3, 12m": evaluate(
        market, rules.relative_momentum(prices, SECTORS, 252, 3), rebalance_band=0.05
    ),
    "Dual momentum SPY/EFA else IEF": evaluate(
        market, rules.relative_momentum(prices, ["SPY", "EFA"], 252, 1, fallback="IEF"),
        rebalance_band=0.05,
    ),
}
print(format_table(results_table(results)))
print()
for name, result in results.items():
    parts = sub_periods(result, EDGES)
    print(f"{name:<32}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))
