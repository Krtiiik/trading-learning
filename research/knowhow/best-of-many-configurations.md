---
title: "Picking the best of about thirty configurations explains an edge of about 0.2 Sharpe by itself"
kind: lesson
area: everyone
source: "ETF scout: research/REPORT.md and LOG.md on branch claude/daily-rebalance-etf-research-495a46 (one night, 25 US ETFs, daily bars, 2005-2024), 'Known risks and limits'"
trust: medium
date: 2026-11-18
---

The ETF scout evaluated 29 configurations on one window. Their Sharpe ratios spread with a standard deviation of about 0.25, so the best one sitting 0.2 above the passive benchmark is roughly what selection alone produces; its holdout Sharpe fell from 0.96 to 0.51.

This is why every hypothesis here is registered before it runs, has one primary test, and passes Benjamini-Hochberg across all registered hypotheses, and why a variant is a new hypothesis that counts in that total. The size of the selection effect (0.2) is specific to that sample; the mechanism is general.
