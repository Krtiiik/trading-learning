# Context

<!--
Glossary for Claude: the terms and top-level concepts this project uses with a specific meaning.
- Define a term only if it means something particular here; skip ordinary words.
- One or two sentences each. Say what it is, not where it lives in the code.
- Keep the whole file short enough to read every session.
-->

## Language

**Bar**: One period of trading for one symbol: raw open, high, low, close, volume, plus the provider's adjusted close and the dividends and splits that occurred on it.
_Avoid_: candle, tick, row.

**Granularity**: The length of a bar, written like `1d`. Only `1d` exists so far; intraday values (`1h`, `1m`) are planned.
_Avoid_: interval, timeframe, resolution.

**Raw price**: The price that actually traded on that day, never revised.
_Avoid_: unadjusted price, nominal price.

**Adjusted close**: The close scaled so its changes equal total return (dividends reinvested, splits removed). The provider rewrites its whole history whenever a new dividend or split occurs.
_Avoid_: adj price, total-return price.

**Adjustment factor**: Adjusted close divided by raw close for a bar; a change in it on an already stored bar signals the history was re-adjusted.

**Provider**: An external source of bars behind a common interface (Yahoo Finance today).
_Avoid_: feed, vendor, source.

**Store**: The local Parquet files holding bars, one file per symbol and granularity.
_Avoid_: cache, database.

**Universe**: The configured list of symbols `trading fetch` downloads by default.
_Avoid_: watchlist, tickers.

**Panel**: One bar field (usually adjusted close) for several symbols side by side, one column per symbol.

**Issue**: A sanity-check finding on stored bars (gap, duplicate, bad price, unexplained jump); reported as a warning, never blocks storing.

## Relationships

- A **Provider** delivers **Bars** at a **Granularity**; the **Store** keeps them per symbol.
- The **Universe** names which symbols to fetch; a **Panel** is built from the **Store**.
- **Issues** are computed from stored **Bars** after each fetch.

## Ambiguities

- "Price" alone is ambiguous: say **raw price** or **adjusted close**. Returns are computed on adjusted close; orders and fills use raw prices.
- "Splits" column: the split ratio on that bar, `0` meaning no split (Yahoo's convention), not `1`.
