# Conventions

<!--
Idioms and placement rules that a linter or formatter can't enforce.
Skip anything tooling already checks. Prefer a rule plus a one-line reason over a long explanation.
-->

## Code

<!-- Error handling, naming, patterns to follow and patterns to avoid. -->

## Learning site writing

- A concept must make sense on its own to a beginner: plain words, short paragraphs, one concrete example with numbers. Explain any unlinked term you need in passing instead of requiring the reader to click away. Links are for going deeper.
- Link each concept the first time it is mentioned with `[[slug]]`. Use `[[slug|text]]` when the wording differs (plural, inflection, a proper noun that the default lowercasing would break). Default link text is the title with its first letter lowercased, except acronyms.
- Don't follow a `[[slug]]` link with a parenthesis that restates the linked page's catalog summary: the link's hover preview already shows that summary, so the parenthesis only repeats it. Keep a parenthesis after a link only when it adds what the summary does not: a value from the example ("an [[atr]] of $1"), the narrower thing a broader page covers (a limit order linked to order-types, a stop-limit linked to stop-loss), or which example is meant. Prefer working that detail into the sentence ("a weekend [[gap]]") over a parenthesis. If a term needs a better one-line explanation, improve its catalog summary instead.
- Advanced concepts and lessons may lean on basics, and should link them rather than re-explain them.
- One page owns each definition. Other pages give a one-line version in passing and link the owner, so the wording can't drift. Owners so far:
  - market mechanics: bid-and-ask (bid, ask, order book), spread (the spread cost), liquidity, slippage (fill price against expected price, the causes of slippage), fees-and-commissions (payment for order flow, overnight financing, the currency conversion fee and its 0.25% to 1.5% range, stamp duty and transaction taxes), broker (custody, market maker, compensation schemes, how to check a broker and the ČNB register), leverage (margin, margin call, stop out, leverage limits), short-selling (borrow fee, short squeeze, share recall, SEC Rule 201), taxes-on-trading (realised gains, holding-period rules and the oldest-first order of the Czech time test, tax-free allowances, tax-advantaged accounts, the US, UK and Czech tax rates);
  - assets: valuation (market value, earnings, P/E ratio, forward P/E), dividend (the four dates, dividend yield, withholding tax), cfd (CFDs, ESMA's CFD protections, negative balance protection, the losing-accounts warning, the appropriateness test, professional client status), forex-pair (pip, lot), cryptocurrency (blockchain, wallet, stablecoin, MiCA and its July 2026 start), index (cap and price weighting, price and total-return index), etf (expense ratio and TER, leveraged and inverse ETFs, daily reset, UCITS, accumulating and distributing, domicile), bond (face value, coupon, maturity, yield, credit ratings, interest rate risk), futures (expiry, multiplier, futures margin, daily settlement, rolling), commodity (spot price, cost of carry, contango and backwardation, roll cost), option (call, put, strike, premium, exercise and assignment, American and European style, intrinsic and time value, time decay, option break-even), reit (equity and mortgage REITs, the payout rule, FFO);
  - charts: ohlc (open/high/low/close), line-vs-candle-chart (bar chart), peak-and-trough (swing high and low, late confirmation), support-and-resistance (zones, role reversal), breakout (what counts as a break, retest, false breakout), candlestick-pattern (named patterns, pattern confirmation), chart-pattern (named chart patterns, neckline, measured-move target);
  - indicators: moving-average (length), atr (true range, ATR-based stops), rsi (70 and 30 levels, divergence), bollinger-bands (standard deviation of closes, squeeze, walking the band), macd (exponential moving average, signal line, histogram, signal-line and zero-line crossovers), volume-profile (point of control, value area, high- and low-volume nodes);
  - strategies: backtest (overfitting, look-ahead bias), breakout-trading (trailing stop), entry-and-exit-rules (exit kinds, rule timing), momentum (ranking by past return, look-back, momentum crash), buy-and-hold (time in the market), trading-journal (R multiples, paper trading), rebalancing (target mix, drift, calendar and threshold rebalancing);
  - risk and money: stop-loss (stop-limit), position-sizing (position size), risk-reward (target, ratio direction, break-even win rate), win-rate-and-expectancy (win rate, expectancy), drawdown (maximum drawdown, time under water, the gain needed to recover), compounding (compounding, how fees compound, the rule of 72), trading-psychology (loss aversion, disposition effect, revenge trading), volatility (historical and implied volatility, the calm and jumpy stocks), diversification (correlation, company-specific and market-wide risk), currency-risk (how asset and currency returns multiply, listing currency vs holdings, currency-hedged funds and their cost).
- The site reuses one set of example numbers. Reuse them as they are, and give the full calculation only on the page that owns the idea:
  - the order book: asks $50.02 × 100 and $50.03 × 200, bids $49.98 × 400 and $49.97 × 150;
  - the trade: a $10,000 account risking 1%, 25 shares bought at $42, stop at $38, planned target $54 (3 to 1), sold at $64 about eight months later;
  - the gap: Monday close $40 (low $39.20), Tuesday open $35 (high $36, low $34.50, close $35.50);
  - the calm and jumpy $42 stocks: ATR $1 and $2, stops $38 and $34, 25 and 12 shares, targets $54 and $66;
  - the trend: turning points $40, $48, $44, $53, $49, $58; the trend-following rule buys on a close above the 100-day moving average and sells on a close below;
  - the 10-trade backtest table (backtest, win-rate-and-expectancy, drawdown);
  - forex: EUR/USD at 1.0850, a mini lot of 10,000 units, $1 per pip;
  - the range stock: sideways between about $45 and $55 for months, troughs $45.20, $44.70 and $45.40, peaks $54.80 and $55.30, so zones $44.70–$45.40 and $54.80–$55.30; ATR $1, 20-day average $50, standard deviation $2 (bands $46 and $54). Mean reversion buys a close at $46 (RSI 25) with a stop at $42 (4 ATRs below) and exits near $50; support and resistance buys $45.50 with a stop at $43.50 (a little more than one ATR below the zone) and a target of $54.50; breakout trading buys a $56 close on twice the usual volume with a stop at $54 (just below the zone), 50 shares and a target of $65;
  - the short: 25 shares sold short at $42, buy stop at $46, a gap to $50 loses $200;
  - the dividend: 40 cents a quarter on the $42 stock;
  - the future: a Micro E-mini S&P 500 at 6,000, $5 per point, margins $2,500 and $2,250;
  - the bond: $1,000 at a 4% coupon for 10 years, about $920 if rates go to 5%, about $1,085 at 3%;
  - the option: a $45 call on the $42 stock, three months to expiry, $1.50 a share ($150), break-even $46.50;
  - the oil roll: spot $70.00, next month $70.50, a 50-cent (about 0.7%) roll cost;
  - the double top (not the $45–$55 stock): peaks $60.00 and $59.80, neckline $54, close $53.40, target $48, buy stop on a short at $60.50;
  - the REIT: $40, 50 cents a quarter, 5% dividend yield; 6.25% at $32;
  - the rebalance: $10,000 at 60/40, stocks up 30% to $7,800 (about 66%), sell $720 of stocks for bonds, or add $1,200 of new money to bonds;
  - compounding: $10,000 at 7% a year for 30 years grows to about $76,000; about $74,600 with a 0.07% yearly fee and about $61,600 with 0.75% (the fee levels of the etf table);
  - the volume profile of the $45–$55 stock: POC near $50, value area $47–$53 (70 of 100 million shares);
  - the exchange rate: a dollar at 21 CZK;
  - the CFD: 25 shares of the $42 stock, a $1,050 position value, $210 margin at 5:1;
  - the first-order round trip: 100 shares through the shared order book, $2.50 per order, 0.5% conversion each way, $59 (1,239 CZK) in all; the thin evening book: bid $49.90, ask $50.10.
- When a page sets a stop on a shared example, say how it was set (ATRs from the entry, or beyond a zone), and if another page sets a different stop on the same example, name the difference.
- Fixed glosses, reused word for word when a sentence explains the term in its own words (never as a parenthesis after its link, see above): the spread is "the gap between the best price buyers offer and the best price sellers want"; CFDs are "contracts with a broker that pay the change in a price"; on strategy and risk pages, "a trade means one position: a buy and the later sale that closes it". In passing, where a page needs them: a stop loss is "an order that sells automatically if the price falls to a level you chose"; ATR is "the price's average move in one period" ("average daily move" in daily examples); a gap is "a jump in price, for example overnight" (weekend for forex and futures); an ETF is "a fund that holds many assets and trades like one stock"; an index is "a number that tracks the combined price of a basket of stocks"; short selling is "selling borrowed shares, hoping to buy them back cheaper".
- EU fixed glosses: the MSCI World is "an index of more than 1,000 large and mid-sized companies in about 23 developed countries"; write "the ČNB (the Czech National Bank)" on first use; a firm not in the ČNB register "may not offer you investment services in Czechia".
- More fixed glosses, for use in passing: an option is "a contract giving the right, but not the duty, to buy or sell at a set price"; a bond is "a loan to a government or company"; a dividend is "money a company pays for each share you own"; dividend yield is "the past year's dividends divided by the price".
- When a new page becomes the owner of an idea that older pages already mention, link the new owner from those pages in the same change. Every written page needs at least one incoming link from another written page.
- In prose calculations, write division as "/", not "÷".
- Write ratios as "3 to 1", reward first. Only leverage uses the "30:1" form. "N to 1" is for a plan; write a result as "N R" (5.5 R).
- Don't state market conventions as universal: some apps, especially in China and Japan, reverse the candle colours, so write "(usually green)" or "(usually red)" when a colour means up or down. Name the market when a rule is not universal (US, UK, EU).
- Keep the shared examples in US dollars. When a page mentions tax, a regulator, a compensation scheme, a product's availability or trading hours, give the EU version too, and the Czech one where it differs (ČNB, the Czech tax rules). Give times in the exchange's local time, plus CET for exchanges outside Europe (write "CET", also in lessons; trading-hours explains CEST). Give a dated fact (a rate, a ban's start, a tax year's figure) with its date only on the owner page; other pages say "as of 2026" or leave the date out. The reader's money is often CZK or EUR, so where a dollar result would differ for them, say so and link currency-risk.
- Describe CFDs as "common in the EU and UK but not offered to private traders in the US", not as "outside the US", so the EU is not framed as the exception.
- Write cents as numerals: "1 cent", "40 cents", not "$0.10".
- End a concept with a "Watch out" section and a linked "Next, see …" line. The Next line should name at least one written page, unless a planned page is clearly the right next step.
- A concept body is usually 300–500 words (each link counted as its display text, tables left out, since they hold numbers the prose already walks through). 500 is a ceiling, to keep pages short; 300 is only a guide. A shorter page that explains its concept fully is fine, so never pad one to reach the count. Count with `uv run python scripts/build.py --words <slug>`; that count is the one that decides.
- Acronym titles need no link text: write `[[atr]]`, not `[[atr|ATR]]`.
- Catalog titles and summaries that contain a comma must be quoted; the build rejects them otherwise.
- Adding a concept starts in `catalog.yaml` (slug, title, summary). Writing it means adding `content/concepts/<group>/<slug>.md` (body only, no frontmatter) and `banners/<slug>.svg`.
- Lessons need frontmatter `title`, `summary`, `added` (date) and `builds_on` (concept slugs; list every concept a step builds on, and link each one in the body so it gets the backlink). An optional `step` (a whole number) puts the lesson on the reading path; its closing line should point to the next step.
- Banners: `viewBox="0 0 1200 400"`, colours only through `--banner-bg/fg/up/down/accent` with fallbacks, no `id` attributes. Each one should show at a glance what the page explains.

## Where things go

- Site sources (catalog, content, banners, templates, static assets) live at the repository root; Python scripts go in `scripts/`, their tests in `tests/`, and the built site in `dist/` (not committed).

## Testing

<!-- What gets tested and how; test layout and naming. -->
