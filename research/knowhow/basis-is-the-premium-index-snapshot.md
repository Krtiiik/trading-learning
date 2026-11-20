---
title: "The stored basis is Binance's premium index: zero whenever the index price is inside the contract's impact spread, and its hourly close is one five-second snapshot"
kind: pitfall
area: data
source: "Data steward check on 2026-11-19, train data only (to 2022-12-31): binance/premium/1h id 5dd2d25c086b, binance/funding id 619020e39d56, binance/spot/1h id a7d21dafe920; one raw zip; definition from Binance's funding-rate FAQ, read 2026-11-19"
trust: high
date: 2026-11-19
---

**What it is.** The `premium` series is the archive's premium index klines: per hour the open, high, low and close of a number the exchange computes every five seconds (the raw file counts 720 samples an hour) as `[max(0, impact bid - index) - max(0, index - impact ask)] / index`, a fraction of the index price, positive when the perpetual trades above the index. It is not perpetual price over spot price minus one: it is exactly zero whenever the index lies between the contract's impact bid and ask. On train 18.7% of member-hours are exactly zero (1 to 3% for tier 1, 9 to 17% for tier 2, 18 to 29% for tier 3), and 20.6% of member-days in the daily panel. Perpetual prices are not in the Store, so the definition is confirmed only through funding: the exchange's formula applied to the eight hourly bars before a payment reproduces the funding rate with a median error of 0.002% and a rank correlation of 0.87 (281,078 payments).

**Size.** Member-hours with basis (894,032): median 0, mean -0.03%, 1st to 99th percentile -0.27% to +0.37%. The yearly median for tier 1 is +0.02% in 2020, +0.04% in 2021 and -0.04% in 2022. 2,487 member-hours are 1% or more in size; almost all of the 1,888 at 5% or more are frozen values of dead contracts (see the note on masking), the rest are real dislocations: 2021-05-19 12:00 and 13:00 for about twenty coins, OMG on 2021-11-08 to 11 (67 hours), SOL on 2022-11-09 and 10 (29 hours, to about -20%).

**One close is a noisy reading.** The hourly range (high minus low) has a median of 0.26%, several times the level. The daily panel's value is the last five-second sample of the day: across 129 coins its correlation with the mean of the day's 24 hourly closes has a median of 0.62, and its day-to-day autocorrelation a median of 0.37 against 0.78 for the daily mean (BTC: 0.86, 0.72 and 0.88). A hypothesis about the level of the basis should average it: take `series("premium", "1h")`, put it on the full hourly grid and use the mean of the last 8 or 24 hourly closes at each bar, which is knowable at that bar's close.

**Alignment, verified.** `series("premium", "1h")` at a label equals the close of the premium bar with the same label, and `series("premium", "1d")` at date D equals the close of the last premium bar labelled within D, normally 23:00, which closes with the daily bar: recomputed independently for every train column, no cell differs. 82 daily values come from an earlier hour because the 23:00 bar is missing (71 coins on 2020-12-01, from 22:00). 1,953 premium bars fall in hours without a spot bar and are not in the hourly panel.

**Gaps.** 0.70% of hourly labels are missing inside the contracts' own spans, nearly all in whole days missing for everyone: 2021-07-01, 2021-07-24 to 27 (every contract; the daily panel is NaN for all coins), 2022-10-02 (78 contracts, BTC among them, 22 of that month's members), and ICP from 2022-07-12 to 2022-09-27. No duplicated or off-grid label, no NaN, no high below low (10,159,179 bars over the whole history).

Not established: the perpetual's price or a true futures-minus-spot basis (not derivable from this series); anything after 2022.
