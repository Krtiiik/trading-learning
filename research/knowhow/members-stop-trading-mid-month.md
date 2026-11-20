---
title: "Nine train members stop trading during a month of membership; nothing else is missing from members' daily bars"
kind: pitfall
area: data
source: "Data steward check on 2026-11-18, every (reconstitution, member) up to 2022-12: binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-18
---

Train has 1,980 member-months and 60,307 member-days. 147 member-days (0.24%) have no daily bar, all of them after the last bar of a pair that ended while it was a member. No member misses a bar and trades again within its membership.

| Pair | Rank that month | Last bar | Member-days without a bar | What ended it (from memory, not measured) |
|---|---|---|---|---|
| BCCUSDT | 5 | 2018-11-20 | 14 (no bars 16th to 19th either) | fork into BCHABC and BCHSV |
| BCHSVUSDT | 18 | 2019-04-22 | 8 | delisted |
| BCHABCUSDT | 5 | 2019-11-28 | 2 | renamed BCH |
| ERDUSDT | 38 | 2020-08-31 | 30: all of September 2020 | swap to EGLD |
| LENDUSDT | 22 | 2020-10-12 | 19 | swap to AAVE |
| NPXSUSDT | 29 | 2021-04-05 | 25 | swap to PUNDIX |
| BTTUSDT | 29 | 2022-01-17 | 14 | swap to BTTC |
| LUNAUSDT-2022 | 5 | 2022-05-13 | 18 | collapse, trading halted |
| HNTUSDT | 34 | 2022-10-14 | 17 | delisted |

ERDUSDT is the odd one: its last bar is the last day of August, it had a bar on all 30 lookback days, so it is a member for September without a single bar.

What follows from it. The engine values a coin without a bar at its last close and sells it there at the next trade; a target weight on a coin with no bar is dropped into cash. Measured on the equal-weight benchmark: `dropped_weight` is 0.025 over train, which is ERD in September 2020 (the benchmark holds 39 coins and 2.5% cash that month). A rule must come out flat when its signal is NaN, not carry the last value. A pair's last bar covers only the hours before the halt (0.7 hours for LUNA, 2 to 10 for the others), and its close is the last trade: selling there assumes the holder got out before the halt. Delisting announcements are not in the Store, so a rule cannot leave early as a trader who read them could.

Not established: whether that last close was achievable in size, and what holders of the swapped coins received (the successor symbol is a separate coin in the Store; see the note on renamed coins).
