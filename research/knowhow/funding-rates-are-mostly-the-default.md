---
title: "Half of all funding payments on train are exactly 0.01%, so a ranking by funding is mostly ties and its level is mostly the default"
kind: fact
area: data
source: "Data steward measurement on 2026-11-19, train data only (events up to 2022-12-31): binance/funding id 619020e39d56, binance/premium/1h id 5dd2d25c086b, binance/universe id 88f9a7cf72c7; formula from Binance's funding-rate FAQ, read 2026-11-19"
trust: high
date: 2026-11-19
---

Per payment, over the 284,664 events of the 183 train columns (2020 to 2022): the median is 0.0001 (0.01% per eight hours, 10.95% a year), and 50.1% of all payments are exactly 0.0001. The mean is 0.00012, 20.6% are negative, the 1st and 99th percentiles are -0.14% and +0.24%, the extremes -2.5% and +0.75% (the exchange's floor and cap; 327 payments sit at -0.75% and 475 are at least 0.75% in size).

| Year | Payments | Mean per payment | Exactly 0.01% | Negative | 1st to 99th percentile |
|---|---|---|---|---|---|
| 2020 | 41,122 | 0.0138% | 57% | 10% | -0.25% to 0.20% |
| 2021 | 109,686 | 0.0322% | 49% | 10% | -0.10% to 0.31% |
| 2022 | 133,728 | -0.0048% | 49% | 33% | -0.14% to 0.01% |

Per daily bar on member-days (37,126): median 0.0003, mean 0.00049 (18% a year), 5th to 95th percentile -0.10% to 0.33%, 30% exactly 0.0003 and 22% negative. The mean per day annualises to 19% in 2020, 41% in 2021 and -6% in 2022: the level is a regime, not a constant. Across members on one day the standard deviation of daily funding has a median of 0.058%, and on 234 of the 914 days from 2020-07 more than half of the members with funding have exactly 0.0003.

Why: the rate is the average premium index over the interval plus a term that pulls it to 0.01% whenever that average lies between -0.04% and +0.06% (the exchange's formula). The data agree: where the eight-hour mean of the stored hourly premium is inside that band, 84% of payments are exactly 0.0001, and the formula applied to hourly bars reproduces the rate with a median error of 0.002% (rank correlation 0.87).

What to do: a cross-sectional rank of funding needs a rule for ties (half the coins share one value on a quiet day), and "funding above its default" is a different and sparser signal than "funding". The basis is continuous where funding is clipped; consider it when the hypothesis is about the size of the premium. Winsorise or rank: the few squeeze days (a daily sum of -16% for OMG on 2021-11-11) dominate any mean.

Not established: anything after 2022; these are descriptive facts from train and not a finding about returns.
