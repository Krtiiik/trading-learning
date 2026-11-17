# Course site design

The visual design of the `learn/` Jekyll site: tokens, layout, and every screen and component with its states. A port session builds the site from this file and the mockups; where they disagree, this file wins.

- **Mockups:** [`design/`](design/) (open `design/index.html` through a local server, e.g. `python -m http.server -d learn/design`), also published as a private artifact: <https://claude.ai/artifact/Wc4mobPXcD1jzvwTGvnDk7> (its main page is `index.html` with the document wrapper stripped, since the artifact host adds its own)
- **Reference CSS:** [`design/design.css`](design/design.css) implements everything below and can be lifted into the site's stylesheet almost unchanged. Sections 1–11 of that file match the sections here. The "Mockup only" block at its end and [`design/design.js`](design/design.js) are scaffolding; `design.js` shows the intended behaviour but is not production code.
- **States gallery:** [`design/components.html`](design/components.html) freezes every component state side by side.

## Direction

A quiet paper page. Serif (Literata) for everything you read, sans (Inter) for everything you operate: nav, sidebar, TOC, buttons, tables, chat. Warm paper neutrals in light, warm charcoal in dark. Orange is rare: it marks only interaction (links, focus, buttons) and "you are here" (current lesson, current TOC section, lesson number in the kicker). It never decorates.

This replaces the Tufte look in `assets/course.css`. Margin notes are gone: notes are inline asides at every width.

## 1. Tokens

All colours are CSS custom properties on `:root`. Dark values apply in two places with identical values: under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and under `:root[data-theme="dark"]`. Both dark blocks also set `color-scheme: dark`. No component uses a literal colour.

### Colour

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#FAF7F0` | `#1A1815` | Page paper. `body` background. |
| `--raised` | `#FFFDF8` | `#211E1A` | Cards, quiz boxes, chat panel, popovers, drawer. |
| `--surface` | `#F3EEE3` | `#26231D` | Code, hover fills, inline TOC, user chat bubble. |
| `--ink` | `#22201C` | `#ECE6DA` | Body text, headings. |
| `--ink-2` | `#4A453D` | `#CFC7B8` | Subtitles, notes, explanations, sidebar items. |
| `--muted` | `#6E685E` | `#A39B8C` | Labels, captions, nav links, table headers. |
| `--faint` | `#958D80` | `#7A7366` | Placeholders, idle icons, lesson numbers in lists. Never body text. |
| `--rule` | `#E4DDCE` | `#38332B` | Hairlines, card borders. |
| `--rule-strong` | `#CFC6B4` | `#4A443A` | Control borders, table header rule, note rule. |
| `--accent` | `#C2581C` | `#E8925A` | Focus ring, hover borders, slider, markers, TOC indicator. Not for text in light. |
| `--accent-text` | `#A84C15` | `#EDA273` | Links and any orange text. |
| `--accent-fill` | `#A84C15` | `#E8925A` | Filled buttons (Check, Ask Claude, send). |
| `--on-accent` | `#FFFFFF` | `#1A1815` | Text and icons on `--accent-fill`. |
| `--tint` | `#F6E7DA` | `#3A2A1F` | Current sidebar item, highlighted table row, key box. |
| `--good` / `--good-bg` | `#2F6B45` / `#E3EEE5` | `#86C79A` / `#1F3326` | Right answer. |
| `--bad` / `--bad-bg` | `#A8322D` / `#F7E1DC` | `#EF9A93` / `#3B2220` | Wrong answer, chat error. |
| `--shadow` | two-layer warm brown, 6% and 10% | two-layer black, 30% and 45% | Floating things only: FAB, popover, overlay panel, drawer. |
| `--scrim` | `#22201C` at 32% | black at 55% | Behind drawer and overlay chat. |

Contrast (WCAG, on `--bg`, light / dark): ink 15.2 / 14.3, ink-2 8.9 / 10.6, muted 5.2 / 6.4, accent-text 5.3 / 8.5, good 5.9 / 9.0, bad 6.2 / 8.2. Text on fills: `--on-accent` on `--accent-fill` 5.7 / 7.3; good and bad text on their own `-bg` at least 5.3. `--accent` (`#C2581C`) is only 4.2:1 on light paper, which is why link text uses `--accent-text`. `--faint` is about 3:1 and is for non-text or placeholder use only.

