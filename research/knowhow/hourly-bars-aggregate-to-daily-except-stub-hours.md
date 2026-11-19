---
title: "Hourly bars of all 183 train members aggregate to their daily bars, except single-trade stub hours in December 2021 and two days of differing volume"
kind: pitfall
area: data
source: "Data steward check on 2026-11-19, bars up to 2022-12-31: binance/spot/1h id a7d21dafe920, binance/spot/1d id 2d6763395242, one raw zip under data/raw/"
trust: high
date: 2026-11-19
---

For every coin that is a member at some train reconstitution, over its whole history to 2022-12-31, the 24 hourly bars of a UTC day were aggregated (first open, highest high, lowest low, last close, summed quote volume) and compared with the daily bar: 167,464 coin-days with 24 hourly bars.

- **Prices agree** on all but 94 of the 669,856 values. 59 are opens (and a few highs and lows) of thin coins in 2019-08 to 2020-10 whose first hours of the day have no trade: the hourly bar is flat at the previous close, the daily open is the day's first trade, up to 1.8% away. Aggregating only hours with trades reproduces the daily bar exactly, so both are right. The other 35 are the stub hours below (34) and DOGE's close on 2021-10-28 (0.03%, one trade).
- **Stub hours, December 2021.** On the 2nd, 4th, 5th, 7th to 14th and 23rd to 27th, 344 hourly bars of 115 coins hold exactly one trade (open = high = low = close, a volume of a fraction of a coin) while the hours around them hold thousands and the daily bar holds the whole day; 69 of them are bars of that month's members (19 coins, 55 coin-days). The raw archive file has the same row (AXSUSDT 2021-12-05 23:00: 1 trade, 0.38 coins), so it is the archive, not the parser. On those 252 coin-days the hourly quote volume sums to less than the daily bar, typically by 2% and by up to 22%. The stub's close is the hour's first trade, so it is stale, not from the future: where the stub is the 23:00 bar the hourly close is up to 2.1% from the daily close (DYDX 2021-12-07) and the next hourly open jumps by as much. BTC and ETH have none.
- **Volume otherwise** equals the daily bar within 1e-6, except 2021-01-21 (124 coins: the hourly sum is higher, by 2.0% in total and up to 7% for a coin, prices equal), 2021-04-23 (133 coins: lower by 0.09% in total) and 2022-04-13 (59 coins: 2e-5). Which granularity is right on those days is unknown.
- **Days with fewer than 24 hourly bars** (2,157 coin-days: outages, first and last days): the hourly high and low stay inside the daily range, the open equals the daily open when the 00:00 bar exists and the close when the 23:00 bar exists, without exception. Twelve coin-days have a daily bar and no hourly bar at all (the six pairs listed on 2018-02-09 and 2018-02-10).
- **Values.** Among the 4,063,719 hourly bars: no duplicate label, no missing or non-positive price, no high below low, no open or close outside the range. 1,558 bars have zero volume; all are flat and have zero trades (see the note on outages).

What to do: daily and hourly bars can be mixed in one hypothesis (a daily signal traded on hourly bars) without a seam. A signal built on hourly volume, trade count or range must not read a December 2021 stub or a flat maintenance hour as a quiet market: require a minimum trade count, or use a median over several hours. An hourly return into a stub is small and the move appears in the next bar, so hourly return series are shifted by at most an hour there, never wrong in total.

Not established: that either granularity equals what traded (only their agreement was checked); whether stub hours exist after 2022 (the same count over the whole history was not made, to keep away from test-period values).
