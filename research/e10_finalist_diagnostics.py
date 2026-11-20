"""E10: what holding the leading candidate would have felt like (no new configurations).

Rolling comparisons of the capped 60/40 against its uncapped base and SPY inside the
walk-forward window: how often it wins, its worst year, and how long it stays under water.

Run: uv run python research/e10_finalist_diagnostics.py
"""

import numpy as np
import pandas as pd

from common import evaluate, research_market, research_prices
from trading.strategies import rules

market = research_market()
prices = research_prices()
mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
results = {
    "SPY": evaluate(market, rules.fixed_mix(prices, {"SPY": 1.0})),
    "60/40": evaluate(market, mix),
    "Capped 60/40": evaluate(market, rules.volatility_cap(mix, prices, 0.08, 20), rebalance_band=0.05),
}
returns = pd.DataFrame({name: result.returns for name, result in results.items()})

window = 3 * 252
rolling_sharpe = returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)
rolling_sharpe = rolling_sharpe.dropna()
print("rolling 3-year Sharpe: share of days the capped mix is ahead")
for other in ("60/40", "SPY"):
    ahead = (rolling_sharpe["Capped 60/40"] > rolling_sharpe[other]).mean()
    print(f"  vs {other}: {ahead:.0%}   median gap {(rolling_sharpe['Capped 60/40'] - rolling_sharpe[other]).median():+.2f}")

year = 252
rolling_year = (1 + returns).rolling(year).apply(np.prod, raw=True) - 1
print("\nrolling 12-month return")
print((rolling_year.describe().loc[["min", "25%", "50%", "75%", "max"]] * 100).round(1).to_string())
print(f"share of 12-month windows that lost money:  "
      + "  ".join(f"{name} {(rolling_year[name].dropna() < 0).mean():.0%}" for name in returns))

print("\nlongest time under water (trading days) and dollars at the worst point of a $10k start")
for name, result in results.items():
    equity = result.equity
    peak = equity.cummax()
    under = (equity < peak).astype(int)
    longest = int(under.groupby((under == 0).cumsum()).sum().max())
    print(f"  {name:<14}{longest:>5} days   lowest equity ${equity.min():,.0f}   "
          f"deepest drawdown ${(equity - peak).min():,.0f}")

print("\ncalendar-year P&L in dollars on the compounding account (5 bps)")
yearly = pd.DataFrame({name: result.equity.groupby(result.equity.index.year).last() for name, result in results.items()})
pnl = yearly.diff()
pnl.iloc[0] = yearly.iloc[0] - 10_000
print(pnl.round(0).astype(int).T.to_string())
print("\ncalendar-year return in percent")
pct = yearly.pct_change()
pct.iloc[0] = yearly.iloc[0] / 10_000 - 1
print((pct * 100).round(1).T.to_string())
print("\nyears with a loss: " + "  ".join(f"{name} {(pct[name] < 0).sum()}/{len(pct)}" for name in pct))
invested = results["Capped 60/40"].weights.sum(axis=1)
print(f"\ncapped mix: average invested {invested.mean():.0%}, fully invested (>99%) on "
      f"{(invested > 0.99).mean():.0%} of days, below 50% on {(invested < 0.5).mean():.0%} of days")
