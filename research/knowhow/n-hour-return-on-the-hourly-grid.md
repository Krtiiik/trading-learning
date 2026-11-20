---
title: "Shifting an hourly panel by N rows is not N hours near an outage: compute lookbacks on the full hourly grid"
kind: how-to
area: data
source: "Data steward measurement on 2026-11-19, hourly train market (46,949 bars by 183 coins): binance/spot/1h id a7d21dafe920, binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-19
---

`market("1h").index` has no row for an hour in which the exchange was down (159 hours in 26 runs on train), so `close.shift(N)` reaches further back than N hours on every row within N rows after an outage. Measured on train: the window is longer than N hours on 0.06% of rows for N = 1 (up to 76 hours), 0.22% for N = 4, 1.33% for N = 24 (up to 99 hours; up to 32 from 2019-07), 4.0% for N = 72, 9.0% for N = 168 and 32% for N = 720. For N = 24 that is 40,732 coin-bars whose "24-bar return" is a return over more than a day.

What a Researcher gets at a gap: no row at all when every coin misses the hour; NaN in one coin's column when only that coin does (on train only the halted BCC in November 2018 and 2018-06-26 02:00 to 11:00); a flat zero-volume bar in a few maintenance hours.

To get a return over exactly N hours, put the panel on the full grid, shift there and come back:

```python
close = market.frame("close")
grid = pd.date_range(close.index[0], close.index[-1], freq="1h")
on_grid = close.reindex(grid)                    # an outage becomes rows of NaN
ret = (on_grid / on_grid.shift(n) - 1).reindex(close.index).to_numpy()
```

The result is NaN wherever either end of the window has no bar: 2,542 member coin-bars for N = 24 and 2,860 for N = 168, of about 1.44 million, so nothing is lost by being exact. If the rule should still have a signal there, carry the last close forward a bounded number of hours first (`on_grid.ffill(limit=12)`): that uses only earlier bars. Rolling statistics (a 168-hour volatility) belong on `on_grid` too, with `min_periods` set, so that a window always covers the same span of time. The grid ends at the panel's last label, so the harness's look-ahead check is unaffected. Decide in the hypothesis file whether the lookback is N hours or N bars; for a daily lookback on daily bars the question does not arise (no member misses a daily bar while it trades).

Not established: whether results differ materially between the two definitions; that is for each hypothesis to check.
