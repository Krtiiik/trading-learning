---
title: "A trading claim whose true Sharpe difference is 0.25 becomes a candidate one time in four and supported one time in nine, and a candidate's train estimate averages 0.7"
kind: lesson
area: statistics
source: "Simulation on 2026-11-18 (2 million normal draws per case, seed 1001) with the standard errors of H1001's two run records (0.38 on train from 2019-07, 0.485 on dev); H1001 itself is one instance"
trust: medium
date: 2026-11-18
---

Take a train estimate with standard error 0.38 and a dev estimate with 0.485, independent and normal around the same true effect, a candidate threshold of p at or below 0.10 (one registered literature hypothesis; more hypotheses make it stricter) and the default dev rule (at least half the train estimate and at least 0.2):

| True Sharpe difference | Becomes a candidate | Becomes supported | Mean train estimate of the candidates |
|---|---:|---:|---:|
| 0 | 10% | 2.5% | 0.67 |
| 0.25 | 27% | 11% | 0.72 |
| 0.5 | 51% | 30% | 0.79 |
| 0.75 | 76% | 55% | 0.91 |
| 1.0 | 91% | 75% | 1.07 |

Passing train needs an estimate of about 0.49, so a candidate's train estimate says little about the true size: it averages about 0.7 whether the truth is 0, 0.25 or 0.5. H1001 predicted 0.25, got 0.66 on train and 0.12 on dev, which is the typical path of a small or absent effect.

What to do. Quote a candidate's train estimate as "at least large enough to pass", never as the size of the effect. Expect "not replicated" for most true effects of the size the literature suggests for long-or-flat rules; it does not show the effect is absent. Because the dev rule asks for half of an inflated train estimate, a real effect of 0.25 fails dev more often than not; whether `min_ratio` 0.5 is the right default is a question for the owner, and it must not be changed for a hypothesis that has already run. Claims with a smaller standard error (predictive claims pooled across coins, or a benchmark more correlated with the strategy) are the ones the ladder can separate.

Not established: the table assumes normal, independent estimates with these two standard errors; it was not simulated through the bootstrap or on fat-tailed returns.
