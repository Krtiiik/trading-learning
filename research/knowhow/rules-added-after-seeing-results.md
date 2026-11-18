---
title: "A rule added after seeing where the previous one failed did not hold out of sample"
kind: lesson
area: process
source: "ETF scout: research/REPORT.md and LOG.md on branch claude/daily-rebalance-etf-research-495a46 (one night, 25 US ETFs, daily bars, 2005-2024), experiments E09 and E13 and the holdout"
trust: medium
date: 2026-11-18
---

The scout's leading rule (a volatility cap) failed a pre-registered check on an untouched decade. A trend switch was then added because it repaired exactly that decade; on the holdout the repaired rule did worse than the rule it repaired. One instance, so medium trust, but it is the textbook way overfitting happens.

Here: if a hypothesis fails, it stays failed. A repair is a new hypothesis with origin `exploration` (it came from looking at results), so only its dev run counts.
