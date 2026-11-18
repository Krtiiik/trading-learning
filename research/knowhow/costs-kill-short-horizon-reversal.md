---
title: "Trading costs can turn a short-horizon reversal edge into a loss"
kind: lesson
area: everyone
source: "ETF scout: research/REPORT.md and LOG.md on branch claude/daily-rebalance-etf-research-495a46 (one night, 25 US ETFs, daily bars, 2005-2024), experiment E01"
trust: medium
date: 2026-11-18
---

On ETFs a 5-day cross-sectional reversal had Sharpe 0.82 at zero cost, 0.37 at 5 bps per side and 0.24 with a one-bar later fill; it traded 90 times the account a year and paid 3.6 times the account in costs over 20 years.

What carries over to crypto is the arithmetic, not the conclusion: our costs are 12 to 25 bps per side, so a rule that turns the portfolio over once a day needs roughly 0.25% to 0.5% of gross edge per day just to break even. Whether crypto reversal survives that is an open hypothesis. Before registering any high-turnover rule, estimate turnover times cost and compare it with the predicted gross effect; the run record's `turnover_per_year` and `cost_per_year` show it afterwards.
