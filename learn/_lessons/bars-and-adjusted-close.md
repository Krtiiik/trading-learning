---
number: 1
title: What is in a bar, and how the adjusted close is built
short: Bars and adjusted close
part: market-data
subtitle: "After this lesson you can read every column `trading fetch` stores, and compute an adjusted close by hand."
delivered: 2026-11-17
---

## One bar, eight columns

A **bar** is one trading session of one symbol. Here is a real one from your store, SPY on 18 September 2026, with the session before it:

{% capture rows %}
| date | open | high | low | close | adj_close | volume | dividends | splits |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-09-17 | 763.15 | 763.57 | 759.96 | 762.60 | 760.71 | 49,652,800 | 0 | 0 |
| 2026-09-18 | 761.31 | 762.00 | 757.97 | 761.69 | 761.69 | 65,395,100 | 1.889 | 0 |
{% endcapture %}{% include table.html content=rows hl="2" %}

- **open, high, low, close** (“OHLC”): the first trade, the highest and lowest trade, and the official closing price of the session.
- **volume**: how many shares changed hands that session.
- **dividends**: cash paid per share, recorded on the *ex-dividend date*, the first session where buying the share no longer gets you that payment. SPY pays quarterly; here $1.889.
- **splits**: the split ratio on that session (2.0 for a 2-for-1 split), and `0` on ordinary days. That zero is a Yahoo convention, not “ratio 0”.
- **adj_close**: the **adjusted close**, explained below.

{% include note.html content="Why record the dividend on the ex-date and not the pay date? Because that is the day the price drops by about the dividend: the share stops carrying the claim to it. [investor.gov on ex-dividend dates](https://www.investor.gov/introduction-investing/investing-basics/glossary/ex-dividend-dates-when-are-you-entitled-stock-and-cash-dividends)." %}

## The problem the adjusted close solves

On 18 September the close went from 762.60 to 761.69, a raw change of **−0.12%**. Yet nobody holding SPY lost money that day: each share also produced $1.889 of cash. Counting it:

$$\frac{761.69 + 1.889}{762.60} - 1 = +0.13\%$$

That +0.13% is the **total return**: price change plus distributions. If you backtested on raw closes, every ex-date would look like a small loss, and over 30 years the missing dividends add up to a large part of SPY's return. The adjusted close is a single price series whose day-to-day changes *are* total returns, so `adj_close.pct_change()` gives you them directly.

## How it is actually adjusted

