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
- Vectorised backtest engine in `trading.backtest`: target weights against open and close prices, signal at a bar's close and trade at the next open, long or flat, with rows that hold instead of rebalancing, a per-side cost model (10 bps fee plus slippage by liquidity tier) and a double-cost multiplier. Annualisation follows from granularity and calendar.
- Hourly granularity (`1h`) and crypto market data from the Binance public archive: spot bars with quote volume, plus funding rate, basis and open interest of perpetual contracts as series. Downloads are checksum-verified and cached.
- `trading rebuild` rebuilds the crypto datasets from nothing in one command, and `trading verify` checks every dataset against its manifest.
- Point-in-time universe: the top 40 USDT spot pairs by trailing 30-day quote volume at each monthly reconstitution, with stablecoins, wrapped, pegged and leveraged tokens excluded, delisted coins kept, and a liquidity tier per coin.
- Dataset manifests with content hashes, so the data behind a result can be identified; `trading fetch` now writes one for the ETF bars too.
- Research process in `trading.research` with `trading research` commands: a chronological split (train to 2022, dev 2023-2024, test from 2025) whose test segment is sealed in code and opened once for at most five finalists; hypothesis files registered by committing them; a harness that refuses unregistered or altered hypotheses and uncommitted code, checks every experiment for look-ahead and writes the run record itself; a claim ladder with false-discovery control computed from the records; and a generated catalogue. Experiments are evaluated with shared helpers that report every trading claim at double cost against benchmarks run through the same engine, refuse weights on coins outside the point-in-time universe, and give research the ETF bars only up to the end of its segment. A hypothesis can be replayed on train for a Skeptic review, whose verdict is written into the hypothesis file.
- Research records in `research/` (hypotheses, run records, know-how notes, literature notes, a generated catalogue, a log and a guide for newcomers), four agent definitions (Researcher, Skeptic, Data steward, Literature scout) and four skills for the procedures the code cannot enforce.
- Statistics toolkit in `trading.stats`: predictive regressions and mean tests with Newey-West errors, rank information coefficients, Fama-MacBeth slopes, a paired block bootstrap for differences between strategies, placebo tests (time shift, asset permutation), a pooled panel regression with errors from time blocks, Benjamini-Hochberg and Holm corrections, and minimum-detectable-effect calculations. Every tool is validated on synthetic data with a known answer.

### Changed

- The three course lessons and the bars-and-stats reference sheet are now Markdown pages of the course site, with formulas in LaTeX; the standalone HTML pages and their stylesheet are gone.

### Fixed

- `trading fetch` re-downloads a symbol in full after a new split, instead of appending post-split prices to pre-split history.
- Sanity checks report a large close move on a split day as history stored before the split, instead of treating the split as explaining it.
