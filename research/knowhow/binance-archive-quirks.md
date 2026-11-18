---
title: "The Binance archive has format quirks that are handled in the provider and nowhere else"
kind: pitfall
area: data
source: "Found while building trading/data/providers/binance.py on 2026-11-18; each has a test in tests/test_binance.py"
trust: high
date: 2026-11-18
---

- **Timestamp unit changes.** Spot kline times are milliseconds until 2024-12 and microseconds from 2025-01. Futures files stay in milliseconds.
- **Headers come and go.** Spot kline files have no header row; futures files do.
- **Funding times are a few milliseconds late** (08:00:00.003): they are rounded to the minute.
- **Off-grid hourly bars.** After the outage of 2018-02-08 the six pairs then listed have 43 hourly bars that open 28 minutes past the hour. They are dropped: relabelled, their contents would not be knowable at label plus one hour. Daily bars are unaffected.
- **Symbol reuse.** `LUNAUSDT` is the old Luna until 2022-05-13 and a different coin from 2022-05-31; `USDSUSDT` is one stablecoin until 2020 and another from 2026. The earlier coin is stored as `LUNAUSDT-2022`, `USDSUSDT-2020`.
- **Redenominations under the same symbol**: BTCST, COCOS, DREP, SUN (2021), VIDT (2022), BNX, QUICK (2023), STRAX (2024). Found as a trading gap followed by a price ratio near a power of ten; stored like splits. The ratios 10 for BTCST and VIDT rest partly on memory of the swap terms (the data shows 0.13 and 0.05 across the gap): medium trust for those two.
- **Perpetuals quoted per 1000 coins** (`1000SHIBUSDT`, `1000PEPEUSDT`): funding and basis are scale-free and are stored under the spot symbol.
- **Stray files**: a few `metrics` files dated 1993; symbols that are not ASCII; one empty symbol folder (`USDSOLDUSDT`).

If a new oddity appears, `uv run trading verify --quality` lists symbols with missing bars or extreme jumps; fix it in the provider with a test, then rebuild.
