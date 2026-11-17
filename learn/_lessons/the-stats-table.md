---
number: 2
title: "Five numbers: CAGR, volatility, Sharpe, drawdown, worst day"
short: The stats table
part: performance
subtitle: "After this lesson you can compute every number in the notebook's “Annualized statistics” table by hand, and say what each one hides."
delivered: 2026-11-17
---

All five come from the same two series in `notebooks/explore_bars.py`:

```
prices  = load_panel(picker.value).dropna()   # adj_close, one column per symbol
returns = prices.pct_change().dropna()        # daily total returns
```

Two details matter before any formula:

- **`.dropna()` keeps only dates where every picked symbol has data.** GLD starts in November 2004, so picking SPY together with GLD cuts SPY's 1993–2004 history away. The same symbol gets different statistics depending on its neighbours in the picker.
- **A year is 252 sessions**, the usual count of US trading days. The notebook converts sessions into years with `len(returns) / 252`.

The worked numbers below are from your store: SPY, TLT and GLD from 2004-11-18 to 2026-11-16, 5,533 sessions.

{% capture rows %}
|  | CAGR | Volatility | Sharpe (rf=0) | Max drawdown | Worst day |
|---|---:|---:|---:|---:|---:|
| SPY | 10.69% | 18.84% | 0.63 | −55.19% | −10.94% |
| TLT | 2.82% | 14.50% | 0.26 | −48.35% | −6.67% |
| GLD | 9.91% | 18.31% | 0.61 | −45.56% | −10.27% |
{% endcapture %}{% include table.html content=rows hl="1" %}

## 1 · CAGR: how fast did it grow?

**Compound annual growth rate**: the single constant yearly rate that would turn the starting price into the ending price over the same number of years.

$$\text{CAGR} = \left(\frac{P_\text{end}}{P_\text{start}}\right)^{1/\text{years}} - 1$$

It looks only at the two endpoints. A path that crashed 50% and recovered and a perfectly smooth path get the same CAGR. That is what the next numbers are for.

## 2 · Volatility: how bumpy was the ride?

The standard deviation of daily returns, scaled to a year:

$$\sigma_\text{annual} = \operatorname{std}(r_\text{daily}) \times \sqrt{252}$$

Why $$\sqrt{252}$$ and not 252? If daily returns are independent, their *variances* add up over a year: 252 days give 252× the variance, so the standard deviation grows by $$\sqrt{252} \approx 15.9$$. SPY's daily standard deviation is about 1.19%, so its annual volatility is about 18.8%.

{% include note.html content="The $$\sqrt{252}$$ rule assumes days are independent. When returns are autocorrelated it is wrong, sometimes badly; see [Lo, “The Statistics of Sharpe Ratios” (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf). For liquid ETFs it is a fine approximation." %}

Volatility counts upside moves as “risk” exactly like downside ones. It measures bumpiness, not loss.

## 3 · Sharpe ratio: return per unit of bumpiness

$$\text{Sharpe} = \frac{\operatorname{mean}(r_\text{daily})}{\operatorname{std}(r_\text{daily})} \times \sqrt{252}$$

This equals annualized mean return (mean × 252) divided by annualized volatility (std × $$\sqrt{252}$$). SPY: 11.94% / 18.84% ≈ 0.63. It lets you compare a calm asset with a wild one on one scale.

Sharpe's own definition, in [his 1994 paper](https://web.stanford.edu/~wfsharpe/art/sr/sr.htm), uses the return *in excess of a benchmark*, normally the risk-free rate (T-bills). The notebook sets that rate to zero (“rf=0”), which flatters every asset when cash pays something. Even a modest 2% cash rate pulls SPY's to (11.9 − 2) / 18.8 ≈ 0.53.

{% include note.html content="**Why is the 11.94% mean higher than the 10.69% CAGR?** Bumpiness costs compounding: lose 10% then gain 10% and you are at 0.99, not 1. The drag is about half the variance, $$0.188^2 / 2 \approx 1.8\%$$, exact when CAGR is written as a log rate: $$\ln(1.1069) = 10.2\% = 11.9\% - 1.8\%$$. That is why Sharpe uses the arithmetic mean but you should quote CAGR as “what you earned”." %}

## 4 · Max drawdown: the worst fall from a peak

The **drawdown** on any day is how far the price sits below the highest price seen so far:

