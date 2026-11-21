# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog starts when the learning site got its own repository. Earlier changes are in the git history.

## [Unreleased]

### Added

- Concept page: risk/reward, the possible gain on a trade compared with the possible loss, and the win rate a ratio needs to break even.
- Concept page: broker, what a broker does for you, the two kinds of broker, and the protection schemes that pay clients back when a broker fails (US, UK, EU).
- Concept page: drawdown, how far an account has fallen from its high, maximum drawdown, time under water, and the larger gain needed to recover.

### Changed

- The repository holds only the learning site and is named `trading-learning`. The site moves to <https://krtiiik.github.io/trading-learning/>; the old `/trading/` address stops working.
- Site sources are at the repository root. Build with `uv run python scripts/build.py` (output in `dist/`), preview with `uv run python scripts/serve.py --open`, test with `uv run pytest`.
- Concept pages agree with each other after a site-wide audit: "position size" means the number of shares (its money value is the position value), payment for order flow and slippage are named where they are described, US-only rules on the exchange page say so, and bid, ask, spread and colour wording is the same on every page.

### Removed

- The unused `trading` Python package and its data dependencies (pandas, yfinance, pyarrow, marimo).
