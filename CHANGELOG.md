# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Python project managed with uv, with pandas, yfinance and Parquet support.
- Daily bar download from Yahoo Finance behind a swappable provider interface, stored as Parquet per symbol with incremental updates.
- `load_bars()` and `load_panel()` to read stored bars into pandas for research.
