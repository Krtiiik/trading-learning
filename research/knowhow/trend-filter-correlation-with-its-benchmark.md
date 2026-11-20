---
title: "For the minimum detectable effect of a per-coin long-or-flat filter against its equal-weight benchmark, a correlation of 0.75 matches what was measured"
kind: how-to
area: time-series
source: "Bootstrap standard errors in run records H1001-r01 (0.381 over 3.51 years) and H1001-r02 (0.485 over 2.00 years), put back into the formula behind `trading research mde sharpe-difference`"
trust: medium
date: 2026-11-18
---

`trading research mde sharpe-difference` needs the correlation between the strategy's and the benchmark's returns, which nobody knows before the run. For H1001 (each member's slot held or in cash, against the same slots always held) I assumed 0.7, reasoning that one slot switched on half the time gives 0.71 and forty slots switching at different times give more. The standard errors the block bootstrap then measured correspond to 0.75 on train and 0.76 on dev in the same formula (the formula assumes independent days, so this is a calibration, not a measured correlation).

So for a filter of this kind, invested a little under half the time, use `--correlation 0.75`: the minimum detectable effect is then 0.94 on train from 2019-07-01 and 1.24 on dev. A rule that is invested more of the time, or that moves in and out as one block, will differ; state the assumption and the reason in `power.note` as before.

Added by the Skeptic of H1001 on 2026-11-19: the correlation of the two daily return series themselves, measured on the train window (2019-07-01 to 2022-12-31, 1,280 bars, the registered strategy and benchmark), is 0.68. Put into the formula it gives a standard error of 0.43, above the 0.38 the block bootstrap recorded, so the bootstrap's blocks, not a higher correlation, are what brought the standard error down. Both numbers therefore have a use: 0.68 is the correlation, 0.75 is the value that makes the formula for independent days reproduce the bootstrap for this rule. The original assumption of 0.7 was right as a correlation.

Not established: the correlation on dev (the series cannot be loaded), and anything for rules other than H1001's.
