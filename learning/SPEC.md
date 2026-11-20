# Learning site: structure spec for the design

This is the contract between the site's structure (build script, catalog, content, banners) and its design (templates and styles). The design can change any markup and styling as long as it keeps the data, URLs and hooks below working.

## Ownership

| Part | Owner | Files |
|---|---|---|
| Structure | build and content work | `build.py`, `catalog.yaml`, `content/`, `banners/`, `artifact-url.txt` |
| Design | design work | `templates/*.html`, `static/site.css`, any new files in `static/` (fonts, icons) |
| Behaviour | shared | `static/site.js`: the design may restyle or extend it, but keeps the hooks in [Behaviour hooks](#behaviour-hooks) |

The current templates and `site.css` are bare placeholders. They show every piece of data in use, so replace them freely.

## What the site is

A knowledge base for learning trading, built up one page at a time.

- **Concepts**: short, standalone explanations of one idea each ("Candle", "Stop loss"). Each concept belongs to one **concept group**.
- **Concept groups**, in order: Assets, Market mechanics, Charts, Indicators, Strategies, Risk and money.
- **Lessons**: longer guided pages that connect several concepts. Each one lists the concepts it builds on.
- **Planned concepts**: concepts in the catalog that are not written yet (most of them, at first). They have a title, a one-line summary and a shared "coming soon" banner. Links to them work. They should look clearly secondary but still be reachable: the catalog doubles as the roadmap.

Expect high tens of pages, growing over time. Most pages start planned.

## Pages and URLs

All URLs are relative. Every template gets `root` (`""` on the home page, `"../"` one level down) and must prefix every internal link and asset with it. The site is published as a multi-file artifact and also served from `learning/dist/` locally.

| Page | URL | Template | Purpose |
|---|---|---|---|
| Home | `index.html` | `home.html` | Intro, then one **shelf** per concept group, then a Lessons shelf |
| Group | `groups/<group>.html` | `group.html` | Full grid of cards for every concept in the group |
| Lessons | `lessons/index.html` | `lessons.html` | Full grid of lesson cards, newest first |
| Concept | `concepts/<slug>.html` | `concept.html` | One concept, written or planned |
| Lesson | `lessons/<slug>.html` | `lesson.html` | One lesson |

### Home layout (decided)

- A short intro at the top.
- One section per concept group: the group title as a heading, which links to the group page, plus blurb and progress ("1 of 10 written"). Under it is **a single row of cards** that scrolls sideways, with left/right arrow buttons. It never wraps to a second row.
- Then a **Lessons** section in the same style: the heading links to `lessons/index.html`, with one row of lesson cards.
- Group and lessons pages show the same cards in a **full grid**.

### Card

Used in shelves and grids, for concepts and lessons alike: banner (scaled down), group name (concepts only), title, one-line summary. Planned concepts also show "Not written yet". Order: written concepts first, then planned ones, each in catalog order. Lessons are ordered newest first.

### Concept page

Banner (full width at the top, the main visual identity of the page) → group label linking to the group page → title → one-line summary (lead) → body → **Related** (concepts this page links to) → **Used in** (pages that link here). A planned concept has no body, only a "planned but not written yet" note. Its Related list is empty, but it may already have Used in entries.

### Lesson page

Banner → "Lesson" label → title → summary → **Before you start** (prerequisite concepts) → body → **Concepts used**.

### Body content

The body is Markdown rendered to HTML: `h2`/`h3`, paragraphs, `ul`/`ol`, `table`, `strong`/`em`, `code`/`pre`, and inline concept links. Style it under `.prose`. Concept bodies are short (300–500 words) and meant for beginners, so they should read comfortably.

## Template data

Templates are Jinja2 (`StrictUndefined`, autoescape on). Every template receives:

| Name | What |
|---|---|
| `site.groups` | list of groups: `slug`, `title`, `blurb`, `url`, `concepts` (list of pages), `written_count` |
| `site.lessons` | list of lesson pages, newest first |
| `site.pages` | dict slug → page, every concept and lesson |
| `root` | relative prefix to the site root |
| `current` | this page's URL relative to the root |
| `title` | page title text for `<title>` |
| `cards(pages)` | orders pages for display: written first, then planned |

A **page** has `kind` (`concept`/`lesson`), `slug`, `title`, `summary`, `url`, `written`, `status` (`written`/`planned`), `banner_svg` (inline SVG markup, output with `| safe`), `group` (concepts only), `added` (lessons only), `builds_on` (slugs), `links` (slugs linked from the body), `backlinks` (slugs linking here).

Page templates also receive: `group.html` → `group`; `concept.html` and `lesson.html` → `page` and `body` (rendered HTML, output with `| safe`).

## Banners

- Every written page has its own hand-drawn SVG, inlined into the page. Planned pages share `banners/_planned.svg`.
- Canvas: `viewBox="0 0 1200 400"` (3:1). Display it full width at that ratio on article pages. Cards show the same SVG scaled down, so keep the 3:1 frame or crop deliberately with CSS.
- Colours come from CSS custom properties, which the design defines for light and dark themes:

  | Variable | Use |
  |---|---|
  | `--banner-bg` | banner background |
  | `--banner-fg` | lines, text, neutral shapes |
  | `--banner-up` | rising / positive / buy (green family) |
  | `--banner-down` | falling / negative / sell (red family) |
  | `--banner-accent` | highlight (the thing the page is about) |

  The SVGs use them as `style="fill: var(--banner-bg, #f2f4f7)"`, with light fallbacks. Banner text is uppercase `system-ui` and bold. If the design wants a different banner font or stroke style, say so, and future banners will follow it. Existing ones can be redrawn.
- No `id` attributes inside banners: many are inlined on one page.

## Behaviour hooks

`static/site.js` relies on these. Keep the classes and attributes, or update the script along with the markup.

| Feature | Hook |
|---|---|
| Data | `static/index.js` (generated) sets `window.LEARNING_INDEX = {groups, pages}`. Each page entry has `slug, kind, title, summary, url, status, group?`. Load it before `site.js`. |
| Root | `<html data-root="{{ root }}">` |
| Concept links | `a.concept-link[data-slug]` with `is-written`/`is-planned`. These appear in bodies, Related, Used in and Before you start. Body links come from the build, so their class names are fixed. |
| Hover preview | a single `.link-preview` element (hidden) that the script fills with `.link-preview__group`, `__title`, `__summary`, `__status` and positions under the hovered link |
| Search | `.search` holding `input.search__input` and `ol.search__results`. Results are `li.search__result.is-<status>` > `a.search__link` > `.search__title` + `.search__meta`, or `li.search__empty`. |
| Shelf | `.shelf` holding `.shelf__row` (the scrolling row) and `.shelf__arrow--prev` / `.shelf__arrow--next` buttons |
| Status | `.is-written` / `.is-planned` on cards, links and the article |
| Page kind | `body.page-home|group|lessons|concept|lesson` |

## Constraints

- The site is published as a private Claude artifact. Everything must be local files in `static/`. External stylesheets may come only from Google Fonts. Scripts may only come from cdnjs, jsdelivr or unpkg, pinned to exact versions. Prefer none.
- It must work at phone width (16px side gutter, no horizontal page scroll; shelf rows scroll inside themselves) and in light and dark mode (`prefers-color-scheme`).
- Keep pages readable without JavaScript, except search and previews.

## Build and preview

```
uv run python learning/build.py          # builds learning/dist/
uv run pytest tests/learning             # structure tests; they also build the real site
```

Preview locally with the `learning-site` entry in `.claude/launch.json`. It runs `learning/serve.py`, which serves `learning/dist` on `$PORT` (default 8765); add `--open` to also open it in the default browser. Don't publish the artifact from a branch: it is republished from `main` after merge.
