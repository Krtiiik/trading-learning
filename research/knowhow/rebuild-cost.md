---
title: "Rebuilding the Store takes about half an hour and 3.7 GB; open interest would add hours"
kind: fact
area: data
source: "Rebuild runs on 2026-11-18"
trust: medium
date: 2026-11-18
---

`uv run trading rebuild` downloads 28,800 monthly daily-bar files for all 777 USDT pairs (6 minutes), 18,200 hourly files for the 363 pairs that were ever universe members, and 28,400 funding and basis files for the 339 of them with a perpetual contract. Result: 1.3 GB of Parquet under `data/binance/`, 1.0 GB of verified zips under `data/raw/`, and 1.4 GB of panel cache under `data/cache/` once hourly data has been loaded. With the raw cache in place a rebuild only re-parses (a few minutes).

Open interest is not in the default steps: it is one zip per coin per day, roughly 1,500 files per coin and about 400,000 files for all members. `uv run trading rebuild --steps open-interest` fetches it and will take hours; consider restricting it to the coins a hypothesis needs first. Timings depend on the network and were measured once.
