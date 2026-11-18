# Context

<!--
Glossary for Claude: the terms and top-level concepts this project uses with a specific meaning.
- Define a term only if it means something particular here; skip ordinary words.
- One or two sentences each. Say what it is, not where it lives in the code.
- Keep the whole file short enough to read every session.
-->

## Language

**Bar**: One period of trading for one symbol: raw open, high, low, close, volume, plus the provider's adjusted close and the dividends and splits that occurred on it. Crypto bars add quote volume (in USDT), trade count and taker-buy volumes; their volume is in coins and fractional.
_Avoid_: candle, tick, row.

**Bar label**: The timestamp that names a bar: the moment it opens. A daily crypto bar is labelled with its UTC date and covers 00:00 to 24:00 UTC; an hourly bar with the UTC instant it opens. A crypto bar's contents are knowable at its close, which is its label plus its granularity. An ETF daily bar is labelled with its session date and is knowable at that session's close (before the same date's crypto bar closes).

**Granularity**: The length of a bar: `1d` or `1h` (hourly bars exist for crypto only).
_Avoid_: interval, timeframe, resolution.

**Raw price**: The traded price adjusted for splits only, never for dividends. Equal to what actually traded since the last split; earlier bars are divided by each later split ratio, so a split rewrites raw history too (that is how Yahoo serves it).
_Avoid_: unadjusted price, nominal price.

**Adjusted close**: The close scaled so its changes equal total return (dividends reinvested, splits removed). The provider rewrites its whole history whenever a new dividend or split occurs.
_Avoid_: adj price, total-return price.

**Adjustment factor**: Adjusted close divided by raw close for a bar; a change in it on an already stored bar signals a new dividend re-adjusted the history. Splits leave it unchanged, since they scale raw and adjusted prices alike.

**Provider**: An external source of bars behind a common interface: Yahoo Finance for US ETFs, the Binance public archive for crypto.
_Avoid_: feed, vendor, source.

**Store**: The local Parquet files holding bars and series, one file per symbol, grouped into datasets.
_Avoid_: cache, database.

**Dataset**: One directory of the Store with one kind of data from one provider, named by its path: `binance/spot/1d`, `binance/funding`, or `1d` for the ETF bars.

**Manifest**: The file that gives a dataset its identity: a content hash per file and an id over all of them. A run record names the ids of the datasets it used.

**Series**: A per-symbol time series that is not a bar: funding rate, basis (premium index) or open interest of a perpetual contract. Used as predictors only; stored under the spot symbol they describe.

**Universe**: The configured list of ETF symbols `trading fetch` downloads by default.
_Avoid_: watchlist, tickers.

**Point-in-time universe**: The crypto coins research may trade at a given moment: at each monthly reconstitution, the 40 USDT spot pairs with the highest quote volume over the previous 30 days, decided only from bars that closed before that date. Stablecoins, wrapped or pegged tokens, tokenised stocks and leveraged tokens are never members; coins delisted later stay in the history.
_Avoid_: the universe (for crypto), top 40.

**Reconstitution**: The monthly re-ranking that sets the point-in-time universe. The one dated the 1st applies to bars labelled that day or later.

**Liquidity tier**: A coin's slippage class at a reconstitution: tier 1 is BTC and ETH, tier 2 the next ten members by volume, tier 3 everything else.

**Redenomination**: A token swap that keeps the symbol but changes the unit (1 old coin becomes 1000 new). Stored like a split: earlier prices are divided by the ratio and the ratio sits in `splits`.

**Symbol reuse**: Binance giving a delisted coin's symbol to a different coin (`LUNAUSDT`). The Store keeps the earlier coin under a dated name (`LUNAUSDT-2022`).

**Panel**: One bar field (usually adjusted close) for several symbols side by side, one column per symbol.

**Issue**: A sanity-check finding on stored bars (gap, duplicate, bad price, unexplained jump); reported as a warning, never blocks storing.

### Research (`research/`, `trading.research`)

**Hypothesis**: One falsifiable claim about the crypto market, with a predicted direction and rough size, a single primary test and a decision rule, all written down before anything is run. One file each in `research/hypotheses/`. A variant is a new hypothesis.
_Avoid_: idea, strategy (a strategy is what a trading claim tests).

**Registration**: Committing a hypothesis file before its first run. Git history proves the order; the fields that define the hypothesis are frozen from that commit on.

**Family**: The approach a hypothesis belongs to: `time-series`, `cross-sectional`, `derivatives` or `cross-market`. Families get equal effort.

**Origin**: Where a hypothesis came from: `literature` (published evidence) or `exploration` (looking at train data). It decides which data may test it.

**Claim**: What kind of statement a hypothesis makes: `predictive` (a signal ranks or forecasts returns) or `trading` (a long-or-flat rule beats a benchmark after costs). Also, loosely, a finding that has climbed the claim ladder.

**Primary test**: The one statistical test that decides a hypothesis, giving an estimate and a one-sided p-value in the predicted direction.

**Experiment**: The code that carries out a hypothesis's primary test: a module with a `panel` function (target weights or a predictor) and a `test` function.

**Run**: One execution of an experiment on one segment, by the harness. Its **run record** (hypothesis, parameters, dataset ids, commit, segment, estimate, p-value, seed, duration) is written by the harness, never by hand.

**Harness**: The only way a hypothesis is tested. It refuses unregistered or altered hypotheses and uncommitted code, checks the experiment for look-ahead, and writes the run record.

**Split**: The fixed division of time into three **segments**: train (up to 2022), dev (2023-2024), test (2025 on). Earlier data may be lookback history for a later segment; nothing is fitted, tuned or chosen on a later one.
_Avoid_: in-sample/out-of-sample, validation set, holdout.

**Seal**: The lock on the test segment. Research cannot load test-period data until the seal is opened, once and on record, for at most five finalists.

**Claim ladder**: The statuses a hypothesis moves through: registered, then rejected or candidate (train), then not replicated or supported (dev), then refuted or confirmed (Skeptic review). Computed from the records, never set by hand.

**Candidate**: A literature hypothesis whose train p-value passes Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.

**Supported**: A candidate whose dev estimate has the predicted sign and at least the pre-declared size. For an exploration hypothesis: its dev p-value passes false-discovery control across all exploration hypotheses.

**Skeptic review**: An independent attempt to break a supported finding, starting from the hypothesis file and run records. It ends in confirmed or refuted, written into the hypothesis file. A review of a hypothesis with any other status is an audit: it ends in `audited` and changes no status.

**Finalist**: A confirmed hypothesis chosen, before the seal opens, for the single test run.

**Catalogue**: The generated index of every hypothesis and its status, negatives included (`research/CATALOGUE.md`).

**Know-how**: A note stating one lesson, pitfall or how-to, where it came from and how far to trust it (`research/knowhow/`). How agents and the owner share what was learned.

**Benchmark**: What a trading claim is compared with, run through the same engine and costs: buy-and-hold BTC, the equal-weight point-in-time universe, or cash.

**Double cost**: The same test with every trading cost doubled; reported for every trading claim.

**Minimum detectable effect**: The smallest true effect a test on a given segment would find with 80% power. Computed before a hypothesis is run, to judge whether it is testable at all.

### Course (`learn/`)

**Lesson**: One numbered page of the course that teaches a single objective and ends with Practice questions. Numbers run across the whole course.

**Part**: A named group of lessons in teaching order; a part with no lessons yet is shown as planned.
_Avoid_: module, chapter, unit.

**Reference sheet**: A dense one-page summary of taught material, for looking things up rather than learning them.
_Avoid_: cheat sheet.

**Course brief**: The mission and glossary sent to Claude with every Ask Claude request, so answers use the course's terms.

**Thread**: The saved Ask Claude conversation of one page, including "New topic" breaks; there is one per page.
_Avoid_: chat log, history.

## Relationships

- A **Provider** delivers **Bars** at a **Granularity**; the **Store** keeps them per symbol, in **Datasets** that each carry a **Manifest**.
- The **Universe** names which ETF symbols to fetch; a **Panel** is built from the **Store**.
- The **Point-in-time universe** is ranked from the daily crypto bars at each **Reconstitution**, which also sets every coin's **Liquidity tier**.
- **Issues** are computed from stored **Bars** after each fetch.
- A **Hypothesis** has one **Primary test**, carried out by its **Experiment**; each **Run** of it on a **Segment** leaves a **Run record**.
- The **Claim ladder** status of every hypothesis follows from its file and its run records; the **Catalogue** lists them.
- The **Seal** guards the test **Segment** of the **Split**; only **Finalists** ever run on it.

## Ambiguities

- "Price" alone is ambiguous: say **raw price** or **adjusted close**. Returns are computed on adjusted close; orders and fills use raw prices.
- "Splits" column: the split ratio on that bar, `0` meaning no split (Yahoo's convention), not `1`.
- "Universe" alone means the ETF list. For crypto always say **point-in-time universe**.
- "Test" has two meanings: the test segment of the split, and a statistical test. Say **test segment** or **primary test**.
- "Rejected" (failed on train), "not replicated" (failed on dev) and "refuted" (broken by the Skeptic) are different statuses; do not use one for another.
- A p-value in a run record is one-sided in the predicted direction; a result in the wrong direction has p above 0.5.
- "Volume" is in shares or coins; rank and size crypto by **quote volume**, which is in USDT.
