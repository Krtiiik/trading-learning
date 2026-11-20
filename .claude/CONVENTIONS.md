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
- Adding a concept starts in `catalog.yaml` (slug, title, summary). Writing it means adding `content/concepts/<group>/<slug>.md` (body only, no frontmatter) and `banners/<slug>.svg`.
- Lessons need frontmatter `title`, `summary`, `added` (date) and `builds_on` (concept slugs).
- Banners: `viewBox="0 0 1200 400"`, colours only through `--banner-bg/fg/up/down/accent` with fallbacks, no `id` attributes. Each one should show at a glance what the page explains.

## Where things go

- Everything for the learning site stays inside `learning/`; its tests go in `tests/learning/`.

## Testing

<!-- What gets tested and how; test layout and naming. -->
