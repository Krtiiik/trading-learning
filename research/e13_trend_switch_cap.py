"""E13: does a trend switch on the stock leg fix the cap's slow-bear weakness?

E09 showed the volatility cap added nothing in 1994-2004, where the bear market was slow.
Trend rules are meant for exactly that. One configuration, written down before running:
hold 60% SPY only while SPY's 12-month return is positive (else that 60% is cash), 40%
bonds always, then the same 8% / 20-day cap and 5% band.

Judged on the walk-forward window first (2005 .. seal, IEF, next-open fill). The
1994-2004 run (VFITX, next-close fill) is reported too, but that period's yearly returns
had already been seen when this idea was formed, so it is not an untouched test of it.

Run: uv run python research/e13_trend_switch_cap.py
"""

import pandas as pd

from common import (
    INITIAL_CASH,
    SEAL_END,
    evaluate,
    format_table,
    research_market,
    research_prices,
    results_table,
    sharpe_difference_bootstrap,
    sub_periods,
)
from e01_baselines import EDGES
from trading.backtest import Market, run_backtest
from trading.data import BarStore, load_bars
from trading.data.storage import PROJECT_ROOT
from trading.strategies import rules


def switched(prices: pd.DataFrame, bond: str) -> pd.DataFrame:
    """60/40 with the SPY leg in cash while SPY's 12-month return is not positive."""
    return rules.trend_switched_mix(prices, "SPY", bond, risky_weight=0.6, lookback=252)


print("### Walk-forward window 2005 .. seal (5 bps, next-open fill)\n")
market = research_market()
prices = research_prices()
mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
trend_mix = switched(prices, "IEF")
window = {
    "60/40 SPY/IEF": evaluate(market, mix),
    "Capped 60/40": evaluate(market, rules.volatility_cap(mix, prices, 0.08, 20), rebalance_band=0.05),
    "Trend-switched 60/40": evaluate(market, trend_mix, rebalance_band=0.05),
    "Trend-switched + capped": evaluate(
        market, rules.volatility_cap(trend_mix, prices, 0.08, 20), rebalance_band=0.05
    ),
}
print(format_table(results_table(window)))
print()
for name, result in window.items():
    parts = sub_periods(result, EDGES)
    print(f"{name:<26}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))
stats = sharpe_difference_bootstrap(
    window["Trend-switched + capped"].returns, window["Capped 60/40"].returns
)
print(f"\nswitched+capped - capped Sharpe: {stats['difference']:+.2f}  "
      f"90% [{stats['p05']:+.2f}, {stats['p95']:+.2f}]  P(diff<=0)={stats['share_not_better']:.2f}")

print("\n### 1994-2004 with VFITX (5 bps, next-close fill)\n")
extra = BarStore(PROJECT_ROOT / "data" / "extra")


def panel(field: str) -> pd.DataFrame:
    return pd.DataFrame({
        "SPY": load_bars("SPY", end=SEAL_END)[field],
        "VFITX": load_bars("VFITX", end=SEAL_END, store=extra)[field],
    }).dropna()


old_prices = panel("adj_close")
old_market = Market(open=panel("open"), close=panel("close"), dividends=panel("dividends"))
old_mix = rules.fixed_mix(old_prices, {"SPY": 0.6, "VFITX": 0.4})
old_trend = switched(old_prices, "VFITX")


def run(targets, band=0.0):
    return run_backtest(old_market, targets, initial_cash=INITIAL_CASH, cost_bps=5.0, fill="close",
                        rebalance_band=band, start="1994-02-01", end="2004-12-31")


old = {
    "60/40 SPY/VFITX": run(old_mix),
    "Capped 60/40": run(rules.volatility_cap(old_mix, old_prices, 0.08, 20), 0.05),
    "Trend-switched 60/40": run(old_trend, 0.05),
    "Trend-switched + capped": run(rules.volatility_cap(old_trend, old_prices, 0.08, 20), 0.05),
}
print(format_table(results_table(old)))
