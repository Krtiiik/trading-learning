---
title: Resources
description: Primary sources behind the lessons, and the gaps still to fill.
permalink: /resources.html
---

# Algorithmic Trading Resources

## Knowledge

- [Yahoo Help: "What is the adjusted close?"](https://help.yahoo.com/kb/SLN28256.html)
  Primary source for how Yahoo builds `adj_close`: CRSP-style split and dividend multipliers with a worked example. Use for: anything about adjustment.
- [Ian Gow: "Yahoo returns" note](https://iangow.github.io/notes/published/yahoo-returns.pdf)
  Compares Yahoo returns with CRSP and describes Yahoo's two closes (split-adjusted `close`, split-and-dividend `adjusted`). Use for: data quality of free sources.
- [investor.gov: ex-dividend dates](https://www.investor.gov/introduction-investing/investing-basics/glossary/ex-dividend-dates-when-are-you-entitled-stock-and-cash-dividends)
  SEC investor-education page on ex-dividend and record dates. Use for: when a dividend lands in the bar data.
- [William F. Sharpe, "The Sharpe Ratio" (1994)](https://web.stanford.edu/~wfsharpe/art/sr/sr.htm)
  The author's own definition: excess return over a benchmark per unit of its volatility, ex ante vs ex post. Use for: Sharpe ratio, choosing a benchmark.
- [Andrew Lo, "The Statistics of Sharpe Ratios" (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf)
  Shows when √time annualization fails (serial correlation) and how to estimate Sharpe's error. Use for: annualizing, significance of backtest Sharpe ratios.
{: .links}

## Wisdom (Communities)

- Not yet proposed. Candidates to evaluate: r/algotrading, Quantitative Finance Stack Exchange (quant.stackexchange.com).

## Gaps

- A high-trust textbook for backtesting methodology (look-ahead, survivorship, overfitting).
- A primary source for drawdown and CAGR conventions (currently derived from first principles).
