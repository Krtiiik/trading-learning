---
number: 3
title: The adjusted close rewrites the past, and what survives
short: Adjusted close rewrites the past
part: market-data
subtitle: "After this lesson you can tell which numbers in a backtest stay the same when Yahoo rewrites its history, and which ones change."
delivered: 2026-11-17
# Computed from the learner's stored SPY bars (download date simulated by
# multiplying only the dividends known by then).
asof:
  caption: "SPY's first bar, as downloaded on"
  columns: ["downloaded on", "adj_close of 1993-01-29", "factor", "SPY total return in 2000"]
  numeric: [2, 3, 4]
  ticks: ["1993", "2000", "2008", "2016", "2025", "2026"]
  rows:
    - ["1993-12-31", "42.86", "0.9755", "not yet known"]
    - ["2000-12-31", "38.08", "0.8667", "−8.85%"]
    - ["2008-12-31", "33.06", "0.7524", "−8.85%"]
    - ["2016-12-31", "28.00", "0.6373", "−8.85%"]
    - ["2025-12-31", "24.24", "0.5517", "−8.85%"]
    - ["2026-11-16", "24.05", "0.5474", "−8.85%"]
---

[Lesson 1](bars-and-adjusted-close.html) ended on this claim: SPY's first bar (29 January 1993) traded at 43.94 but has an adjusted close of 24.05, a factor of 0.547. Here is where that number comes from, and why it matters for anything you build on `adj_close`.

## Factors stack by multiplication

Each dividend multiplies *all* earlier prices by its own multiplier, $$1 - D / \text{previous close}$$. A bar therefore carries the product of the multipliers of every dividend that came *after* it:

$$\text{factor}(t) = \prod_{\text{ex-dates after } t} \left(1 - \frac{D}{\text{previous close}}\right)$$

SPY has had 136 dividends since March 1993. Multiply their 136 multipliers together and you get 0.547449. Yahoo's stored factor for the first bar is 0.547449. Rebuilt this way, the factor matches Yahoo's on every one of your 8,508 SPY bars to within 0.0000007. There is nothing more to it than this product.

{% include note.html content="SPY has never split. For a symbol that has, the split multipliers (1 / ratio) join the product in `adj_close`, but Yahoo already applies them to `close` too, so they cancel out of `adj_close / close`." %}

Each multiplier is about 0.995, one quarter's dividend yield. Stack them up and you get a steady drag: 0.547 spread over 33.8 years is **−1.77% a year**, which is roughly SPY's average dividend yield. The factor is, in effect, the record of every dividend paid since that bar.

## The same old bar, downloaded on different dates

Because each new dividend adds a multiplier, the adjusted close of a bar depends on *when you downloaded it*. Here is SPY's first bar as each download date would have shown it:

{% include slider-table.html id="asof" data=page.asof %}

Drag the slider. The adjusted close and the factor move every time; once the year 2000 is in the data, its return never does. That is the whole lesson in one table.

{% include key.html content="**Adjustment rescales, it never reshapes.** A new dividend multiplies every earlier price by the same number, so the *ratio* between any two earlier prices is unchanged. Returns are ratios. SPY's total return for 2000 is −8.85% whether you downloaded in December 2000 or today, even though the adjusted prices it is computed from fell from 143.92 → 131.19 to 90.91 → 82.86." %}

{% include note.html content="The raw close return for 2000 was −9.80%. The 0.95-point difference is the dividends SPY paid that year." %}

## What this means for your research

### Safe on `adj_close`: anything built from ratios

Returns, CAGR, volatility, Sharpe, drawdowns, “price above its 200-day average”, momentum (“12-month return > 0”). Multiply every price by the same constant and none of these change. That is why all of [lesson 2](the-stats-table.html) uses `adj_close`.

### Unsafe on `adj_close`: anything in dollars

“Buy when SPY is below $30”, a stop-loss at $X, an indicator measured in dollars (a dollar ATR, MACD in price units), and the number of shares you can afford. On adjusted data SPY sits below $30 on **570** days; its raw close was never below $30. A rule like that would fire in a backtest on days when nobody could ever have traded at that price, and it would fire on different days depending on when you downloaded.

### Your stored copy goes stale

Your Parquet files are a snapshot taken on one download date. After SPY's next ex-date, every stored `adj_close` before it is off by the new multiplier. Returns *inside* the stored history are still right, but if you just appended new bars, the return across the old/new boundary would be wrong by about one dividend. That is why `trading fetch` compares the adjustment factor on the last stored bar and re-downloads the whole history when it has changed.

{% capture body %}
A bar's factor collects multipliers from events after it. Bars since SPY's latest ex-date (18 September 2026) have no events after them, so their factor is exactly 1 and their adjusted close equals their close. Lesson 1 called this “the most recent price is always unadjusted”; more precisely, every bar since the latest ex-date is. The next dividend will push all of them below 1 too.
{% endcapture %}{% include reveal.html summary="Why only the most recent bars have factor 1" content=body %}

## Practice

Answer from memory, without scrolling up.
{: .practice-intro}

{% include numeric.html answer="48.51" tol="0.01"
   q="A bar closed at 50.00. Two dividends came later, with multipliers 0.99 and 0.98. What is its adjusted close today?"
   explain="The factor is the product 0.99 × 0.98 = 0.9702, and 50.00 × 0.9702 = **48.51**. Multipliers stack by multiplication, not addition." %}

{% include quiz.html answer="c"
   q="You re-download SPY after a new dividend and rerun a backtest. Which signal can now fire on different days?"
   a="Price closes above its own 200-day average"
   b="Daily return falls below minus three percent"
   c="Price drops below a fixed $500 level"
   d="Twelve-month return turns negative after being positive"
   explain="Only the fixed dollar level depends on the scale of the prices. The others compare prices with other prices, so a uniform rescaling cancels out." %}

{% include quiz.html answer="b"
   q="A new dividend goes ex today. What happens to the return between two bars from 2010?"
   a="It shrinks by the new dividend's yield"
   b="It stays exactly the same as before"
   c="It grows by the new dividend's yield"
   d="It becomes undefined until you download again"
   explain="Both 2010 bars are multiplied by the same new multiplier, so their ratio, and therefore the return, does not change." %}

{% include numeric.html answer="0.817" tol="0.004"
   q="A fund yields a steady 2% a year. Roughly what factor does a bar from 10 years ago carry? (three decimals)"
   explain="About 0.98 per year, stacked ten times: $$0.98^{10} \approx$$ **0.817**. The same reasoning turns SPY's 0.547 into a 1.77% average yield over 33.8 years." %}

{% capture answer %}
Smaller: 0.433 for TLT's first bar (July 2002), against SPY's 0.547 from 1993. TLT has nine fewer years of history but yields more, about 3.4% a year against SPY's 1.8%, and the yield wins.
{% endcapture %}
{% capture body %}
```
from trading.data import load_bars
b = load_bars("SPY")
mult = (1 - b.dividends / b.close.shift()).where(b.dividends > 0, 1.0)
factor = mult[::-1].cumprod()[::-1].shift(-1).fillna(1.0)   # product of later multipliers
(factor - b.adj_close / b.close).abs().max()                 # ≈ 0: Yahoo's factor, rebuilt
```

Then pick another symbol, say TLT, which pays monthly. Predict before running: does its first bar carry a bigger or smaller factor than SPY's?

{% include reveal.html summary="Answer" content=answer %}
{% endcapture %}{% include reveal.html summary="Try it on your own data" content=body %}

{% include ask.html text="Questions? For example: how to build fully adjusted OHLC from these factors, or how a backtest should use raw prices for fills. Ask Claude in the chat." %}
