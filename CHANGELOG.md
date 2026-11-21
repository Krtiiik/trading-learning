# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog starts when the learning site got its own repository. Earlier changes are in the git history.

## [Unreleased]

### Added

- Concept page: index, what an index tracks, major indices by market, cap-weighted and price-weighted indices, points and percent, and how people trade an index.
- Concept page: peak and trough, how to spot turning points (swing highs and lows), why they are confirmed late, and how they place stops and targets.
- Concept page: line vs candle chart, the same prices drawn two ways, what a line hides (swings and gaps), and bar charts.
- Concept page: ATR (average true range), true range on a gap day, Wilder's average, and using ATR to set the stop and the position size.
- Concept page: risk/reward, the possible gain on a trade compared with the possible loss, and the win rate a ratio needs to break even.
- Concept page: broker, what a broker does for you, the two kinds of broker, and the protection schemes that pay clients back when a broker fails (US, UK, EU).
- Concept page: leverage, the leverage ratio, margin, margin calls and stop outs, and the leverage limits for private traders in the EU, UK and US.
- Concept page: cryptocurrency, what a coin and a blockchain are, keys and wallets, stablecoins, crypto pairs, and who holds your coins on an exchange.
- Concept page: volatility, how big a price's moves are (not their direction), how traders measure it, and how it sets the stop, the position size and the target.
- Concept page: drawdown, how far an account has fallen from its high, maximum drawdown, time under water, and the larger gain needed to recover.

### Changed

- The repository holds only the learning site and is named `trading-learning`. The site moves to <https://krtiiik.github.io/trading-learning/>; the old `/trading/` address stops working.
- Site sources are at the repository root. Build with `uv run python scripts/build.py` (output in `dist/`), preview with `uv run python scripts/serve.py --open`, test with `uv run pytest`.
- Concept pages agree with each other after a site-wide audit: "position size" means the number of shares (its money value is the position value), payment for order flow and slippage are named where they are described, US-only rules on the exchange page say so, and bid, ask, spread and colour wording is the same on every page.

### Removed

- The unused `trading` Python package and its data dependencies (pandas, yfinance, pyarrow, marimo).
