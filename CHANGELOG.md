# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog starts when the learning site got its own repository. Earlier changes are in the git history.

## [Unreleased]

### Changed

- The repository holds only the learning site and is named `trading-learning`. The site moves to <https://krtiiik.github.io/trading-learning/>; the old `/trading/` address stops working.
- Site sources are at the repository root. Build with `uv run python scripts/build.py` (output in `dist/`), preview with `uv run python scripts/serve.py --open`, test with `uv run pytest`.

### Removed

- The unused `trading` Python package and its data dependencies (pandas, yfinance, pyarrow, marimo).
