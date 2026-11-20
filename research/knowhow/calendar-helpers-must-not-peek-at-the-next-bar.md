---
title: "Deciding that a bar is the last of its week from the bar after it is look-ahead"
kind: pitfall
area: engine
source: "Caught by the harness's own look-ahead check on 2026-11-18, in the first version of rebalance_labels"
trust: high
date: 2026-11-18
---

The first `rebalance_labels` marked a bar as the week's last when the next bar in the data belonged to another week. On the full data that is right; with later bars removed, the final bar is never marked, so the panel's last row differs. The harness's truncation check refused the experiment.

The values were not wrong in any way that mattered to the test, but the same pattern in a signal would be: anything of the form "compare with the next row" uses the future. Decide period ends from the calendar (the bar's own close time falls in a new period), as the fixed helper does. More generally: when the look-ahead check fires, believe it.
