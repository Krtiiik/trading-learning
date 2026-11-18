---
title: "A rule that decides every day drops one slot at each member's last bar, and `dropped_weight` adds these up from the first bar of the data"
kind: pitfall
area: engine
source: "Run records H1001-r01 (train, dropped_weight 0.075) and H1001-r02 (dev, 0.125); the train figure taken apart with a scratch script on train data on 2026-11-18 (binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7)"
trust: high
date: 2026-11-18
---

`dropped_weight` in a run record is target weight that could not be bought because the coin had no bar at the next open. For H1001, which sets a target for every member at every close, the train figure of 0.075 is three slots of 1/40, one day each: ERDUSDT on 2020-09-01, NPXSUSDT on 2021-04-06 and BTTUSDT on 2022-01-18. Each is the day after the pair's last bar (see the note on members that stop trading): the signal was on at the final close, the next day had no bar, and the engine closed the position at that final close. Nothing was bought that could not be bought. The same daily schedule without a filter (the equal-weight universe re-equalised every bar) drops 0.32 over the train data.

Two things to know when reading the number. It is summed over the whole run, from the first bar of the data and not from the evaluation window, so a dev record contains the train drops as well (H1001: 0.125 on dev, of which 0.05 is new) and the dev part cannot be taken apart, because dev data cannot be loaded. And it grows with how often a rule decides: the monthly equal-weight benchmark drops 0.025 over train, a daily rule about one slot per member that stops trading while its signal is on.

What to do: if a hypothesis file names a level of `dropped_weight` that would make a run invalid, give it as a number and say what it counts ("more than N slots", or a share per decision). H1001 registered "more than a few percent of one day's portfolio in total", got 7.5%, and left its readers to argue about whether that is a few.

Not established: what the two dev slots of H1001 were.
