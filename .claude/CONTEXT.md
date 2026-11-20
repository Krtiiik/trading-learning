# Context

<!--
Glossary for Claude: the terms and top-level concepts this project uses with a specific meaning.
- Define a term only if it means something particular here; skip ordinary words.
- One or two sentences each. Say what it is, not where it lives in the code.
- Keep the whole file short enough to read every session.
-->

## Language

**Learning site**: the static knowledge base in `learning/`, published as one private Claude artifact.
_Avoid_: wiki, docs site.

**Concept**: a short, standalone page explaining one idea in simple words.
_Avoid_: term, entry, article.

**Concept group**: one of the topic groups that every concept belongs to (Assets, Market mechanics, Charts, Indicators, Strategies, Risk and money).
_Avoid_: category, section.

**Planned concept**: a concept listed in the catalog with a title and summary but no body yet. It already has a working page and links.
_Avoid_: stub, draft.

**Lesson**: a longer guided page that connects several concepts and lists the ones it builds on. Written on request.
_Avoid_: guide, tutorial, article.

**Catalog**: `learning/catalog.yaml`, the single list of concept groups and concepts with their titles and summaries.

**Banner**: the hand-drawn SVG at the top of each written page that shows what the page is about.

**Shelf**: a single sideways-scrolling row of cards on the home page, one per concept group plus one for lessons.

## Relationships

- A **Concept group** has many **Concepts**. A **Concept** is either written or a **Planned concept**.
- A **Lesson** builds on several **Concepts**. Concepts and lessons link to concepts inline, and those links produce each page's backlinks.

## Ambiguities

<!-- Words used loosely or differently by different people, and which meaning wins. -->
