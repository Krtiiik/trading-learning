# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Python project managed with uv, with pandas, yfinance and Parquet support.
- Daily bar download from Yahoo Finance behind a swappable provider interface, stored as Parquet per symbol with incremental updates.
- `load_bars()` and `load_panel()` to read stored bars into pandas for research.
- `universe.toml` listing the starter ETF universe (index, bond, commodity and sector ETFs).
- Sanity checks on daily bars: duplicate dates, bad prices, inconsistent OHLC, missing or extra NYSE sessions, and large moves without a split.
- `trading fetch` command to download the universe or given symbols, with `--full` to re-download and validation warnings per symbol.
- marimo notebook `notebooks/explore_bars.py` comparing growth, statistics, drawdowns and raw vs adjusted prices of stored symbols.
- Course site in `learn/`, built with Jekyll: a course dashboard, lesson and reference layouts with a course sidebar and on-page contents, and light and dark themes.
- Jekyll includes for the course's content components: multiple-choice and numeric questions, notes, key ideas, tables, reveals and slider tables, with formulas typeset by KaTeX.
- Ask Claude on every page of the published course: a side chat about the page, and "Explain this" or your own question on text selected in a lesson. Chats are saved per page for the course owner.

### Changed

- The three course lessons and the bars-and-stats reference sheet are now Markdown pages of the course site, with formulas in LaTeX; the standalone HTML pages and their stylesheet are gone.

### Fixed

- `trading fetch` re-downloads a symbol in full after a new split, instead of appending post-split prices to pre-split history.
- Sanity checks report a large close move on a split day as history stored before the split, instead of treating the split as explaining it.
