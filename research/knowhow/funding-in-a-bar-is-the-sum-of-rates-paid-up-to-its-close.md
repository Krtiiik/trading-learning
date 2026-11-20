---
title: "Funding in a daily bar is the sum of the rates paid after 00:00 up to and including 24:00 UTC; in the hourly panel a rate sits only in the bar that closes at the payment"
kind: fact
area: data
source: "Data steward check on 2026-11-19 of `ResearchData.series('funding', ...)` against the stored events up to 2022-12-31: binance/funding id 619020e39d56, binance/spot/1d id 2d6763395242, binance/spot/1h id a7d21dafe920, raw zips under data/raw/"
trust: high
date: 2026-11-19
---

The Store holds one row per funding payment of a coin's perpetual contract: the payment time, `rate` (a fraction of the position paid by longs to shorts when positive) and `interval_hours`. In the 3,342 raw files up to 2022-12 the 298,586 stamps are 0 to 47 ms after a whole hour and never before it; the provider rounds them to the minute.

- **`series("funding", "1d")`** at date D is the sum of the rates stamped after D 00:00 up to and including D+1 00:00: normally three, paid at 08:00, 16:00 and 24:00. The payment at 00:00 of D belongs to bar D-1. Recomputed with plain date arithmetic for all 284,664 events of the 183 train columns: none of the 94,865 filled cells differs. By hand, BTC on 2021-05-19: 0.00035813 (08:00) - 0.00089697 (16:00) + 0.0001 (24:00) = -0.00043884, the panel's value. 94,796 bars hold three payments, 47 hold one or two (a contract's first day) and 22 hold four to twelve (see below).
- **`series("funding", "1h")`** has a value only in the bar labelled one hour before a payment (07:00, 15:00, 23:00) and NaN in the other 21 hours of the day. NaN there means "no payment in this hour", not "no data". For the latest known rate carry the value forward (on the full hourly grid); for funding over the last day sum 24 hours with `min_count=1`. Do not average the panel over time without that.
- **Knowable at the close.** The last payment in a bar is stamped exactly at the bar's close, and its rate is fixed by samples up to that instant, so a decision taken at that close and traded at the next open uses nothing from later. Nothing stamped after a bar's close is in it (checked for every event).
- **Lost in outages.** At four payments the hour that closes at the payment has no spot bar (2020-02-19 16:00, 2020-12-21 16:00, 2021-04-25 08:00, 2021-09-29 08:00), and the hourly panel drops those 305 events (22, 72, 100 and 111 coins); the daily panel keeps them. Summing the hourly panel over a day therefore differs from the daily panel on those four days.
- **Interval.** 299,949 of the 300,131 train events are eight hours apart. The exchange shortened the interval to two or four hours during four squeezes: OMG on 2021-11-11, SOL and FTT from 2022-11-09 to 2022-11-18, HNT from 2022-12-21 to 2022-12-26 (182 events, many at the floor of -2% to -2.5% per payment; SOL's bar of 2022-11-10 sums eleven payments to -15.4%). The sum per bar handles any interval; a per-event rate is not comparable across intervals, so use bar sums or divide by `interval_hours`.
- **Structure.** No duplicated stamp, no NaN, every stamp on a whole hour (1,664,031 events over the whole history). One series has a hole: BTCST from 2021-12-09 to 2022-02-15 (203 payments).

Not established: values after 2022-12-31; that the archive's rate equals what the exchange charged (only internal consistency with the basis was checked, see the note on the premium index).
