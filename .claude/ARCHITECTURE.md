# Architecture

<!--
The big picture and the reasons behind it, for Claude.
Don't list files, classes or signatures: the source shows those.
Write what a newcomer couldn't work out by reading the code: how the parts fit together,
why a design was chosen over the obvious alternative, and the constraints that shaped it.
-->

## Overview

A personal research workbench for learning algorithmic trading. It covers market data for two markets (daily bars for a universe of US ETFs from Yahoo; daily and hourly crypto bars plus perpetual-futures series from the Binance public archive), kept locally and sanity-checked, and a research process for crypto built on top of it. A course site in `learn/` teaches with it (see the last section).

## Components and flow

`trading fetch` → for each symbol in the universe, the update step asks a provider for bars (everything, or only since the last stored bar) → normalizes them into the common bar shape → writes them to the store → runs the sanity checks and prints issues as warnings.

Research code never talks to a provider: it reads the store through `load_bars` / `load_panel`, so notebooks work offline and see the same data every time.

## Design notes

**Provider behind a protocol.** yfinance is an unofficial scraper that can break or be rate-limited; keeping it behind a small interface lets Stooq, Alpaca or a paid source replace it without touching storage or research code. Providers normalize to one bar shape so nothing downstream knows where data came from.

**Raw prices plus adjusted close, not fully adjusted OHLC.** Raw prices (split-adjusted only, as Yahoo serves them) equal what traded since the last split and are never touched by dividends; the adjusted close gives total returns. Fully adjusted OHLC can be derived when needed. Storing only adjusted data would lose the traded prices.

**Incremental updates re-fetch the last stored bar.** A bar stored while its session was open gets replaced by final values. Comparing that bar's adjustment factor with the provider's tells whether a new dividend re-adjusted history. A split does not change the factor (it scales raw and adjusted prices alike), so a split not yet stored is checked separately. Either way the symbol is downloaded in full, since the stored prices are stale; appending would mix pre- and post-split prices.

**Parquet per symbol, data not in git.** Typed, compressed, fast with pandas, trivially inspectable per symbol, and appending one symbol never rewrites others. Data is reproducible from `trading fetch` and redistributing Yahoo data would break its terms, so `data/` is gitignored.

**Sanity checks warn, never block.** Free data regularly has gaps and real extreme moves (e.g. silver on 2026-01-30); refusing to store it would leave no data. Issues are surfaced so research can decide.

**Daily index is tz-naive dates, hourly index is tz-aware UTC.** A daily bar belongs to a date, not an instant: the session date for an ETF, the UTC day for a coin. That keeps ETF and crypto daily panels joinable by date. Hourly bars are instants and carry their time zone.

## Crypto data

`trading rebuild` → list every USDT spot pair in the Binance archive → daily bars for all of them → the point-in-time universe is ranked from those → hourly bars, funding and basis only for pairs that were ever members → a manifest per dataset.

**The archive, not the API.** Bulk monthly files need no key, keep delisted pairs, and every file can be verified, so a rebuild months later gives the same Store. The price is freshness: the Store ends with the last complete month.

**Daily bars for every pair, the rest for members only.** Ranking needs the volume of all ~780 pairs, which is 50 MB as daily bars. Hourly bars for all of them would be several times the download and never used, since research trades only universe members.

**Downloads are verified and cached.** Each file is checked against the checksum in the bucket listing and kept under `data/raw/`, so a rebuild after a code change re-parses without re-downloading, and "from nothing" still works by deleting `data/`.

**A dataset's identity is a hash of its content, not of its files.** Parquet bytes change with library versions; the values do not. The manifest hashes values, index and column types, so the same data rebuilt later has the same id, and a run record that names the id names the data.

**Archive quirks stay in the provider.** Timestamps that switch from milliseconds to microseconds, files with and without headers, symbols reused for another coin, token swaps that change the unit, perpetual contracts quoted per 1000 coins: all handled in the Binance provider, so everything after it sees normalized bars. The curated tables there (symbol reuse, redenominations) came from looking at gaps and jumps in the data and are the first place to look when a new oddity appears.

**The universe excludes by a curated list, with a volatility net under it.** Names alone cannot tell a coin from a leveraged token or a tokenised stock (JUP is a coin, BTCUP is not), so the exclusions are listed by hand. A stablecoin nobody has listed yet is still caught, because a pair whose price barely moved for 30 days is treated as pegged.

