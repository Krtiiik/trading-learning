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
- One page owns each definition. Other pages give a one-line version in passing and link the owner, so the wording can't drift. Owners so far:
  - market mechanics: bid-and-ask (bid, ask, order book), spread (the spread cost), liquidity (slippage), fees-and-commissions (payment for order flow, overnight financing), broker (custody, CFDs, market maker, compensation schemes), leverage (margin, margin call, stop out, leverage limits);
  - assets: forex-pair (pip, lot), cryptocurrency (blockchain, wallet, stablecoin), index (cap and price weighting);
  - charts: ohlc (open/high/low/close), line-vs-candle-chart (bar chart), peak-and-trough (swing high and low, late confirmation);
  - indicators: moving-average (length), atr (true range, ATR-based stops);
  - strategies: backtest (overfitting, look-ahead bias), entry-and-exit-rules (exit kinds, rule timing);
  - risk and money: stop-loss (stop-limit), position-sizing (position size), risk-reward (target, ratio direction, break-even win rate), win-rate-and-expectancy (win rate, expectancy), drawdown (maximum drawdown, time under water, the gain needed to recover), volatility (historical and implied volatility, the calm and jumpy stocks).
- The site reuses one set of example numbers. Reuse them as they are, and give the full calculation only on the page that owns the idea:
  - the order book: asks $50.02 × 100 and $50.03 × 200, bids $49.98 × 400 and $49.97 × 150;
  - the trade: a $10,000 account risking 1%, 25 shares bought at $42, stop at $38, planned target $54 (3 to 1), sold at $64;
  - the gap: Monday close $40 (low $39.20), Tuesday open $35 (high $36, low $34.50, close $35.50);
  - the calm and jumpy $42 stocks: ATR $1 and $2, stops $38 and $34, 25 and 12 shares, targets $54 and $66;
  - the trend: turning points $40, $48, $44, $53, $49, $58; the trend-following rule buys on a close above the 100-day moving average and sells on a close below;
  - the 10-trade backtest table (backtest, win-rate-and-expectancy, drawdown);
  - forex: EUR/USD at 1.0850, a mini lot of 10,000 units, $1 per pip.
- Fixed glosses, reused word for word: the spread is "the gap between the best price buyers offer and the best price sellers want"; CFDs are "contracts with a broker that pay the change in a price"; on strategy and risk pages, "a trade means one position: a buy and the later sale that closes it".
- Write ratios as "3 to 1", reward first. Only leverage uses the "30:1" form.
- Don't state market conventions as universal: some apps, especially in China and Japan, reverse the candle colours, so write "(usually green)" or "(usually red)" when a colour means up or down. Name the market when a rule is not universal (US, UK, EU).
- Write cents as numerals: "1 cent", "40 cents", not "$0.10".
- End a concept with a "Watch out" section and a linked "Next, see …" line. The Next line should name at least one written page, unless a planned page is clearly the right next step.
- A concept body is usually 300–500 words (each link counted as its display text, tables left out, since they hold numbers the prose already walks through). 500 is a ceiling, to keep pages short; 300 is only a guide. A shorter page that explains its concept fully is fine, so never pad one to reach the count. Count with `uv run python scripts/build.py --words <slug>`; that count is the one that decides.
- Acronym titles need no link text: write `[[atr]]`, not `[[atr|ATR]]`.
- Catalog titles and summaries that contain a comma must be quoted; the build rejects them otherwise.
- Adding a concept starts in `catalog.yaml` (slug, title, summary). Writing it means adding `content/concepts/<group>/<slug>.md` (body only, no frontmatter) and `banners/<slug>.svg`.
- Lessons need frontmatter `title`, `summary`, `added` (date) and `builds_on` (concept slugs).
- Banners: `viewBox="0 0 1200 400"`, colours only through `--banner-bg/fg/up/down/accent` with fallbacks, no `id` attributes. Each one should show at a glance what the page explains.

## Where things go

- Site sources (catalog, content, banners, templates, static assets) live at the repository root; Python scripts go in `scripts/`, their tests in `tests/`, and the built site in `dist/` (not committed).

## Testing

<!-- What gets tested and how; test layout and naming. -->