### Type

Google Fonts, one request: `Inter:wght@400;500;600`, `JetBrains+Mono:wght@400;600`, `Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400`, `display=swap`. Literata uses its optical-size axis (`font-optical-sizing: auto`).

| Token | Family | Fallbacks |
|---|---|---|
| `--serif` | Literata | Iowan Old Style, Palatino Linotype, Georgia, serif |
| `--sans` | Inter | Segoe UI, system-ui, -apple-system, sans-serif |
| `--mono` | JetBrains Mono | Cascadia Mono, Consolas, monospace |
| `--math` | Latin Modern Math | STIX Two Math, Cambria Math, math |

| Token | Desktop | Phone (<840px) | Face, weight, line height | Used for |
|---|---|---|---|---|
| `--fs-display` | 44px | 34px | serif 600, 1.08, −0.02em | Dashboard title |
| `--fs-h1` | 38px | 30px | serif 600, 1.15, −0.015em | Page titles |
| `--fs-h2` | 24px | 22px | serif 600, 1.3 | Section headings (`##`) |
| `--fs-h3` | 19px | 19px | serif 600, 1.35 | `###`, card titles |
| `--fs-lead` | 20px | 18px | serif italic 400, 1.5 | Subtitle, dashboard lead |
| `--fs-body` | 18px | 17px | serif 400, 1.7 | Reading text |
| `--fs-small` | 16px | 16px | serif 400, 1.6 | Notes, explanations, Claude replies, card text |
| `--fs-ui` | 15px | 15px | sans 400–600 | Buttons, tables, chat input, user messages |
| `--fs-ui-sm` | 14px | 14px | sans 500 | Nav links, sidebar, feedback |
| `--fs-ui-xs` | 13px | 13px | sans | TOC, kicker, table headers, captions |
| `--fs-label` | 12px | 12px | sans 600, uppercase, +0.08em | Micro-labels: PART 2, KEY IDEA, QUESTION 4, ON THIS PAGE |

Headings use `text-wrap: balance`. Tables use `font-variant-numeric: tabular-nums`. Inline `code` is 0.84em of its context.

### Space, shape, measure

- Spacing scale (4px base): `--s1` 4, `--s2` 8, `--s3` 12, `--s4` 16, `--s5` 24, `--s6` 32, `--s7` 48, `--s8` 64 (px). Use it for every gap and padding.
- Radius: `--r-sm` 4 (inline code, kbd), `--r-md` 8 (buttons, fields, choices, sidebar items, code blocks), `--r-lg` 12 (quiz boxes, cards, panel, popover), `--r-full` (pills, FAB).
- Measure: `--measure` 42rem (672px, about 70 characters of Literata 18px) for lessons and plain pages; `--measure-wide` 60rem for reference sheets.
- Chrome: `--nav-h` 56px (52px on phone), `--sidebar-w` 264px (240px on tablet), `--toc-w` 216px, `--panel-w` 400px, `--col-gap` 48px (40px on tablet), `--page-max` 1440px.

## 2. Layout and breakpoints

Every page: optional mockup bar (mockups only) → sticky nav bar → page body. The page side gutter is `max(24px, safe-area inset)` (16px on phone), written with `padding-left`/`padding-right`, never a `padding` shorthand.

| Width | Lesson | Reference | Dashboard, Mission, Resources |
|---|---|---|---|
| ≥ 1280px | sidebar · lesson · TOC rail | sidebar · wide content | single centred column |
| 840–1279px | sidebar · lesson, TOC becomes inline disclosure | sidebar · wide content | single centred column |
| < 840px | one column, sidebar in a drawer, TOC inline disclosure | one column, drawer | one column, drawer |

- The lesson column is `minmax(0, 1fr)`; the prose inside it is capped at `--measure` and centred in that column, so text sits midway between sidebar and TOC.
- Sidebar and TOC rail are `position: sticky` below the nav and scroll on their own.
- Page bottom padding is 64px so the FAB never covers the last line.
- Below 640px the chat panel is full-screen.

## 3. Site chrome

