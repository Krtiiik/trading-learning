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

## Ambiguities

- "Price" alone is ambiguous: say **raw price** or **adjusted close**. Returns are computed on adjusted close; orders and fills use raw prices.
- "Splits" column: the split ratio on that bar, `0` meaning no split (Yahoo's convention), not `1`.
- "Universe" alone means the ETF list. For crypto always say **point-in-time universe**.
- "Volume" is in shares or coins; rank and size crypto by **quote volume**, which is in USDT.
