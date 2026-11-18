---
title: "The point-in-time universe has fewer than 40 members before July 2019"
kind: fact
area: data
source: "data/binance/universe (id 88f9a7cf72c7), counted 2026-11-18"
trust: high
date: 2026-11-18
---

Binance listed few USDT pairs at first: the universe has 2 members in October 2017, 5 in January 2018, 19 in January 2019, and reaches 40 on 2019-07-01. From then on it is always 40. On average 6 members change at a reconstitution over the whole train period; counted only from 2019-08, when there are 40, it is 8 of the 40 (between 2 and 16).

Consequences: cross-sectional hypotheses effectively have a train period of 3.5 years (2019-07 to 2022-12), not 5.4. Anything measured per coin before mid-2019 rests on a handful of coins. State the start date you use in the hypothesis file and pass it to `trading research mde --start`.

Added by the Data steward on 2026-11-18 (daily market to 2022-12-31, binance/spot/1d id 2d6763395242): the first reconstitution is 2017-10-01, because no pair has 30 daily bars on 2017-09-01. The first 45 train days (2017-08-17 to 2017-09-30) therefore have no member at all, and the equal-weight benchmark holds cash on them (45 bars with nothing invested). Members with a bar per day: 2 until the end of 2017 (the benchmark is half BTC, half ETH), 5 to 8 in the first half of 2018, 12 to 18 in the second, 19 to 39 in the first half of 2019. Of the 281 week ends on train, 236 have at least 10 members and 166 have all 40. A rule that holds 1/N per coin is a different portfolio in each of these stretches; time-series hypotheses need a stated start date as much as cross-sectional ones.
