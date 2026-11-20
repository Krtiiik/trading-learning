---
title: "The bootstrap p-value of a Sharpe difference moves with the block length and the seed, so a p-value near a threshold is a range, not a number"
kind: pitfall
area: statistics
source: "Skeptic review of H1001 on 2026-11-19: `stats.block_bootstrap_difference` re-run on the registered train return series with other seeds, 20,000 draws and block lengths set by hand, and a stationary bootstrap written separately; the table is in the 'Skeptic review' section of research/hypotheses/H1001-trend-filter-on-daily-bars.md"
trust: medium
date: 2026-11-19
---

`evaluate_strategy` takes its p-value from a paired circular block bootstrap with 2,000 draws, the hypothesis's seed, and a block length chosen automatically (Politis-White on the difference of the two return series). For H1001's train run that gave 0.044 with a block of 9 bars. Re-running the same test on the same series, the p-value stayed below 0.10 in every variant but crossed 0.05 in both directions: other seeds alone move it visibly, independent days (block 1) give the largest p-value, and longer blocks give steadily smaller ones. The automatic block is also unstable: for return series that differ only by one day of lookback it came out more than twice as long for some as for others, and the p-value moved with it.

What to do. Read a recorded p-value near a threshold as a range (the review's table shows how wide it was for H1001), and say so in the verdict. A Skeptic should re-run the test with several seeds and with blocks of 1, about 20 and about 60 bars and report the spread next to the recorded value; `block_bootstrap_difference` takes `block` and `seed`. Nothing here is a reason to change the registered test of a hypothesis that has run, and the claim ladder's 10% gate was never in doubt for H1001.

Update 2026-11-19, before any Phase 2 run: the automatic choice was replaced by a rule. The block length is now the cube root of the number of observations (11 bars for H1001's 1,280 train days, 32 for 30,000 hourly bars), the same for every hypothesis on the same window; run records from `harness_version` 3 on use it. H1001's two records (version 1) used the automatic block and were not re-run. The p-value still moves with the seed and would move with another block: reading it as a range still applies.

Not established: which block length is right (the simulations in `tests/test_stats.py` validate the tool at one setting, not the automatic choice on fat-tailed crypto returns), and whether longer blocks lower the p-value for other rules; this is one hypothesis on one window.
