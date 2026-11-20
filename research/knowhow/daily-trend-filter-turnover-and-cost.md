---
title: "A 20-day trend filter evaluated every day across the 40 members turns the portfolio over 22 to 24 times a year and pays about 10% a year in costs"
kind: fact
area: time-series
source: "Run records H1001-r01 (train window 2019-07-01 to 2022-12-31) and H1001-r02 (dev), metrics `turnover_per_year` and `cost_per_year`"
trust: high
date: 2026-11-18
---

H1001 holds each member's 1/40 slot only while the coin's close is above its 20-day average and re-equalises the slots at every bar. Its one-way turnover is 22.4 times the portfolio a year on train and 23.5 on dev, at an average invested weight of 0.43 and 0.46, and it pays 9.9% and 10.4% of the portfolio a year in costs. Its benchmark, the equal-weight universe re-equalised every bar, turns over 7.5 times a year and pays 3.5% a year for the re-equalising alone. Doubling costs lowers the Sharpe difference between the two by about 0.2 (0.18 on train, 0.21 on dev).

Before the run I had worked out 6% a year for the filter's switches from the one published turnover figure for this rule (7.95% of the position a day for Bitcoin, 2010 to 2018, Detzel et al.) and our average slot cost of 22 bps a side, and had left the re-equalising of held slots as an unknown extra. The record shows about 60% more in total. So a single-coin turnover figure from the literature understates what a per-coin rule costs across the universe with daily re-equalising, and a cost estimate made that way should be raised by at least half.

What to do: normal costs are already inside a trading claim's estimate, and doubling them takes about another 0.2 off a rule that decides every day. A hypothesis of that kind that predicts a net gain of 0.2 to 0.3 in Sharpe ratio is predicting something double cost roughly erases; one that expects so little should decide less often, and say so at registration.

Not established: how the cost splits between the filter's switches and the re-equalising of held slots, how it varies by year or tier, and how any other lookback or schedule behaves. None of those was run.
