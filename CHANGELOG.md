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
- Learning site concept page: trend.
- The learning site is deployed to GitHub Pages at <https://krtiiik.github.io/trading/> after every push to `main` that changes it.
