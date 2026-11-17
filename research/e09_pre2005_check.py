"""E09: the capped 60/40 on 1994-2004, a period no experiment here has touched.

IEF only starts in 2002, so the bond leg is VFITX (Vanguard Intermediate-Term Treasury
fund, daily NAV from Yahoo, stored in data/extra). A mutual fund trades at the closing
NAV, so fills are at the next close. Same parameters as E03: 8% cap, 20-day window, 5%
band, 5 bps. Written down before running: the cap should raise Sharpe and cut drawdown.

Run: uv run python research/e09_pre2005_check.py
"""

import pandas as pd

from common import INITIAL_CASH, SEAL_END, format_table, results_table, sharpe_difference_bootstrap
from trading.backtest import Market, run_backtest
from trading.data import BarStore, load_bars, load_panel
from trading.data.storage import PROJECT_ROOT
from trading.strategies import rules

extra = BarStore(PROJECT_ROOT / "data" / "extra")


def panel(field: str) -> pd.DataFrame:
    spy = load_bars("SPY", end=SEAL_END)[field]
    bond = load_bars("VFITX", end=SEAL_END, store=extra)[field]
    return pd.DataFrame({"SPY": spy, "VFITX": bond}).dropna()


prices = panel("adj_close")
market = Market(open=panel("open"), close=panel("close"), dividends=panel("dividends"))
mix = rules.fixed_mix(prices, {"SPY": 0.6, "VFITX": 0.4})
capped = rules.volatility_cap(mix, prices, 0.08, 20)


def run(targets, start, end, band=0.0):
    return run_backtest(market, targets, initial_cash=INITIAL_CASH, cost_bps=5.0, fill="close",
                        rebalance_band=band, start=start, end=end)


for label, start, end in [("1994-2004 (untouched period)", "1994-01-03", "2004-12-31"),
                          ("2005-seal (proxy check against the IEF version)", "2005-01-03", None)]:
    results = {
        "SPY buy & hold": run(rules.fixed_mix(prices, {"SPY": 1.0}), start, end),
        "60/40 SPY/VFITX": run(mix, start, end),
        "Capped 60/40 SPY/VFITX": run(capped, start, end, band=0.05),
    }
    print(f"\n### {label}\n")
    print(format_table(results_table(results)))
    stats = sharpe_difference_bootstrap(
        results["Capped 60/40 SPY/VFITX"].returns, results["60/40 SPY/VFITX"].returns
    )
    print(f"\ncapped - uncapped Sharpe: {stats['difference']:+.2f}  "
          f"90% [{stats['p05']:+.2f}, {stats['p95']:+.2f}]  P(diff<=0)={stats['share_not_better']:.2f}")
    if end:
        yearly = lambda r: ((1 + r).groupby(r.index.year).prod() - 1) * 100
        table = pd.DataFrame({name: yearly(result.returns) for name, result in results.items()})
        print(table.round(1).T.to_string())
