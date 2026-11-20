---
title: "From 2019-07 to 2022-12 the equal-weight universe re-equalised every day did worse than re-equalised monthly, so a benchmark's schedule is part of a trading claim"
kind: fact
area: market
source: "Run record H1001-r01 (train window 2019-07-01 to 2022-12-31): `benchmark` is the equal-weight universe re-equalised at every bar, `reference_equal_weight` the same universe re-equalised monthly; train data only"
trust: medium
date: 2026-11-18
---

Through the same engine and costs, over the train window from 2019-07-01:

| Equal-weight point-in-time universe | Net Sharpe ratio | Compound annual growth | Maximum drawdown | Cost a year |
|---|---:|---:|---:|---:|
| Re-equalised every bar | 0.33 | -16.4% | -91.5% | 3.5% |
| Re-equalised monthly | 0.47 | -4.2% | -89.9% | not in the record |

The gap in growth, about 12 points a year, is several times what the extra trading costs can explain (the monthly portfolio paid 1.2% a year over the whole train period, per the log). Re-equalising every day sells what rose and buys what fell each day; why that lost money in this window was not examined, and one window is one observation.

What it means for a trading claim: "the equal-weight universe" is not one benchmark. H1001's Sharpe difference on train is 0.66 against the daily one and 0.52 against the monthly one. Decide at registration which schedule the benchmark follows and why (`equal_weight(market, labels)` takes the schedule; the same schedule as the strategy isolates the rule from the rebalancing), and quote the reference benchmarks next to the estimate.

Not established: the cause, whether it holds in sub-periods, and anything outside train.
