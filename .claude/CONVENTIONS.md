# Conventions

<!--
Idioms and placement rules that a linter or formatter can't enforce.
Skip anything tooling already checks. Prefer a rule plus a one-line reason over a long explanation.
-->

## Code

<!-- Error handling, naming, patterns to follow and patterns to avoid. -->

## Learning site writing

- A concept must make sense on its own to a beginner: plain words, short paragraphs, one concrete example with numbers. Explain any term you need in passing instead of requiring the reader to click away. Links are for going deeper.
- Link each concept the first time it is mentioned with `[[slug]]`. Use `[[slug|text]]` when the wording differs (plural, inflection, a proper noun that the default lowercasing would break). Default link text is the title with its first letter lowercased, except acronyms.
- Advanced concepts and lessons may lean on basics, and should link them rather than re-explain them.
- One page owns each definition (ohlc owns open/high/low/close, spread owns the spread cost, moving-average owns length). Other pages give a one-line version in passing and link the owner, so the wording can't drift.
- Don't state market conventions as universal: candle colours are reversed in parts of East Asia, so say "usually" when a colour means up or down.
- End a concept with a "Watch out" section and a linked "Next, see …" line.
- A concept body is usually 300–500 words (each link counted as its display text, tables left out, since they hold numbers the prose already walks through). 500 is a ceiling, to keep pages short; 300 is only a guide. A shorter page that explains its concept fully is fine, so never pad one to reach the count. Count with `uv run python learning/build.py --words <slug>`; that count is the one that decides.
- Acronym titles need no link text: write `[[atr]]`, not `[[atr|ATR]]`.
- Catalog titles and summaries that contain a comma must be quoted; the build rejects them otherwise.
- Adding a concept starts in `catalog.yaml` (slug, title, summary). Writing it means adding `content/concepts/<group>/<slug>.md` (body only, no frontmatter) and `banners/<slug>.svg`.
- Lessons need frontmatter `title`, `summary`, `added` (date) and `builds_on` (concept slugs).
- Banners: `viewBox="0 0 1200 400"`, colours only through `--banner-bg/fg/up/down/accent` with fallbacks, no `id` attributes. Each one should show at a glance what the page explains.

## Where things go

- Everything for the learning site stays inside `learning/`; its tests go in `tests/learning/`.

## Testing

<!-- What gets tested and how; test layout and naming. -->
