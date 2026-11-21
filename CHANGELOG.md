# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog starts when the learning site got its own repository. Earlier changes are in the git history.

## [Unreleased]

### Added

- Concept page: diversification, company-specific and market-wide risk, correlation, and why correlated positions add up to one larger bet.
- Concept page: support and resistance, levels where falls or rises stopped more than once, levels as zones, why they can work, role reversal, and placing a stop and a target around them.
- Concept page: candlestick pattern, common one- to three-candle patterns (doji, hammer, shooting star, engulfing, morning star), why context and confirmation matter, and why a pattern alone is a weak signal.
- Concept page: entry and exit rules, what makes a rule exact (condition, time, order), the kinds of exit, and turning a vague idea into exact rules.
- Concept page: mean reversion, buying a price far below its usual level and selling when it comes back, how far is measured, and why it has many small wins and a few large losses.
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

- Learning pages agree with each other after a second site-wide audit: CFDs are explained the same way and owned by the broker page, the drawdown page alone gives the recovery maths, the calm and jumpy stocks are described by their ATR, Bitcoin's volatility is worded the same on every page, an account's highest value is its "high" (not a "peak"), and the candle chart lesson now says a candle's colour compares its close with its own open.
- The repository holds only the learning site and is named `trading-learning`. The site moves to <https://krtiiik.github.io/trading-learning/>; the old `/trading/` address stops working.
- Site sources are at the repository root. Build with `uv run python scripts/build.py` (output in `dist/`), preview with `uv run python scripts/serve.py --open`, test with `uv run pytest`.
- Concept pages agree with each other after a site-wide audit: "position size" means the number of shares (its money value is the position value), payment for order flow and slippage are named where they are described, US-only rules on the exchange page say so, and bid, ask, spread and colour wording is the same on every page.

### Removed

- The unused `trading` Python package and its data dependencies (pandas, yfinance, pyarrow, marimo).
