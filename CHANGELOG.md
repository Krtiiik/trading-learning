# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Python project managed with uv, with pandas, yfinance and Parquet support.
- Learning site: a static knowledge base of concepts in six groups and lessons, built from Markdown by `learning/build.py`, with `[[slug]]` links, hover previews, search and planned concept pages.
- First learning site pages: concepts stock, order types, candle, moving average, trend following and stop loss, and the lesson "Reading your first candle chart".
- Learning site design: a hard-edged layout with hairline borders, light and dark themes, home page shelves with scroll arrows, per-group progress meters and colour kept for highlights.
- `learning/serve.py --open` opens the local learning site in the default browser once the server listens.
- Learning site content agents: a planner, a writer, a banner illustrator, a reviewer, a fact checker and a site-wide auditor, plus a `/write-page` skill that writes, checks and commits one page.
- Learning site concept pages: trend, price chart, OHLC, bid and ask, spread, indicator, strategy, timeframe, wick, volume, liquidity, gap, backtest, exchange, trading hours, fees and commissions, forex pair, position sizing, win rate and expectancy.
- Learning site favicon: a graduation cap with a bold rising trend line, in light and dark variants.
- `learning/build.py --words` prints the body word count of written pages by the site's length rule and fails when a concept is over 500 words, so writers and reviewers count the same way.
- Learning site theme switch: System, Light and Dark buttons in the header, so light mode can be chosen on a device set to dark. The choice is remembered in the browser.
- The learning site is deployed to GitHub Pages at <https://krtiiik.github.io/trading/> after every push to `main` that changes it.

### Changed

- Learning site pages now agree with each other: candle colours are hedged everywhere, "length" is the look-back setting and "period" one bar, candle uses the OHLC definitions, and the first candle chart lesson builds on the price chart and OHLC pages.
- Learning site: the stock, order types, stop loss and trend following pages explain their terms more fully and end with "Watch out" and "Next" sections; stop loss no longer promises a fixed maximum loss, and stock no longer describes US dividend habits as universal.

### Fixed

- Learning site: 18 catalog summaries that contain a comma were cut off at the comma. They now show in full, and the build fails on an unquoted comma.
- `learning/serve.py` tells the browser to check every file again, so a rebuilt stylesheet shows after a normal reload instead of an old cached copy.
