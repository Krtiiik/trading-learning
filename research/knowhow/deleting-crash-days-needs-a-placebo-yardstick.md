---
title: "Deleting the benchmark's worst days lowers the Sharpe difference of any half-invested rule, so judge a rule's dependence on crash days against a placebo's"
kind: how-to
area: statistics
source: "Skeptic review of H1001 on 2026-11-19, train data only: the registered strategy and benchmark return series with the benchmark's worst bars removed, against 300 copies of the rule with its signal rolled in time; the figures are in check 4 of the 'Skeptic review' section of research/hypotheses/H1001-trend-filter-on-daily-bars.md"
trust: medium
date: 2026-11-19
---

A natural attack on a long-or-flat rule is to remove the handful of days on which the benchmark crashed and see whether the Sharpe difference survives. It always falls, and not only for a rule with skill: a portfolio that is in cash half the time misses about half of every crash by arithmetic, and a crash day removed helps the fully invested benchmark's Sharpe ratio more than the half-invested rule's. Removing instead the days with the largest difference between rule and benchmark is worse, because it selects on the outcome and lowers any estimate by construction.

What to do. Choose the days from the benchmark's returns, never from the difference. Then make the same deletion for a placebo with the same on-off pattern at the wrong time (`stats.circular_shift_test`, or the loop it runs) and compare the two falls, and compare the rule's exposure on those days with its average exposure. Report three numbers together: the estimate without the days, the placebo's average fall, and how invested the rule was on those days. For H1001 on train the rule's fall was larger than the average placebo's but inside the placebo's range, which is "concentrated in a few days", not "an artefact of a few days". A result like that is what a large bootstrap standard error already says in another form: a rule whose gain is in risk has as many independent observations as the window has crashes.

Not established: a threshold for "too concentrated"; this was one rule on one window.
