---
title: "Universe exclusions are a hand-made list, and new listings need a look"
kind: how-to
area: data
source: "trading/data/pit_universe.py; listing of all 776 USDT base assets on 2026-11-18"
trust: medium
date: 2026-11-18
---

Stablecoins and fiat pairs, wrapped and staked tokens, gold tokens, leveraged tokens and tokenised stocks are excluded by name, because names alone do not tell them apart (JUP is a coin, BTCUP a leveraged token). A volatility net catches unlisted pegged pairs: a pair whose daily returns had a standard deviation below 0.5% over the 30-day lookback is not ranked. On the full history the net caught only two pairs the list missed, both stablecoin-like and both in 2026.

About 110 pairs ending in `B` (AAPLB, NVDAB, SPYB ...) appear from June 2026. They are treated as tokenised stocks because the names are US tickers and they were listed in monthly batches; nobody here has confirmed it from a primary source. They all fall in the test period.

When the Store is rebuilt after new listings, list bases that are in neither the universe nor the exclusion list and classify the unfamiliar ones before trusting the newest reconstitutions.

Measured by the Data steward on 2026-11-18 on the 63 train reconstitutions (binance/spot/1d id 2d6763395242): the list does real work. Ranking without it would put on average 2.9 excluded pairs in the top 40 (3.8 from 2019-07, at most 12): USDC at 44 reconstitutions, BUSD 38, TUSD 28, PAX 24, EUR 16, UST 4, GBP 2, and leveraged tokens (BTCUP, BTCDOWN, the BULL and BEAR pairs and others) at one to four each. None of the 183 pairs that are members on train is on the list, and the volatility net removed nothing on train: the calmest member-month has a daily return standard deviation of 1.2%. Whether a base that is neither listed nor pegged is an ordinary coin was judged by reading the 182 names, not measured.
