---
title: "A backtest of 40 coins of hourly bars over five years takes about 0.15 seconds"
kind: fact
area: engine
source: "Measured 2026-11-18 on the owner's machine with run_backtest, best of 5 runs"
trust: high
date: 2026-11-18
---

| panel | time |
|---|---:|
| 40 coins x 5 years of daily bars | 3 ms |
| 40 coins x 5 years of hourly bars (43,800 bars) | 141 ms |
| 200 coins x 9 years of hourly bars | 1.0 s |
| real train market, daily (1,963 bars x 183 coins) | 25 ms |
| real train market, hourly (46,949 bars x 183 coins) | 0.7 s |

Time grows with bars times columns, and a research market has a column for every coin that has ever been a member, not just the 40 current ones. Loading a market takes 0.2 s (daily) or 0.8 s (hourly) once its panel cache exists; the first hourly load after a rebuild builds the cache and takes about a minute.

So a daily experiment with its three look-ahead recomputations, two cost levels and three reference benchmarks runs in well under a second, and an hourly one in some tens of seconds. There is no speed reason to skip a check.
