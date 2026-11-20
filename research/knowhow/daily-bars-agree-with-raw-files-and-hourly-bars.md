---
title: "Daily bars of train members are labelled by UTC date, equal the raw archive rows and the 24 hourly bars, and contain no impossible prices"
kind: fact
area: data
source: "Data steward check on 2026-11-18, bars up to 2022-12-31: binance/spot/1d id 2d6763395242, binance/spot/1h id a7d21dafe920, raw zips under data/raw/"
trust: high
date: 2026-11-18
---

Measured on the 183 coins that are universe members at some train reconstitution, over their whole history up to 2022-12-31:

- **Labels.** BTCUSDT and ETHUSDT each have 1,963 daily bars from 2017-08-17 to 2022-12-31: none missing, none duplicated. Every member's labels are unique, increasing, tz-naive midnights.
- **Raw files.** The 5,671 monthly raw files hold 169,633 rows, exactly the stored row count. Every `open_time` is a multiple of 86,400,000 ms (00:00:00.000 UTC), so normalising to a date hides nothing. 22 rows cover less than 24 hours: 17 are a pair's last bar (0.7 to 10 hours of trading before the halt) and 5 precede a trading halt (BCC 2018-11-15, BTCST 2021-03-15, COCOS 2021-01-19, FTT 2022-11-15, CVC 2022-12-09).
- **Hourly bars.** On days with 24 hourly bars the daily open, high, low and close equal the hourly aggregate by UTC date: BTC and ETH 1,932 of 1,932 days, LUNAUSDT-2022 620 of 620, DOGE 1,258 of 1,258 except one close 0.03% apart (2021-10-28, unexplained). Cutting the day one hour later matches at most 23 closes, so the labels are UTC dates. Daily quote volume equals the hourly sum within 1e-6 except on 2021-01-21 (2.4% apart for BTC, ETH and DOGE alike), 2021-04-23 (0.1%) and 2022-04-13; which granularity is right on those days is unknown. On the 29 train days with fewer than 24 hourly BTC bars (outages) the daily bar still exists.
- **Values.** Among the 60,160 bars inside member-months: no missing or non-positive price, no high below low, no open or close outside the range, `adj_close` equals `close` everywhere, and one bar without volume (BCCUSDT 2018-11-20, a 3-hour bar after the fork halt, its last).
- **Continuity.** Over 169,450 consecutive bar pairs the open differs from the previous close by a median of 0.04%; only 3 steps exceed 5% (PERL 20% and DOGE 6% on 2020-03-13, BEAM 6% on 2020-09-06). An unrecorded redenomination or reused symbol would show here and does not.
- **Jumps.** Nine closes quadrupled or fell by three quarters in one bar: LUNAUSDT-2022 on 2022-05-11, 12 and 13 (a member, rank 5), FTT on 2022-11-08, and DOGE 2021-01-28, GXS 2021-12-02, NU 2021-10-15, ONG 2021-05-20, UNFI 2022-06-07 (none a member that month). Each is on consecutive bars and happens inside the bar, so they are trades, not relabelling. `verify --quality` lists 44 symbols with jumps over the whole history; the others are leveraged tokens or lie outside train.

The two redenominations in these histories (BTCST 2021-03-19, COCOS 2021-01-23) fall outside member-months; a lookback of more than 7 months from BTCST's first membership (2021-11) or 10 from COCOS's return (2021-12) crosses one, and BTCST's ratio is of medium trust (see the archive quirks note).

Not established: that the archive equals what traded on the exchange (only checksums and internal agreement were checked); anything value-level after 2022-12-31.

Added by the Data steward on 2026-11-19: the hourly comparison was repeated for all 183 train members (167,464 coin-days). It holds, with exceptions that are all on the hourly side or in volume: see the note on hourly bars aggregating to daily bars.