Yahoo follows the [CRSP method](https://help.yahoo.com/kb/SLN28256.html): it never changes the price on or after an event; it multiplies every price *before* the event by a factor.

$$\begin{aligned} \text{dividend multiplier} &= 1 - \frac{\text{dividend}}{\text{previous close}} \\ \text{split multiplier} &= \frac{1}{\text{split ratio}} \end{aligned}$$

For the bar above: 1 − 1.889 / 762.60 = **0.997523**. Every adjusted close before 18 September is multiplied by that number. Check it against your data: 762.60 × 0.997523 = 760.71, exactly the stored `adj_close` of 17 September.

Why multiply instead of subtracting the dividend? Multiplying keeps every daily *percentage* change intact, which is what returns are made of. Subtracting would distort old returns and could even make very old prices negative.

{% include key.html content="**The adjusted close rewrites the past.** Each new dividend or split multiplies the entire history before it by another factor. The most recent price is always unadjusted, and the further back you go the more factors stack up. SPY's first bar (January 1993) traded at 43.94 but has an adjusted close of 24.05: 33 years of dividends compounded into a factor of 0.547. [Lesson 3](adjusted-close-rewrites-the-past.html) takes this apart." %}

This is why the project tracks the **adjustment factor**, `adj_close / close`. In the table it is 0.997523 on 17 September and exactly 1 from 18 September on, because no dividend has happened since. When the next dividend arrives, Yahoo multiplies all of history again and the factor on already-stored bars changes. `trading fetch` notices that change and re-downloads the symbol in full, since your stored adjusted closes would otherwise be stale.

## A caveat: Yahoo's “close” is not quite raw

The project calls `close` the **raw price**, and it is easy to read that as “exactly what traded”. Your own data says otherwise for splits. QQQ split 2-for-1 on 20 March 2000. A truly raw close would halve that day. In your store:

{% capture rows %}
| date | close | splits |
|---|---:|---:|
| 2000-03-17 | 110.81 | 0 |
| 2000-03-20 | 107.69 | 2.0 |
{% endcapture %}{% include table.html content=rows hl="2" %}

No halving: the pre-split closes have already been divided by 2. XLK (2-for-1, December 2025) and SLV (10-for-1, July 2008) show the same thing. Yahoo's `close` is *split-adjusted but not dividend-adjusted*; only `adj_close` adjusts for both. [Ian Gow's note on Yahoo returns](https://iangow.github.io/notes/published/yahoo-returns.pdf) describes the two series the same way. In practice: returns from `adj_close` are right, but a pre-split `close` is not the price you would have paid.

One consequence: a split scales `close` and `adj_close` alike, so the adjustment factor does not change. `trading fetch` therefore also watches the `splits` column and re-downloads in full when a new split appears; finding that gap is how this lesson was written.

{% include note.html content="Read the [Yahoo help page](https://help.yahoo.com/kb/SLN28256.html) worked example: a 2:1 split and a $0.08 dividend, with every multiplier shown. It is short and it is the primary source for this lesson." %}

## Practice

Answer from memory first; scroll up only after you have committed to an answer.
{: .practice-intro}

{% include quiz.html answer="c"
   q="On an ex-dividend date the raw close falls slightly. What does the adjusted close do on that same day?"
   a="It falls by exactly the dividend amount paid"
   b="It stays flat until the dividend is paid"
   c="It moves by the total return that day"
   d="It moves by the raw price change only"
   explain="The adjusted close changes by (close + dividend) / previous close − 1: the price move plus the cash. For SPY on 2026-09-18 that was +0.13% while the raw close fell 0.12%." %}

{% include numeric.html answer="0.9976" tol="0.00006"
   q="A fund closes at 250.00. The next session is its ex-date for a $0.60 dividend. What multiplier is applied to every earlier adjusted close? (four decimals)"
   explain="1 − 0.60 / 250.00 = 1 − 0.0024 = **0.9976**. The previous close is the denominator, because that is the price the dividend is taken out of." %}

{% include quiz.html answer="b"
   q="You stored SPY last month. Today a new dividend went ex. What happened to the stored history at Yahoo?"
   a="Only today's bar received a new adjusted close"
   b="Every earlier adjusted close was multiplied by a factor"
   c="Every earlier raw close was cut by dividends"
   d="Nothing changed until the next quarterly data rebuild"
   explain="Adjustments go backwards in time: all prices before the event get the new multiplier. That is why `trading fetch` compares the adjustment factor on the last stored bar and re-downloads in full when it changed." %}

{% include numeric.html answer="0.5" tol="0.0001"
   q="A share splits 2-for-1. By what number are the pre-split adjusted closes multiplied?"
   explain="The split multiplier is 1 / ratio = 1 / 2 = **0.5**. One old share became two new ones, each worth half, so old prices are halved to be comparable. (Yahoo applies the same to `close`, as the QQQ table shows.)" %}

{% include quiz.html answer="d"
   q="Which column should a backtest use to compute daily returns?"
   a="close, because it is the traded price"
   b="open, because orders fill at next open"
   c="close plus dividends column, summed over history"
   d="adj_close, because its changes are total returns"
   explain="Returns come from `adj_close`. Raw prices are for sizing orders and simulating fills, which comes later." %}

{% capture body %}
```
from trading.data import load_bars
spy = load_bars("SPY")
spy["factor"] = spy.adj_close / spy.close
spy[spy.dividends > 0].tail(4)          # recent ex-dates
spy.loc["2026-09-10":"2026-09-25", ["close", "adj_close", "dividends", "factor"]]
```

Watch the factor step up to the next value on each ex-date and reach 1.0 after the latest one.
{% endcapture %}{% include reveal.html summary="Try it on your own data" content=body %}

{% include ask.html text="Something unclear, or want to go deeper (dividend-adjusted OHLC, capital-gain distributions, why ETFs rarely split)? Ask Claude in the chat." %}
