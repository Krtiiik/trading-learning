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

- **period / length** (learning site): a *period* is the time one bar or candle covers; an indicator's *length* is how many periods it looks back. Write "length" even though apps label that setting "period".
- **trade** (learning site): on market-mechanics pages, one transaction (a buyer and a seller agreeing on a price); on strategy and risk pages, a position from entry to exit. Say "position" or "round trip" where the difference matters.
- **mid price, round trip** (learning site): the names for the point halfway between bid and ask, and for buying then selling again. Use them instead of paraphrases.
