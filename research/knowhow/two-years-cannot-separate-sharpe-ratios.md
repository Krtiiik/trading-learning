---
title: "Two years of data cannot separate a Sharpe ratio of 0.5 from 1.0"
kind: fact
area: statistics
source: "ETF scout holdout; formula checked against simulation in tests/test_stats.py (test_sharpe_standard_errors_match_simulation)"
trust: high
date: 2026-11-18
---

The standard error of an annualised Sharpe ratio is about sqrt(1 / years): 0.71 over two years. Our dev segment is two years (2023-2024), so a single strategy's dev Sharpe is known to within roughly plus or minus 1.4 at 95%.

Differences against a correlated benchmark are tighter: sqrt(2 (1 - correlation) / years), which is 0.45 at correlation 0.8. Even so, the smallest Sharpe difference dev detects with 80% power at one-sided 5% is about 1.1 (`uv run trading research mde sharpe-difference --correlation 0.8`). So dev can confirm sign and rough size, not significance, for most trading claims; that is why the proposed dev rule asks for sign and size rather than a p-value. Predictive claims pooled across 40 coins have far more observations and are the better-powered kind of hypothesis.
