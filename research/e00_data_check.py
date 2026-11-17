"""E00: check the sealed data and the backtester against known quantities.

Run: uv run python research/e00_data_check.py
"""

import pandas as pd

from common import SEAL_END, SYMBOLS, evaluate, research_market, research_prices

market = research_market()
prices = research_prices()

assert market.dates.max() <= pd.Timestamp(SEAL_END)
print(f"dates {market.dates.min().date()} .. {market.dates.max().date()}  ({len(market.dates)} days)")

print("\nfirst bar and interior gaps per symbol")
for symbol in SYMBOLS:
    close = market.close[symbol]
    first = close.first_valid_index()
    listed = close.loc[first:]
    gaps = int(listed.isna().sum())
    open_gaps = int(market.open[symbol].loc[first:].isna().sum())
    bad_open = int(
        ((market.open[symbol] / market.close[symbol].shift(1) - 1).abs() > 0.15).sum()
    )
    print(f"  {symbol:<5} first={first.date()}  gaps={gaps}  open_gaps={open_gaps}  |gap|>15%={bad_open}")

# Buy and hold SPY in the engine (cash dividends, no cost) against adjusted close.
start = "2005-01-03"
targets = pd.DataFrame({"SPY": 1.0}, index=[market.dates[market.dates.searchsorted(start) - 1]])
result = evaluate(market, targets, cost_bps=0.0, fill="close", start=str(targets.index[0].date()))
adj = prices["SPY"].loc[result.equity.index[1] :]
print("\nSPY buy and hold, 2005 to seal")
print(f"  engine total return (dividends kept as cash): {result.equity.iloc[-1] / 10_000 - 1:.3f}")
print(f"  adjusted close total return (reinvested):     {adj.iloc[-1] / adj.iloc[0] - 1:.3f}")
print(f"  price-only return:                            "
      f"{market.close['SPY'].iloc[-1] / market.close['SPY'].loc[adj.index[0]] - 1:.3f}")

# Daily rebalancing to 100% SPY reinvests dividends, so it should match adjusted close.
daily = pd.DataFrame({"SPY": 1.0}, index=market.dates[market.dates >= targets.index[0]])
reinvested = evaluate(market, daily, cost_bps=0.0, fill="close", start=str(targets.index[0].date()))
print(f"  engine, dividends reinvested daily:           {reinvested.equity.iloc[-1] / 10_000 - 1:.3f}")
