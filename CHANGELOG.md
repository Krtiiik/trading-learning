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

### Fixed

- `trading fetch` re-downloads a symbol in full after a new split, instead of appending post-split prices to pre-split history.
