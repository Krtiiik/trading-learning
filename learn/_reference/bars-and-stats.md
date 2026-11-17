---
title: Bars, adjustment and performance statistics
short: Bars and stats
subtitle: "Terms follow the project glossary (`.claude/CONTEXT.md`). Taught in lessons [1](../lessons/bars-and-adjusted-close.html), [2](../lessons/the-stats-table.html) and [3](../lessons/adjusted-close-rewrites-the-past.html)."
description: Bar columns, how the adjusted close is built, and the five performance statistics.
---

## Bar columns

{% capture rows %}
| column | meaning | adjusted for |
|---|---|---|
| `open` `high` `low` `close` | First, highest, lowest and closing trade of the session | splits only (Yahoo) |
| `adj_close` | Close scaled so its changes are total returns | splits and dividends |
| `volume` | Shares traded in the session | not yet verified |
| `dividends` | Cash per share, on the ex-dividend date; 0 otherwise | — |
| `splits` | Split ratio on the split date (2.0 = 2-for-1); **0** otherwise | — |
{% endcapture %}{% include table.html content=rows %}

<div class="cards" markdown="1">

<div class="card" markdown="1">

## Adjustment (CRSP method)

Each event multiplies every price *before* it; prices on and after are untouched.

$$\text{dividend: } \times \left(1 - \frac{D}{\text{previous close}}\right) \qquad \text{split: } \times \frac{1}{\text{ratio}}$$

**Adjustment factor** = `adj_close / close`. It is 1 after the latest dividend and steps down going back in time. A change on an already stored bar means history was re-adjusted.

**Total return on a day** = (close + dividend) / previous close − 1 = `adj_close.pct_change()`.

Source: [Yahoo, “What is the adjusted close?”](https://help.yahoo.com/kb/SLN28256.html)
{: .source}

</div>

<div class="card" markdown="1">

## Levels vs returns

A bar's factor is the product of all later multipliers, so it shrinks with every new event (SPY 1993: 0.547 ≈ 1.8% a year of dividends).

New events rescale all earlier prices uniformly: **ratios survive, dollar levels do not.**

- Safe on `adj_close`: returns, CAGR, volatility, Sharpe, drawdown, moving-average crossovers, momentum.
- Unsafe: fixed price thresholds, stops, dollar indicators (ATR, MACD), share counts. Use raw prices.
- A stored copy is stale after the next ex-date: re-download, don't append.

</div>

<div class="card" markdown="1">

## Notebook setup

```
prices  = load_panel(symbols).dropna()
returns = prices.pct_change().dropna()
years   = len(returns) / 252
```

`.dropna()` trims every symbol to the **common history**: statistics change with which symbols are picked.

252 = trading sessions per year.

</div>

</div>

## Performance statistics

{% capture rows %}
| name | formula (pandas) | answers | blind to |
|---|---|---|---|
| **CAGR** | `(P[-1] / P[0]) ** (1/years) - 1` | Constant yearly rate from start to end | the path in between |
| **Volatility** | `r.std() * sqrt(252)` | How bumpy, per year | direction; up and down count alike |
| **Sharpe (rf=0)** | `r.mean() / r.std() * sqrt(252)` | Return per unit of volatility | cash rate (set to 0); fat tails |
| **Max drawdown** | `(P / P.cummax() - 1).min()` | Worst fall from a running peak | how long it lasted; intraday lows |
| **Worst day** | `r.min()` | Largest one-session loss | everything else: one observation |
{% endcapture %}{% include table.html content=rows %}

<div class="cards" markdown="1">

<div class="card" markdown="1">

### Rules of thumb

- Volatility scales with $$\sqrt{\text{time}}$$ if days are independent ($$\sqrt{252} \approx 15.87$$).
- $$\text{Mean return} \approx \ln(1 + \text{CAGR}) + \text{volatility}^2 / 2$$: bumpiness drags compounding.
- Recovering from a drawdown $$d$$ needs a gain of $$1 / (1 + d) - 1$$: −50% needs +100%.
- Textbook Sharpe subtracts the risk-free rate from the mean; rf=0 overstates it.

</div>

<div class="card" markdown="1">

### Your data, 2004-11-18 to 2026-11-16

{% capture rows %}
|  | CAGR | Vol | Sharpe | MDD |
|---|---:|---:|---:|---:|
| SPY | 10.7% | 18.8% | 0.63 | −55% |
| TLT | 2.8% | 14.5% | 0.26 | −48% |
| GLD | 9.9% | 18.3% | 0.61 | −46% |
{% endcapture %}{% include table.html content=rows %}

Sources: [Sharpe (1994)](https://web.stanford.edu/~wfsharpe/art/sr/sr.htm), [Lo (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf) on $$\sqrt{\text{time}}$$.
{: .source}

</div>

</div>