## Research process

Hypothesis file committed (registration) → `trading research run` → the harness checks the registration and the code, loads market data that ends with the segment, checks the experiment's panel for look-ahead, runs the primary test, writes the run record → `trading research catalogue` recomputes every status from the records and regenerates the catalogue.

Three packages do the work: `trading.backtest` (engine, costs, metrics), `trading.stats` (the validated tests), `trading.research` (split and seal, market panels, registry, harness, ladder, catalogue). The records themselves live in `research/` and are plain files in git.

**The process is enforced in code, not asked of agents.** Many agents work here and none of them can be relied on to remember a rule. So the harness refuses what must not happen (an unregistered hypothesis, a changed prediction, uncommitted code, a dev run for a non-candidate, a second dev run, any test run before the seal opens) and does itself what must not be forgotten (the run record, the look-ahead check). Skills cover only what code cannot check.

**Registration is proven by git history.** The harness reads the first committed version of a hypothesis file and compares its frozen fields with the current file. There is no "registered" flag to set, and so none to set falsely.

**Statuses are derived, never stored as truth.** Whether a hypothesis is a candidate depends on the p-values of all the others, so a status written by hand would go stale as soon as another hypothesis is registered. The ladder is recomputed from the records each time; the `status` line in a hypothesis file is a copy for readers.

**Experiments get their data handed to them.** An experiment receives a `ResearchData` that stops at the end of its segment and never imports the Store (the harness refuses modules that do). That is what makes the seal hold: later data is not filtered out by the experiment's good behaviour, it is not there. The same object notes every dataset it loaded, which is how the run record knows.

**A market panel has no column for a coin that is not yet a member.** A column for a coin that joins the universe next year would reveal that it will matter. Panels for a segment carry only coins that had been members by its end.

**The look-ahead check is mechanical.** The harness recomputes an experiment's panel three times with later bars removed and requires the earlier rows to be identical. It is cheap because the engine is fast, and it has already caught a helper that decided "this is the week's last bar" from the bar after it.

**The engine is vectorised with hold rows.** A panel of target weights against open prices, as array operations: about 0.15 s for 40 coins of hourly bars over five years and 3 ms for daily bars (measured 2026-11-18, see `research/knowhow/`), so nobody is tempted to skip a check. A row of NaN means "do not trade", which lets a strategy rebalance weekly on daily bars and lets holdings drift between rebalances, still without a loop over bars. A plain loop in the tests proves the two agree.

**Two false-discovery controls, by origin.** A hypothesis found by looking at train data would pass a train test by construction, so exploration hypotheses skip train and are judged on dev, with Benjamini-Hochberg across their dev p-values; literature hypotheses are controlled across their train p-values. A hypothesis without a run counts as p = 1 in its control, so registering many and testing few does not help.

## Course site (`learn/`)

The course that teaches with this workbench is a Jekyll site in `learn/`: Markdown lessons and reference sheets with Liquid includes for quizzes and asides, built locally and published as one private multi-file Claude artifact (republished after every change). There is no GitHub Pages and no server.

**Why the artifact, and why it shapes the code.** Publishing as an artifact gives the reader an in-page Ask Claude chat (the artifact's `sample` capability) and somewhere to keep those chats (its `db`), which later teaching sessions read with ArtifactData to see what the learner asked. Everything follows from where the pages must work: under `jekyll serve`, as plain files, and inside the artifact. Hence relative `.html` links only, KaTeX rendering to MathML (the artifact's content policy allows CDN scripts but not CDN stylesheets or fonts), and Ask Claude lighting up only when the runtime grants it, so the same build shows no trace of it locally.

**Chats are owner-only.** The published db rules restrict every path to the artifact's owner, so a shared link never exposes the learner's questions, while ArtifactData (acting as the owner) can still read them. The private `data/users/<id>/` area was avoided because nobody but that viewer can read it, which would hide the chats from the teaching session too.

**Content has one writer.** Teaching sessions decide what to teach and delegate the writing to the `lesson-writer` agent, which owns the Markdown format, includes and math conventions, so lessons stay uniform as the course grows. The visual design is specified separately in `learn/DESIGN.md`.

**Facts are read, not copied.** The course brief sent with each chat (mission and glossary) and the dashboard's ETF count are read at build time from `MISSION.md`, `.claude/CONTEXT.md` and `universe.toml`, so the site cannot drift from them.
