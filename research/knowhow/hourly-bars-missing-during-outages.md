---
title: "Hourly bars are missing for every coin during exchange outages"
kind: fact
area: data
source: "Hourly train market (to 2022-12-31), datasets binance/spot/1h id a7d21dafe920 and binance/universe id 88f9a7cf72c7; first measured 2026-11-18, member-month accounting by the Data steward on 2026-11-19"
trust: high
date: 2026-11-19
---

The hourly panel's index is the union of bar labels that exist, so an outage is a jump in the index, not a row of NaN. On train the index has 46,949 labels where a full hourly grid has 47,108: 159 hours (0.34%) are missing for every coin, in 26 runs. One is 75 hours long (2018-02-08 01:00 to 2018-02-11 03:00, the outage plus the dropped off-grid bars); the other 25 last 1 to 10 hours. By year: 7 hours in 2017, 94 in 2018, 28 in 2019, 17 in 2020, 13 in 2021, none in 2022.

Counted over the 1,980 train member-months (1,447,368 member-hours):

| Why an hour has no bar for a member | Member-hours | Share |
|---|---|---|
| Label missing for every coin (outage) | 2,853 | 0.197% |
| Label exists, this coin has no bar | 185 | 0.013% |
| After the pair's last bar (it stopped trading mid-month) | 3,609 | 0.249% |

1,340 member-months miss nothing; the 90th percentile is 5 missing hours, the 99th is 10, and three months stand out: BCC in 2018-11 (112, the fork halt from 2018-11-15 17:00), every member in 2018-02 (75) and in 2018-06 (11). The 185 single-coin hours are that BCC halt (105) and one outage that left its labels in the index: on 2018-06-26 02:00 to 11:00 the eight members have NaN while three other pairs have flat bars. So for a member, a gap is in practice always an outage shared by all coins. A coin never misses a single hour on its own on train (over the whole train history of the 183 members, the only other single-coin gaps are the four-day halts before the BTCST and COCOS redenominations).

An outage shows up in two more forms, both a bar that exists but carries nothing: a flat bar (open = high = low = close = the previous close, zero volume, zero trades) for every coin at 2019-06-07 21:00, 2020-12-21 14:00 and 2021-02-11 03:00, and for some at 2019-06-07 20:00 and 2021-04-25 04:00. Thin coins also have flat hours of their own: 1,558 zero-volume hourly bars in all (0.04% of 4,063,719), 219 of them inside member-months (FTT 22 in 2020-02 to 2020-04, STX 14, IOTX 12, the rest ones and twos). A flat bar is honest (nothing traded) but a zero hourly volume or a zero hourly return is not a signal about the coin.

What this means: a "24-bar" lookback is not always 24 hours (see the note on computing an N-hour return). The engine prices a coin without a bar at its last close and returns span the gap correctly. Annualising with 8,760 bars a year overstates the count by 0.3% over train (8,666 bars in 2018, 8,760 in 2022). Daily bars have no gaps for BTC and ETH.

Not established: anything after 2022-12-31 beyond the manifest check, and whether a gap in the archive was an hour without trading or an hour the archive lost.
