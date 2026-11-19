---
title: "On the point-in-time universe the asset-permutation placebo needs a fixed set of coins, and for a trend signal only the time-shift placebo should come out at nothing"
kind: how-to
area: statistics
source: "Skeptic review of H1001 on 2026-11-19, train data only (binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7); the results are in the 'Skeptic review' section of research/hypotheses/H1001-trend-filter-on-daily-bars.md"
trust: medium
date: 2026-11-19
---

A research market has a column for every coin that was ever a member (183 on train) while 40 are members at a time, and most coins have no bars for much of the period. Two consequences for the placebo tools in `trading.stats`:

- `asset_permutation_test` permutes whole columns. Across all columns it mostly hands a member the signal of a coin that had not been listed yet, which is "no signal", not "another coin's signal". Run it on coins that are members throughout: on train from 2019-07 eight coins are members at all 42 reconstitutions (ADA, BNB, BTC, ETH, LINK, LTC, TRX, XRP), and the real estimate has to be recomputed on that same sub-universe to compare.
- `circular_shift_test` on a bars x coins signal rolls all coins together, which keeps what coins have in common. A coin listed inside the window gets "no signal" rolled onto part of its membership, so the placebo is invested somewhat less than the real rule; report the placebo's average invested weight next to its estimate. Roll only the rows of the evaluation window and leave the earlier rows as they are, so the positions carried into the window stay real.

Which placebo should give nothing depends on the signal. Trend signals of different coins agree on most bars, so a coin's slot switched by another coin's signal still times the market: for a trend rule the asset permutation measures how much of the effect is common to all coins, and it is not a test that should fail. The time shift is the placebo that should lose to the benchmark (by about the rule's costs), and the complement rule (hold when the signal is off) should mirror the real estimate. State in the review which of the placebos is expected to come out at nothing before reading the result.

Not established: anything for signals that are not shared across coins (a cross-sectional rank, a funding rate), where the asset permutation is the natural placebo.
