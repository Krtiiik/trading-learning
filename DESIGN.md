# Design guideline: Hairline

A portable design language, taken from the trading learning site (`learning/static/site.css`). Use it for documentation sites, knowledge bases, dashboards and tools. Copy this file into a new project and start from the [starter tokens](#14-starter-tokens).

The reference implementation is `learning/static/site.css`. When this file and that stylesheet disagree on the learning site, the stylesheet is correct and this file must be updated.

---

## 1. The idea in one paragraph

The page is **one framed column**. Full-height vertical rules mark its left and right edges. Every section is a **row** that a 1px line separates from the next. Cards and list items **tile edge to edge and share their borders**, like cells in a table. There are **no rounded corners and no shadows**. The neutrals are almost colourless. **One highlight colour** is kept for the few things that matter most. Labels and numbers use a **monospace, uppercase, tracked** style. Headings are a **tight, heavy sans**. The effect is an engineering drawing or a printed spec sheet: calm, exact, dense but not crowded.

## 2. Principles

1. **Lines, not boxes.** Structure comes from 1px rules. Do not use cards that float on a background, drop shadows or gradients for depth.
2. **Shared borders.** Two neighbours never show two lines. Tiles share one line (use negative margins, `gap: 1px` on a line-coloured background, or `box-shadow: 1px 0 0, 0 1px 0`).
3. **Zero radius.** Set `border-radius: 0` on everything, including buttons, inputs and focus rings.
4. **Colour is a signal, not decoration.** Neutrals carry the layout. The highlight appears only on: the most important links, keyboard focus, and the accent in illustrations. If everything is highlighted, nothing is.
5. **Two voices of type.** A sans for reading and headings. A mono for labels, counts, numbers, arrows and status. Never mix their roles.
6. **State through weight and tone, not new colours.** "Secondary" or "not ready" means: muted text, lighter weight, greyscale image, dashed or dotted line.
7. **Quiet motion.** Only background and colour change on hover, in 120 ms, and only when the user allows motion.
8. **Works everywhere.** Phone width, light and dark themes, keyboard, and without JavaScript for the core content.

## 3. Colour

All colours are in OKLCH. The neutrals use hue 250 (a cool grey) with chroma under 0.01, so they look nearly neutral.

### 3.1 Neutral tokens

| Token | Role | Light | Dark |
|---|---|---|---|
| `--bg` | page and frame background | `oklch(0.978 0.002 250)` | `oklch(0.165 0.004 250)` |
| `--panel` | hover fill, raised surface, table head | `oklch(0.995 0.001 250)` | `oklch(0.195 0.005 250)` |
| `--sunk` | code, inset areas, illustration ground | `oklch(0.955 0.003 250)` | `oklch(0.145 0.004 250)` |
| `--fg` | body text, strong lines, filled states | `oklch(0.22 0.006 250)` | `oklch(0.93 0.003 250)` |
| `--muted` | secondary text, labels, summaries | `oklch(0.50 0.008 250)` | `oklch(0.68 0.006 250)` |
| `--faint` | placeholders, arrows at rest, tertiary status | `oklch(0.62 0.006 250)` | `oklch(0.55 0.006 250)` |
| `--line` | all structural rules (1px) | `oklch(0.88 0.004 250)` | `oklch(0.29 0.006 250)` |
| `--line-2` | stronger rules: controls, popovers, markers | `oklch(0.68 0.006 250)` | `oklch(0.46 0.008 250)` |

Rules:

- `--panel` is *lighter* than `--bg` in light mode and slightly lighter in dark mode. A hover lifts the surface; it does not darken it.
- Use `--line` for layout. Use `--line-2` only for interactive edges (buttons, search results popover, empty meter squares) and for list markers.
- Body text is `--fg`. Supporting text is `--muted`. Use `--faint` only for things the eye may skip.

### 3.2 Highlight

| Token | Light | Dark |
|---|---|---|
| `--hi` | `oklch(0.53 0.18 262)` (blue) | `oklch(0.74 0.15 262)` |

Use `--hi` for:

- The underline of the most important in-text links (2px, see [Links](#9-links)).
- The focus outline.
- The accent in illustrations.

Do not use `--hi` for buttons, backgrounds, headings, icons or borders. To change the brand colour in a new project, change only the hue (262) and keep the lightness and chroma. That keeps the contrast.

### 3.3 Semantic colours for illustrations

Illustrations and data use a separate, small set. In the learning site they are named `--banner-*`; in a new project, name them for their use (`--figure-*`, `--chart-*`).

| Token | Meaning | Light | Dark |
|---|---|---|---|
| `--figure-bg` | ground | `oklch(0.955 0.003 250)` | `oklch(0.205 0.005 250)` |
| `--figure-fg` | lines, text, neutral shapes | `oklch(0.22 0.006 250)` | `oklch(0.92 0.003 250)` |
| `--figure-up` | positive, rising, success | `oklch(0.56 0.13 150)` | `oklch(0.74 0.14 150)` |
| `--figure-down` | negative, falling, error | `oklch(0.56 0.17 27)` | `oklch(0.70 0.16 27)` |
| `--figure-accent` | the subject of the picture | same as `--hi` | same as `--hi` |

Keep green and red inside figures and data. The UI chrome stays neutral.

### 3.4 Themes

- Light is the default. Dark follows `prefers-color-scheme`.
- A `data-theme="light"` or `data-theme="dark"` attribute on `<html>` overrides the system. Define dark twice: under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }` and under `:root[data-theme="dark"]`.
- Set `color-scheme: light` / `dark` with each theme, so form controls and scrollbars follow.
- In dark mode, the highlight and semantic colours get *lighter and a little less saturated*. Do not reuse the light values.

## 4. Typography

### 4.1 Families

```css
--sans: "Geist", "Segoe UI", system-ui, -apple-system, sans-serif;
--mono: "JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
```

Load from Google Fonts: Geist 400/500/600, JetBrains Mono 400/500, with `display=swap`. Do not use weight 700 in the UI; 600 is the heaviest.

### 4.2 Scale

| Role | Size | Line height | Weight | Tracking | Notes |
|---|---|---|---|---|---|
| Hero title | `clamp(36px, 5.4vw, 60px)` | 1.02 | 600 | -0.035em | `text-wrap: balance` |
| Page title | `clamp(32px, 5vw, 52px)` | 1.04 | 600 | -0.035em | `text-wrap: balance` |
| Listing title | `clamp(32px, 4.6vw, 48px)` | 1.05 | 600 | -0.03em | |
| Section title | 24px | 1.2 | 600 | -0.025em | |
| Prose h2 | 23px | 1.25 | 600 | -0.02em | |
| Lead / summary | 19px (article), 17px (headers) | 1.5 | 400 | 0 | `--muted`, `text-wrap: pretty` |
| Prose body | 17px (16px on phones) | 1.7 | 400 | 0 | |
| Prose h3 | 18px | 1.3 | 600 | 0 | |
| UI body | 16px | 1.55 | 400 | 0 | page default |
| Card title | 16px | 1.3 | 600 | -0.01em | clamp to 2 lines |
| Nav, search, small UI | 14px | inherit | 400 | 0 | |
| Card summary | 14px | 1.45 | 400 | 0 | `--muted`, clamp to 2 lines |
| **Label** | 11px mono | 1.4 | 500 | 0.08em | uppercase, `--muted` |
| Stat number | 22px mono | 1.1 | 500 | -0.02em | `tabular-nums` |

The rule of thumb: **the bigger the text, the tighter the tracking and line height.** Headings are tight and negative-tracked; labels are tiny and wide-tracked.

### 4.3 The label style

One style covers every small piece of metadata: kickers, group names, counts, status, table heads, section headings of link lists, the footer.

```css
.label { font: 500 11px/1.4 var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
```

Use it often. It is the main tool to make a dense page readable without extra colour.

### 4.4 Glyphs as icons

Use mono text arrows, not icon fonts: `→` for "go to", `←` for "back", `←` / `→` in scroll buttons. Put the arrow in `--faint` at rest and `--fg` on hover. Status markers are 7px squares drawn in CSS (see [Status](#10-state-and-status)).

## 5. Layout

### 5.1 The frame

```css
.frame {
  max-width: 1200px; margin: 0 auto; min-height: 100vh;
  border: 1px solid var(--line); border-top: 0;
  display: flex; flex-direction: column;
}
```

- The body has a side padding of `max(16px, env(safe-area-inset-left))`, so the frame's vertical rules stay visible on wide screens and phones.
- The footer sits at the bottom of the frame (`main { flex: 1 }`).
- Every section inside the frame is full width and ends with `border-bottom: 1px solid var(--line)`.

### 5.2 Gutters and spacing

- `--gutter: 24px` (16px under 560px). This is the side padding of every full-width row.
- There is no strict spacing scale. Use these common values: 4, 6, 10, 14, 16, 18, 24, 32, 36, 44, 56 px. Vertical padding of section headers is uneven on purpose: more on top than below (for example `26px` top, `18px` bottom; `44px` / `30px`), so the heading sits near the content it introduces.
- Reading column: a fixed `700px`, not `ch`, so that elements with different font sizes line up on the same edge: `width: min(100% - 2 * var(--gutter), 700px); margin-inline: auto`.
- Text measure for leads and blurbs: `max-width: 46ch` to `70ch`.

### 5.3 Split rows

A hero or header row can split into cells with a vertical rule between them, for example a `1.35fr / 1fr` intro (copy | panel) or the header grid (brand | nav | search). Each cell has its own `border-right`. Under 960px, cells stack and the vertical rule becomes a horizontal one.

### 5.4 Tiling

Three ways to tile with shared lines. Use the one that fits:

1. **Grid with shadow lines** (wrapping card grid): each tile has `box-shadow: 1px 0 0 var(--line), 0 1px 0 var(--line)`. The outer lines fall on the frame and the next rule.
2. **List with top-left border** (link lists): the list has `border-top` and `border-left`; each item has `border-right` and `border-bottom`.
3. **Gap on a line-coloured background** (stat blocks): `gap: 1px; padding: 1px; background: var(--line-2)`, cells have `background: var(--bg)`.

For adjacent buttons, use `margin-left: -1px` so they share one edge.

### 5.5 Horizontal shelves

A row of cards that scrolls inside itself:

- `grid-auto-flow: column; grid-auto-columns: calc(100% / 4.25)` (2.6 under 960px, 1.3 under 560px). The fraction shows part of the next card, which tells the user the row scrolls.
- `scroll-snap-type: x mandatory`, `overscroll-behavior-x: contain`, thin scrollbar in `--line-2`.
- Prev/next square buttons in the header, shown only with JavaScript, disabled at each end, hidden when everything fits.

### 5.6 The blueprint grid

A decorative panel can show a 32px line grid:

```css
background:
  linear-gradient(var(--line) 1px, transparent 1px) 0 0 / 32px 32px,
  linear-gradient(90deg, var(--line) 1px, transparent 1px) 0 0 / 32px 32px,
  var(--panel);
```

Anything placed on it snaps to the grid: start on a crossing, span whole units, and make the inner lines land on grid lines. Mark the corners of a framed object with small L-shaped **crop marks** (9px, 1px `--fg`, offset −5px) at the top-left and bottom-right.

## 6. Components

### 6.1 Header

- Sticky, `--bg`, bottom rule. A grid of cells, each separated by a vertical rule: brand | nav | search.
- **Brand mark**: a 12px square outline with a 6px filled square inside, drawn in CSS, then the name in 600 weight with -0.01em tracking.
- **Nav links**: 14px, `--muted`, padding 14px 16px, each with a right rule. Hover: `--fg` on `--panel`. Current page: `--fg` with a 2px inset bottom bar (`box-shadow: inset 0 -2px 0 var(--fg)`). Nav scrolls sideways with a hidden scrollbar when it does not fit.
- **Search**: a borderless input that fills its cell. Placeholder in `--faint` shows the shortcut (`Search  /`). Focus: `--panel` background plus the same 2px inset bottom bar, no outline. `/` focuses it from anywhere; `Escape` clears; `Enter` opens the first result.
- Under 1120px, the nav moves to its own row below brand and search.

### 6.2 Popover (search results, hover preview)

- `--bg` background, a 1px border, no shadow, no radius.
- Search results: border `--line-2`, rows split by `--line`, row hover `--panel`. Title 14px 600, meta in label style.
- Hover preview: border `--fg` (strongest edge, because it floats over text), 12px 14px padding, label + title + muted summary.
- Position the popover 1px or 6px below its anchor and keep it 8px inside the viewport.

### 6.3 Card

- A full link block: picture on top (3:1, `border-bottom: 1px solid var(--line)`), then text with padding `14px 16px 18px` and `gap: 6px`.
- Text order: label (group) → title (16px 600, 2 lines max) → summary (14px muted, 2 lines max) → optional status.
- Hover: background to `--panel`, title underlined (1px, offset 3px). No lift, no scale, no shadow.
- Focus: outline inset (`outline-offset: -2px`), so it is not hidden by neighbours.

### 6.4 Section header (shelf)

Title (24px, links to the full list, followed by a faint mono `→`), blurb below in `--muted` 15px, and on the right a count and the arrow buttons, aligned to the bottom.

### 6.5 Square buttons

40px square (36px on phones), 1px `--line-2` border, `--bg` fill, mono glyph. Hover **inverts**: background `--fg`, text `--bg`. Disabled: `--faint` text and `--line` border. Inversion is the only "strong" hover in the system; keep it for small controls.

### 6.6 Stats block

A tiled `dl`: each cell has a label (`dt`) and a mono number (`dd`, 22px, tabular figures). A secondary part of the number (`/ 40`) is `small`, 13px, muted. One cell can span both columns.

### 6.7 Progress meter

One 7px square per item, 3px gap, outline `--line-2`. Filled items are solid `--fg`. It is a precise, countable alternative to a progress bar.

### 6.8 Note box

For "not ready" or info notes: `1px dashed var(--line-2)`, padding 16px 18px, muted text, and a label-style title in `--fg` on top (via `::before` or a real element).

### 6.9 Link list

A tiled list of links, columns `repeat(auto-fill, minmax(190px, 1fr))`. Each item: title left, mono `→` right (`justify-content: space-between`), padding 10px 12px, 15px 500. Hover `--panel`, arrow to `--fg`. A secondary item swaps the arrow for a tiny label ("Planned").

### 6.10 Footer

Label style, split left/right with `justify-content: space-between`, top rule, padding `18px var(--gutter)`. Links have no underline; hover to `--fg`.

## 7. Prose (long-form text)

- 17px / 1.7, in the 700px column. The first child gets 24px top margin.
- Block spacing: `margin: 0 0 1.1em`. h2: `1.9em 0 .6em`. h3: `1.6em 0 .4em`.
- Unordered lists use **square** markers in `--faint`. Ordered list numbers are mono, 0.85em, `--faint`.
- `strong` is 600, not 700.
- Inline code: mono 0.86em, `--sunk` background, 1px `--line` border, padding `1px 5px`.
- Code block: `--sunk`, 1px `--line` border, padding 14px 16px, mono 14px/1.6, horizontal scroll.
- Blockquote: no indent, a **2px `--fg`** left bar, 16px padding, muted text.
- Table: full grid of 1px `--line` borders, cells 8px 12px, 15px text. Header cells use the label style on `--panel`. The table scrolls sideways inside itself on small screens.
- `hr`: a 1px `--line` rule with 2em margin.

## 8. Imagery and illustrations

Pictures are **hand-drawn inline SVG diagrams**, like a teacher's sketch on a whiteboard. They are the main visual identity of each page.

- **Canvas**: `viewBox="0 0 1200 400"` (3:1). Keep a margin of about 30 units. Show it full width on the page and scaled down on cards, at the same ratio.
- **One idea per picture.** Draw the single thing the page explains, not a whole screen.
- **Colour only through tokens** with a light fallback: `style="fill: var(--figure-up, #1a9b5b)"`. That makes the SVG follow the theme when it is inlined.
- **Colour meaning**: accent = the subject; up/down = positive/negative; fg = everything else.
- **Hierarchy with opacity**, not extra colours: context shapes at 0.3–0.55 opacity, the subject at full strength. Faint guide lines at 0.18–0.35.
- **Strokes**: main line 6, secondary 3, guides 2. Dashed guides use `stroke-dasharray="6 6"` or `"10 10"`. Sharp joins (`miter`) for data lines.
- **Text**: a few short UPPERCASE labels, `system-ui`, 700, size 26–30, letter-spacing about 3. They must stay readable at a quarter size.
- **Accessibility**: `role="img"` and an `aria-label` that says what the picture shows.
- **Inline safety**: no `id` attributes (many SVGs share one page), no external images or fonts.
- **Placeholder** for content that does not exist yet: faint lines at 0.18 opacity and a centred, wide-tracked label ("COMING SOON") at 0.45 opacity.
- In the UI, a secondary item shows its picture greyscale at 0.6–0.7 opacity.

### Favicon

A small, bold silhouette with one accent element. Cut a gap round the accent with an SVG mask so it reads on any tab colour. Switch fill colours with `@media (prefers-color-scheme: dark)` inside the SVG.

## 9. Links

| Kind | At rest | Hover |
|---|---|---|
| Important in-text link (exists) | `--fg` text, 2px `--hi` underline, offset 3px | text turns `--hi` |
| Secondary in-text link (not ready) | `--muted` text, 1px dotted `--line-2` underline | text turns `--fg` |
| Plain prose link | inherited colour, underline in `--line-2`, offset 3px | |
| Navigation and block links | no underline | `--fg` and/or `--panel`, or underline the title |

Links inherit their colour (`a { color: inherit }`). Colour alone never marks a link; the underline does.

## 10. State and status

| State | Treatment |
|---|---|
| Hover | background `--panel`; text to `--fg`; arrows `--faint` → `--fg` |
| Current | `--fg` text + 2px inset bottom bar |
| Focus | `outline: 2px solid var(--hi); outline-offset: 2px` (inset −2px inside tiles) |
| Disabled | `--faint` text, `--line` border, default cursor |
| Secondary / not ready | `--muted` text, weight 500 → 400 or 600 → 500, greyscale picture, dashed or dotted lines |
| Status tag | label style in `--faint`, prefixed by a 7px outlined square (`::before` with `border: 1px solid currentColor`) |
| Empty | one muted line with gutter padding |

## 11. Motion

```css
@media (prefers-reduced-motion: no-preference) {
  .card, .nav-link, .square-button, .link-item { transition: background-color .12s, color .12s; }
}
```

- Only colour and background change. No transforms, no fades on entry, no spinners for instant work.
- Scroll buttons use `scrollBy({ behavior: "smooth" })`.

## 12. Responsive

| Breakpoint | Changes |
|---|---|
| ≤ 1120px | header becomes two rows (brand + search, then nav) |
| ≤ 960px | split rows stack; shelves show 2.6 cards |
| ≤ 560px | gutter 16px; smaller header padding; shelves show 1.3 cards; 36px buttons; prose 16px |

- No horizontal page scroll at any width. Wide things (nav, shelves, tables, code) scroll inside themselves.
- Respect safe-area insets on the body.
- Use `minmax(0, 1fr)` and `min-width: 0` on grid children so long words do not break the layout; use `overflow-wrap: anywhere` on titles.

## 13. Accessibility and robustness

- Visible focus on every interactive element (`:focus-visible`).
- `aria-current="page"` for the current nav item; `aria-label` on icon-only buttons and on search.
- Decorative markup (meters) gets `aria-hidden="true"` when the same number is in text nearby.
- Core content works without JavaScript. Add `html.js` from the script and show JS-only controls under it.
- `[hidden] { display: none !important; }` so the attribute always wins.
- Check contrast: `--muted` on `--bg` must pass 4.5:1 in both themes; `--faint` is only for non-essential text.

## 14. Starter tokens

Copy this block into a new project, then build components from sections 6 and 7.

```css
:root {
  --bg:     oklch(0.978 0.002 250);
  --panel:  oklch(0.995 0.001 250);
  --sunk:   oklch(0.955 0.003 250);
  --fg:     oklch(0.22 0.006 250);
  --muted:  oklch(0.50 0.008 250);
  --faint:  oklch(0.62 0.006 250);
  --line:   oklch(0.88 0.004 250);
  --line-2: oklch(0.68 0.006 250);
  --hi:     oklch(0.53 0.18 262);

  --figure-bg:     oklch(0.955 0.003 250);
  --figure-fg:     oklch(0.22 0.006 250);
  --figure-up:     oklch(0.56 0.13 150);
  --figure-down:   oklch(0.56 0.17 27);
  --figure-accent: var(--hi);

  --sans: "Geist", "Segoe UI", system-ui, -apple-system, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
  --gutter: 24px;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:     oklch(0.165 0.004 250);
    --panel:  oklch(0.195 0.005 250);
    --sunk:   oklch(0.145 0.004 250);
    --fg:     oklch(0.93 0.003 250);
    --muted:  oklch(0.68 0.006 250);
    --faint:  oklch(0.55 0.006 250);
    --line:   oklch(0.29 0.006 250);
    --line-2: oklch(0.46 0.008 250);
    --hi:     oklch(0.74 0.15 262);
    --figure-bg:   oklch(0.205 0.005 250);
    --figure-fg:   oklch(0.92 0.003 250);
    --figure-up:   oklch(0.74 0.14 150);
    --figure-down: oklch(0.70 0.16 27);
    color-scheme: dark;
  }
}
/* repeat the dark block under :root[data-theme="dark"] */

*, *::before, *::after { box-sizing: border-box; border-radius: 0; }
[hidden] { display: none !important; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.55 var(--sans); -webkit-font-smoothing: antialiased;
  padding: 0 max(16px, env(safe-area-inset-right, 0px)) 48px max(16px, env(safe-area-inset-left, 0px));
}
a { color: inherit; }
button, input { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--hi); outline-offset: 2px; }
@media (max-width: 560px) { :root { --gutter: 16px; } }

.label { font: 500 11px/1.4 var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.frame { max-width: 1200px; margin: 0 auto; min-height: 100vh; border: 1px solid var(--line); border-top: 0; display: flex; flex-direction: column; }
```

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
```

## 15. Checklist for a new screen

- [ ] Everything sits inside the frame; every section ends with a 1px rule.
- [ ] No radius, no shadow used for depth, no gradient except the blueprint grid.
- [ ] Neighbouring tiles share one line.
- [ ] `--hi` appears only on key links, focus and the figure accent.
- [ ] Metadata uses the label style; numbers are mono with tabular figures.
- [ ] Headings are 600 with negative tracking; body is 16–17px.
- [ ] Secondary states use tone and weight, not new colours.
- [ ] Hover changes only colour and background.
- [ ] Works at 375px wide without page scroll, in light and dark, with the keyboard.