### Nav bar
- 56px, sticky at `top: env(safe-area-inset-top)`, `--bg` with a `--rule` bottom border. A fixed `body::before` paints the phone status-bar band in `--bg`.
- Left: course mark + "Algorithmic Trading" (Inter 15 600, `--ink`), links to the dashboard. The mark is a 20px OHLC bar drawn in `--accent`: one vertical stroke with an open tick left and a close tick right (`M10 3v14 M6 7h4 M10 13h4`, stroke 2, round caps).
- Right: Reference, Resources, Mission (Inter 14 500 `--muted`; hover `--ink` on `--surface`; current page `--ink` with a 2px `--accent` underline at the bar's bottom), then the theme toggle.
- "Reference" links to the reference sheet when there is one, later to the first sheet or a list.
- Phone: menu button (36px, left), mark + title, theme toggle (right). Links move into the drawer.

### Theme toggle
- 36px icon button: sun in light, moon in dark (whichever theme is showing).
- Default follows the OS. A click sets `data-theme="light|dark"` on `<html>` to the opposite of what is showing and stores it in `localStorage` (key `course-theme`, wrapped in try/catch). On load, a stored value is applied before first paint (inline script in `<head>`).

### Course sidebar (lessons and reference sheets)
- Inter 14. For each part from `_data/parts.yml`, in order: a label `PART n` (`--muted`), the part title (600 `--ink`), then its lessons as a list.
- Lesson row: number (13px `--faint`, tabular) in a 24px column + the lesson's `short` (`--ink-2`). Padding 6px 8px, `--r-md`. Hover: `--surface` background, `--ink`. Current: `aria-current="page"`, `--tint` background, `--ink` 600, number in `--accent-text`.
- Planned part (no lessons yet): label reads `PART n · [Planned]` (pill: 11px, `--rule-strong` border, `--r-full`), title in `--muted` 500, no list.
- After the parts, a hairline and `REFERENCE` with one row per reference sheet, styled like lesson rows without a number.
- Phone drawer: the same sidebar slides in from the left (`min(20rem, 86vw)`, `--raised`, `--shadow`, 220ms ease; reduced motion: no transition) over a `--scrim`. It starts with the site links (Course home, Reference, Resources, Mission) above a hairline. Closes on scrim tap, Esc, or link tap. Dashboard, Mission and Resources include the sidebar only for this drawer.

### On-page TOC
- Built from the page's `##` headings, including Practice. Each `h2` gets an id (slug of its text).
- Rail (≥1280px): label `ON THIS PAGE`, then a list with a 1px `--rule` left track. Items Inter 13 `--muted`, 4px vertical padding; hover `--ink`. The section currently in view gets `aria-current="true"`: `--accent-text`, 600, and a 2px `--accent` segment on the track. "In view" is the last `h2` whose top is above 140px from the viewport top.
- Inline (below 1280px, and whenever the chat panel is docked): a `<details>` right under the lesson header, closed by default, on `--surface` with `--r-md`. Summary: list icon, "On this page" (Inter 14 600), chevron that flips when open. Items as a numbered list.

## 4. Screens

### Dashboard
Single column, max 68rem, 64px top padding.
- **Hero** (max `--measure`): kicker "A course built alongside the trading workbench"; title "Algorithmic Trading" (`--fs-display`); lead paragraph = the mission's *Why* in second person; "Read the mission" link; a facts row in Inter 13 `--muted` with the numbers in `--ink` 600 (lessons count, ETF count in the universe, data source and start year).
- **Grid**: parts column `minmax(0, 1fr)` + aside 17rem, 48px gap. Below 840px the aside stacks after the parts.
- **Part block**: label `PART n` in `--accent-text`; title h2 26px; description (`--fs-small`, `--ink-2`); lesson list.
- **Lesson row** (whole row is the link): 44px number column (Literata 19 600 `--faint`, tabular lining figures), then title (Literata 18 600 `--ink`) and the lesson's `short` line under it (16px `--muted`), then an arrow icon (`--faint`). Rows separated by `--rule` hairlines with one on top. Hover: `--surface` row, number turns `--accent-text`, arrow `--accent`. On phone the arrow is hidden and the number column is 32px.
- **Planned part**: label `PART n · [Planned]` in `--muted`, title in `--muted`, description, then "Lessons appear here as they are written." (Inter 13 `--muted`) under a dashed `--rule-strong` line.
- **Aside** (sticky below the nav on desktop): groups `REFERENCE SHEETS` and `FURTHER READING` (Resources, Mission). Each entry is a `--raised` box with `--rule` border, `--r-md`: title Inter 14 600, one line of description Inter 13 `--muted`. Hover: `--accent` border.

Mockup note: Parts 3 and 4 in the mockup are invented placeholders to show the planned state.

### Lesson page
- **Header** (`.page-head`): kicker `LESSON n · Part title` (Inter 13 600 uppercase; "Lesson n" in `--accent-text`, the part in `--muted`), h1 title, subtitle (lead, italic, `--ink-2`). 24px bottom padding and a `--rule` hairline, 32px before the content.
- Lesson prose: Literata 18/1.7, paragraphs 1.1em apart, `h2` 48px above and 12px below, list markers `--muted`.
- Ends with the Practice section and then the Ask Claude invitation (see 6).
- No prev/next links, no progress marks.

### Reference sheet
- Sidebar + wide content (`--measure-wide`), no TOC.
- Header kicker `REFERENCE` in `--accent-text`.
- Cards (`.cards`): grid `repeat(auto-fit, minmax(min(100%, 22rem), 1fr))`, 24px gap. Card: `--raised`, `--rule` border, `--r-lg`, 24px padding (16px on phone), its `h2`/`h3` at 19px with no top margin, text at `--fs-small`.

### Mission and Resources (plain Markdown pages)
- Single centred column at `--measure`, header kicker `COURSE`, h1 from the Markdown.
- `blockquote`: `--surface` box, `--r-md`, `--fs-small`, `--ink-2`, no left bar.
- Resource lists (`ul` with class `links`, e.g. a kramdown IAL `{: .links}`): each item is a block with a hairline below; the first link is on its own line at 18px 600, the description under it at 16px `--ink-2`.

## 5. Content components

| Component | Look | States |
|---|---|---|
| Data table | Inter 15, tabular figures, width 100%, inside `.table-wrap` (`overflow-x: auto`). Header: 13px 600 `--muted`, `--rule-strong` bottom border. Rows: `--rule` hairlines. First column 500. `td.num`/`th.num` right-aligned, no wrap. Tables with numeric columns keep the first column on one line; text-only tables give each cell `min-width: 9rem` so they scroll instead of squeezing on phones. | Highlighted row `tr.hl`: `--tint` background and a 2px `--accent` inset bar on its first cell. |
| Formula (display) | KaTeX, centred, 24px above and below, 1.12em, scrolls horizontally inside its own box when wider than the column. | — |
| Inline math | KaTeX at text size. | — |
| Code block | `--surface`, 1px `--rule`, `--r-md`, JetBrains Mono 14/1.55, scrolls horizontally. | — |
| Inline code | `--surface`, `--r-sm`, 0.84em. | — |
| Note `.note` | Inline aside: 16px `--ink-2`, 1px `--rule-strong` left rule, 16px left padding, label `NOTE` above. | — |
| Key takeaway `.key` | `--tint` box, `--r-md`, 16×24 padding, label `KEY IDEA` in `--accent-text`. No border. | — |
| Source line `.source` | Inter 13 `--muted`. | — |
| Reveal `details.reveal` | `--raised` box, `--rule` border, `--r-md`. Summary Inter 15 600 `--accent-text` with a chevron. | Closed; open (chevron rotates 90°, body below). |
| Slider + table `.numeric-slider` | `--raised` box, `--r-lg`. Head row: caption left (Inter 14 `--muted`), current value right (mono 14 600). Native range input with `accent-color: var(--accent)`, tick labels below (12px `--faint`, tabular). Table under it with its one row highlighted. | Value changes update the head and the row. |

### Multiple-choice quiz `.quiz`
- Box: `--raised`, `--rule` border, `--r-lg`, 24px padding (16px on phone), 24px from neighbours.
- Question: label `QUESTION n` above, then the question in Literata 18 600. The number moves from the question text into the label.
- Choices: full-width buttons, 8px apart. Inter 15, `--bg`, `--rule-strong` border, `--r-md`, 10×14 padding. Leading mark: 24px circle with the letter A–D (12px 600 `--muted`, `--rule-strong` border).

| State | Look |
|---|---|
| Idle | as above |
| Hover / focus | border `--accent`, mark border and letter `--accent`; focus adds the 2px `--accent` ring |
| Wrong (clicked) | `--bad-bg`, border `--bad`, mark filled `--bad` with a white ✕ icon; that button is disabled, the rest stay live |
| Right (clicked) | `--good-bg`, border `--good`, mark filled `--good` with a ✓ icon; all buttons disable, untouched ones fade to 55% |
| Explanation | appears below the choices after a hairline: label `EXPLANATION`, text 16px `--ink-2` |

### Numeric-answer quiz `.numeric`
- Same box and question as above. Row: input (JetBrains Mono 15, 11rem, `--bg`, `--rule-strong` border, `--r-md`; placeholder "e.g. 12.3%" for percent answers), **Check** (primary filled button), **Show solution** (ghost text button in `--accent-text`). The row wraps on phone.

| State | Look |
|---|---|
| Idle | as above |
| Focus | input border `--accent` + 3px `--accent` halo at 22% |
| Empty on Check | input border `--bad`; feedback "✕ Type a number first." (Inter 14 `--bad`) |
| Wrong | input border `--bad`; feedback "✕ Not quite: too high. Try again." or "too low" |
| Correct | input `--good-bg` with `--good` border, read-only; feedback "✓ Correct." (600 `--good`); solution appears |
| Solution shown (gave up) | solution appears, no feedback line, input stays editable |
| Solution | below a hairline: label `SOLUTION`, text 16px `--ink-2` |

### Buttons
- Primary: `--accent-fill` with `--on-accent`, Inter 15 600, 10×16 padding, `--r-md`. Hover: brightness 1.08.
- Secondary: `--raised`, `--rule-strong` border; hover border `--accent`.
- Ghost: `--accent-text`, no border; hover `--surface`.
- Icon button: 36px square, `--muted` icon; hover `--surface` and `--ink`.
- Disabled: 50% opacity. Focus everywhere: 2px `--accent` outline, 2px offset.
- Icons: 18px, 1.75 stroke, round caps (Lucide style), `currentColor`.

## 6. Ask Claude

The whole feature renders only when the page is served as an artifact. Outside it (local `jekyll serve`), the FAB, panel, selection icon and end-of-lesson invitation are absent, with no empty space left.

### Floating button (every page)
- Fixed bottom-right at 24px (16px on phone) plus safe-area insets. Pill: chat icon + "Ask Claude", Inter 14 600, `--accent-fill`/`--on-accent`, `--r-full`, `--shadow`.
- When this page already has a saved conversation, a 11px `--good` dot with a 2px `--bg` ring sits on its top-right corner.
- Phone: icon only, 52px circle.
- Hidden while the panel is open.

### End-of-lesson invitation (lessons)
After Practice: a dashed `--rule-strong` box, `--r-lg`. Left: the lesson's closing question in 16px `--ink-2` (the old "Ask your teacher" line). Right: secondary button "Ask Claude" that opens the panel.

### Selection popover (lessons only)
1. When the reader selects text inside the lesson prose (not inside quiz controls), a 32px round button with a sparkle icon (`--accent-fill`, `--shadow`) appears just above and to the right of the selection's last line.
2. Clicking it replaces it with a menu card below the selection (17.5rem, `--raised`, `--rule` border, `--r-lg`, `--shadow`): a row "✦ Explain this" (Inter 14 600, focused first) and, under a hairline, a one-line field "Ask something else…" with a send button.
3. Either action opens the panel and sends a user message carrying the selection as a quote chip. Esc, a click elsewhere or a new selection closes the popover.
- On phone the menu also opens below the selection, so it doesn't fight the system's selection menu above it.

### Side panel
- **Docked (≥1024px):** fixed to the right edge below the nav, 400px wide, full remaining height, `--raised`, `--rule` left border. The page shifts left by 400px and reflows: the TOC rail hides (inline TOC appears instead); between 1024 and 1439px the sidebar also hides and the menu button appears in the nav to reach it as a drawer.
- **Overlay (<1024px):** the panel slides over the page from the right, full height, `--shadow`, over a `--scrim`. Full-screen below 640px.
- **Header:** "Ask Claude" (Inter 15 600) and "About: <page title>" (13px `--muted`, one line, ellipsis); right: ghost button "+ New topic", close (✕). Esc closes.
- **Body:** scrolls; opens scrolled to the bottom. 16px padding, 16px between messages.
- **Footer:** composer (auto-growing textarea up to 9rem, Inter 15, inside a `--bg` box with `--rule-strong` border and `--r-lg`; focus = `--accent` border + halo) with a send button (`--accent-fill`, disabled = `--surface`/`--faint` until there is text). Enter sends, Shift+Enter adds a line. Under it, 12px `--faint`: "Claude reads this page and anything you select. Saved with this page."

### Messages
- **User:** right-aligned bubble, max 88% wide, `--surface`, radius 12 with a 4px bottom-right corner, Inter 15 `--ink`.
- **Quote chip** (inside a user bubble when sent from a selection): 2px `--accent` left bar, line "From § n · Section title" (12px 600 `--muted`), then the selected text in 13px italic `--ink-2`, clamped to 3 lines.
- **Claude:** no bubble; Literata 16/1.65 `--ink`, full width, Markdown and KaTeX rendered.
- **Date divider:** centred uppercase 12px `--faint` label between `--rule` lines: the day ("Tue 17 Nov") for earlier days, "Today" for today. One per day that has messages.
- **New topic divider:** same shape, label "New topic" in `--accent-text`, dashed `--rule-strong` lines. Inserted by the "New topic" button and stored in the thread. It tells Claude (and a later teaching session) that what follows doesn't continue the previous exchange.

### Panel states
| State | Look |
|---|---|
| Empty (page has no thread) | Vertically centred block: "Ask about “<short title>”" (Literata 19 600), one line of help (Inter 14 `--ink-2`), then 2–3 suggested prompts as full-width outline buttons (`--bg`, `--rule` border; hover `--accent` border). Clicking one sends it. |
| Waiting | The user message appears at once; below it three 6px `--faint` dots pulse (1.2s, staggered; reduced motion: static). |
| Streaming | Claude's text grows in place with a blinking `--accent` block caret at the end. |
| Error | In place of the reply: `--bad-bg` box, `--bad` Inter 14 "Claude didn't answer. Your question is kept." and a secondary "Retry" button. |
| Returning thread | Opens on the saved thread with its date dividers, scrolled to the newest message; the composer is empty and focused. |

## 7. Motion and accessibility
- Transitions are short (150–220ms) and only on drawer, panel, chevrons and hover colours. `prefers-reduced-motion: reduce` turns all transitions and animations off.
- Every interactive element shows the 2px `--accent` focus ring. Icon-only buttons have `aria-label`s. The drawer and panel close on Esc.
- `::selection` is `--accent` at 28%.
- Print: no chrome, no practice, no Ask Claude; black on white, links in text colour.

## 8. Notes for the port
- **KaTeX in the artifact:** the artifact's content policy loads scripts from cdnjs but stylesheets only from Google Fonts, so KaTeX's CSS and fonts can't come from a CDN. The mockups load `katex.min.js` and `contrib/auto-render.min.js` from cdnjs (0.16.11) and render with `output: "mathml"`, which needs no KaTeX CSS or fonts; the browser draws the MathML with the `--math` font stack. Keep that, or self-host `katex.min.css` and its fonts in `assets/` if you want KaTeX's HTML rendering.
- With `output: "mathml"` KaTeX emits `span > span.katex > math[display="block"]` for display math (no `.katex-display`); the CSS styles `math[display="block"]` directly. `display: block math` keeps MathML's centring; plain `display: block` loses it.
- Widget markup in the mockups keeps the data attributes of `assets/quiz.js` (`data-answer`, `data-tol`, `data-percent`, `data-choice`) and adds: `.choice` + `.mark` on choice buttons, `.qn` label inside `.q`, and the numeric row built from `.field`, `.btn-primary`, `.btn-ghost`.
- Self-host nothing else: Google Fonts and cdnjs are both allowed in the artifact.
- Class names to reuse: `.site`, `.site-nav`, `.layout.layout-course` (`.no-toc` on reference), `.layout-single`, `.sidebar` (`.drawer-only` where it's only the phone drawer), `.content` (`.wide` on reference), `.prose`, `.page-head`, `.kicker`, `.subtitle`, `.toc`, `.toc-inline`, `.home*`, `.part-block`, `.lesson-list`, `.cards`/`.card`, `.ask-fab`, `.ask-panel`, `.sel-pop`, `.msg-*`, `.quote-chip`, `.divider`. State lives in attributes: `data-theme` on `<html>`, `data-chat` and `data-drawer` on `.site`, `aria-current` on nav, sidebar and TOC links.
