---
title: "The Binance public archive supports a point-in-time universe: delisted pairs are kept and every file is checksummed"
kind: fact
area: data
source: "Bucket listing of data.binance.vision, probed 2026-11-18 (all spot kline prefixes and all USDT-margined futures prefixes)"
trust: high
date: 2026-11-18
---

What it offers, as measured:

- **Spot klines** for 3,767 symbols, 776 of them USDT pairs, as monthly zips per symbol and granularity. BTCUSDT and ETHUSDT start 2017-08-17. Of the USDT pairs, 253 end before the latest month: delisted pairs stay in the archive (BCCUSDT ends 2018-11, SRMUSDT 2022-11, USTUSDT 2022-05), which is what a point-in-time universe needs.
- **Checksums**: every zip has a `.CHECKSUM` file (SHA-256), and the bucket listing's ETag is the file's MD5. The provider verifies each download against the ETag.
- **Funding rate** (`futures/um/monthly/fundingRate`): 924 USDT perpetuals, from 2020-01.
- **Basis** (`premiumIndexKlines`, 1h): same contracts, from 2020-01. Mark-price and index-price klines also exist and are not stored.
- **Open interest** (`futures/um/daily/metrics`, 5-minute snapshots with long/short ratios): BTCUSDT from 2020-09-01, almost everything else from 2021-12-01. One zip per coin per day, 6.5 GB in total; not fetched by default.

Limits: the archive publishes a month after it ends, so the Store stops at the last complete month (2026-10 when built). Before 2020 there is no derivatives data at all, and before 2021-12 no open interest, so derivatives hypotheses have a short train period (three years, or one for open interest). There are no order books, no trades in the Store, no market capitalisation (so "size" must be proxied by volume), and no on-chain or sentiment data.
