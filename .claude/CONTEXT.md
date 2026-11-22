# Context

<!--
Glossary for Claude: the terms and top-level concepts this project uses with a specific meaning.
- Define a term only if it means something particular here; skip ordinary words.
- One or two sentences each. Say what it is, not where it lives in the code.
- Keep the whole file short enough to read every session.
-->

## Language

**Learning site**: the static knowledge base this repository holds, deployed to GitHub Pages.
_Avoid_: wiki, docs site.

**Reader**: a beginner anywhere, written with EU and especially Czech private traders in mind. Examples stay in US dollars; where a rule, product, tax or cost differs, the page gives the EU (and where useful the Czech) version next to the US one.

**Concept**: a short, standalone page explaining one idea in simple words.
_Avoid_: term, entry, article.

**Concept group**: one of the topic groups that every concept belongs to (Assets, Market mechanics, Charts, Indicators, Strategies, Risk and money).
_Avoid_: category, section.

**Planned concept**: a concept listed in the catalog with a title and summary but no body yet. It already has a working page and links.
_Avoid_: stub, draft.

**Lesson**: a longer guided page that connects several concepts and lists the ones it builds on. Written on request.
_Avoid_: guide, tutorial, article.

**Catalog**: `catalog.yaml`, the single list of concept groups and concepts with their titles and summaries.

**Banner**: the hand-drawn SVG at the top of each written page that shows what the page is about.

**Shelf**: a single sideways-scrolling row of cards on the home page, one per concept group plus one for lessons.

## Relationships

- A **Concept group** has many **Concepts**. A **Concept** is either written or a **Planned concept**.
- A **Lesson** builds on several **Concepts**. Concepts and lessons link to concepts inline, and those links produce each page's backlinks.

## Ambiguities

<!-- Words used loosely or differently by different people, and which meaning wins. -->

- **period / length** (learning site): a *period* is the time one bar or candle covers; an indicator's *length* is how many periods it looks back. Write "length" even though apps label that setting "period". A strategy's *look-back* is a span such as 12 months: write "look-back", not "period".
- **trade** (learning site): on market-mechanics pages, one transaction (a buyer and a seller agreeing on a price); on strategy and risk pages, a position from entry to exit. Say "position" or "round trip" where the difference matters.
- **position size** (learning site): the number of shares or units held. Its money value is the *position value*; do not call that the size.
- **slippage** (learning site): getting a worse fill price than expected or assumed. Use the word instead of paraphrases.
- **order book** (learning site): the list of waiting limit orders; its best prices are the bid and the ask.
- **high / peak** (learning site): an account's highest value so far is its *high*. A *peak* is a local turning point of a price (see peak-and-trough). Do not call the account high a peak.
- **bar** (learning site): one period's mark on a chart in general ("bar or candle"). A *bar chart* is the OHLC bar chart; *volume bars* are the bars under a chart. Say which one you mean. *Profile bars* are the horizontal bars of a volume profile, one per price level.
- **range / zone / band** (learning site): the *daily range* is a period's high minus its low. The sideways area between support and resistance is a *trading range*: write that on first use, never "range" alone, and "moves sideways between them" in passing. A *zone* is the narrow price area of one support or resistance level. *Band* means a Bollinger band only.
- **yield** (learning site): on bond pages, the yearly return if you buy now and hold to maturity. On stock pages, always write *dividend yield*. *High yield* means junk bonds only.
- **maintenance margin** (learning site): for US stocks, the FINRA minimum share of the position value; for futures, the exchange-set amount below which a margin call comes. Say which one you mean.
- **confirmation** (learning site): the later prices a rule waits for before it acts: candles after a peak, the next candle after a pattern, or a close beyond a zone. Say what confirms.
- **momentum** (learning site): on strategy pages, the strategy that ranks many assets by past return; on indicator pages, how strong one price's recent moves were (RSI, MACD). Write "momentum strategy" or "momentum indicator" where both could be meant.
- **drift** (learning site): a target mix changing by itself as prices move (rebalancing). Do not use it for the daily-reset decay of leveraged ETFs.
- **target / target mix** (learning site): a *target* is a planned sell price (risk-reward); a *target mix* is the planned share of each asset (rebalancing). Never write "target" alone for a mix.
- **CFD** (learning site): a contract with a broker that pays the change in a price, without holding the asset. Common in the EU and UK; not offered to private traders in the US. The cfd page owns the term; broker keeps the one-line gloss.
- **market maker / large trading firm** (learning site): write "large trading firm" in passing; write "market maker" only where the page explains it.
- **stop loss** (learning site): two words, no hyphen, as in the catalog title.
- **private traders** (learning site): the name for retail investors; use it instead of "retail" or "private clients", except when quoting a regulator's rule.
- **mid price, round trip** (learning site): the names for the point halfway between bid and ask, and for buying then selling again. Use them instead of paraphrases.
- **Czechia** (learning site): the country name; use "Czech" only as an adjective (Czech tax, Czech resident).
