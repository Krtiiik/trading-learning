# Architecture

<!--
The big picture and the reasons behind it, for Claude.
Don't list files, classes or signatures: the source shows those.
Write what a newcomer couldn't work out by reading the code: how the parts fit together,
why a design was chosen over the obvious alternative, and the constraints that shaped it.
-->

## Overview

A personal research workbench for learning algorithmic trading. So far it covers market data: download daily bars for a universe of US ETFs from a free provider, keep them locally, sanity-check them, and load them into pandas for research in marimo notebooks.

## Components and flow

`trading fetch` → for each symbol in the universe, the update step asks a provider for bars (everything, or only since the last stored bar) → normalizes them into the common bar shape → writes them to the store → runs the sanity checks and prints issues as warnings.

Research code never talks to a provider: it reads the store through `load_bars` / `load_panel`, so notebooks work offline and see the same data every time.

## Design notes

**Provider behind a protocol.** yfinance is an unofficial scraper that can break or be rate-limited; keeping it behind a small interface lets Stooq, Alpaca or a paid source replace it without touching storage or research code. Providers normalize to one bar shape so nothing downstream knows where data came from.

**Raw prices plus adjusted close, not fully adjusted OHLC.** Raw prices are the truth and never change; the adjusted close gives total returns. Fully adjusted OHLC can be derived when needed. Storing only adjusted data would lose the real traded prices.

**Incremental updates re-fetch the last stored bar.** A bar stored while its session was open gets replaced by final values. Comparing that bar's adjustment factor with the provider's tells whether a new dividend or split re-adjusted history; if so the symbol is downloaded in full, since the stored adjusted closes are stale.

**Parquet per symbol, data not in git.** Typed, compressed, fast with pandas, trivially inspectable per symbol, and appending one symbol never rewrites others. Data is reproducible from `trading fetch` and redistributing Yahoo data would break its terms, so `data/` is gitignored.

**Sanity checks warn, never block.** Free data regularly has gaps and real extreme moves (e.g. silver on 2026-01-30); refusing to store it would leave no data. Issues are surfaced so research can decide.

**Daily index is tz-naive trading dates.** A daily bar belongs to a session date, not an instant. Intraday bars, once added, should use tz-aware UTC timestamps.