$$\text{drawdown}_t = \frac{P_t}{\max_{s \le t} P_s} - 1 \qquad \text{max drawdown} = \min_t \, \text{drawdown}_t$$

In pandas that is `prices / prices.cummax() - 1`, and the table shows `.min()`. It is 0 at every new high and negative in between; the notebook's “Drawdown from previous peak” chart plots the whole series. SPY's −55.19% is the trough of 9 March 2009, measured from the October 2007 peak.

{% include key.html content="**Drawdowns are asymmetric.** After falling 55% you need +123% to get back to the peak (1 / 0.45 − 1). This is the number that tells you whether you could have stomached holding something." %}

Two limits: it uses daily closes, so the intraday lows were deeper; and it uses `adj_close`, so dividends received during the fall cushion it.

## 5 · Worst day

Simply `returns.min()`: the single largest one-session loss. SPY: −10.94% on 16 March 2020. GLD: −10.27% on 30 January 2026, the precious-metals crash the architecture notes mention. It is one observation, so it says little about what is likely, but a lot about what is possible.

## Practice

Do these without scrolling up. A calculator is fine; looking up the formula is not.
{: .practice-intro}

{% include numeric.html answer="0.0718" tol="0.0006" percent=true
   q="A fund goes from 100 to 200 in exactly 10 years. What is its CAGR? (percent, one decimal)"
   explain="$$(200 / 100)^{1/10} - 1 = 2^{0.1} - 1 \approx$$ **7.2%**. Not 10%: that would be the simple average, which ignores compounding." %}

{% include numeric.html answer="0.1587" tol="0.0015" percent=true
   q="Daily returns have a standard deviation of 1.0%. What is the annualized volatility? (percent)"
   explain="$$1.0\% \times \sqrt{252} \approx 1.0\% \times 15.87 =$$ **15.9%**. Variances add over independent days, so the standard deviation scales with the square root of time." %}

{% include numeric.html answer="-0.25" tol="0.002" percent=true
   q="Closing prices over five sessions: 100, 120, 90, 130, 104. What is the max drawdown? (percent, negative)"
   explain="Running maximum: 100, 120, 120, 130, 130. Drawdowns: 0, 0, −25%, 0, −20%. The minimum is **−25%** (120 → 90). The later fall from 130 to 104 is smaller." %}

{% include quiz.html answer="a"
   q="You add GLD to a picker that held only SPY. SPY's CAGR in the table changes. Why?"
   a="The common history now starts in late 2004"
   b="Volatility of the panel is shared across symbols"
   c="Prices are rescaled to the first common close"
   d="Annualization switches to a different day count"
   explain="`.dropna()` keeps only dates where every picked symbol has a price. GLD's first bar is 2004-11-18, so SPY loses 1993–2004 and its endpoints move." %}

{% include quiz.html answer="c"
   q="Two funds have the same CAGR. Fund A has twice the volatility of fund B. What follows?"
   a="Fund A had the deeper max drawdown, guaranteed"
   b="Fund A earned more money over the same period"
   c="Fund A has the lower Sharpe ratio, most likely"
   d="Fund A had the worse single day, guaranteed"
   explain="Same growth with more bumpiness means less return per unit of volatility. (Strictly, Sharpe uses the arithmetic mean, which is a bit higher for the bumpier fund, hence “most likely”.) Drawdown and worst day are path details that volatility does not pin down." %}

{% include numeric.html answer="1.0" tol="0.002" percent=true
   q="A position falls 50% from its peak. What gain from the trough gets it back to the peak? (percent)"
   explain="1 / 0.5 − 1 = **100%**. Losses and the gains needed to repair them are not symmetric." %}

{% capture body %}
```
import numpy as np
from trading.data import load_panel
prices = load_panel(["SPY"]).dropna()        # SPY alone: history from 1993
r = prices.pct_change().dropna()
years = len(r) / 252
(prices.iloc[-1] / prices.iloc[0]) ** (1 / years) - 1   # CAGR, compare with the table above
(prices / prices.cummax() - 1).idxmin()                  # date of the deepest drawdown
```

Before running it: predict whether SPY's CAGR since 1993 is higher or lower than the 10.69% it shows since 2004.
{% endcapture %}{% include reveal.html summary="Try it on your own data" content=body %}

{% include ask.html text="Questions, or curious about the next measures (Sortino, Calmar, rolling statistics, a real risk-free rate)? Ask Claude in the chat." %}
