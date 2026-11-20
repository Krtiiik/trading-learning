---
title: "A rule that decides every day drops one slot at each member's last bar, and run records written before commit b74ae59 add these up from the first bar of the data"
kind: pitfall
area: engine
source: "Run records H1001-r01 (train, dropped_weight 0.075) and H1001-r02 (dev, 0.125); the train figure taken apart with a scratch script on train data on 2026-11-18 (binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7)"
trust: high
date: 2026-11-18
---

`dropped_weight` in a run record is target weight that could not be bought because the coin had no bar at the next open. For H1001, which sets a target for every member at every close, the train figure of 0.075 is three slots of 1/40, one day each: ERDUSDT on 2020-09-01, NPXSUSDT on 2021-04-06 and BTTUSDT on 2022-01-18. Each is the day after the pair's last bar (see the note on members that stop trading): the signal was on at the final close, the next day had no bar, and the engine closed the position at that final close. Nothing was bought that could not be bought. The same daily schedule without a filter (the equal-weight universe re-equalised every bar) drops 0.32 over the train data.

Two things to know when reading the number. It is summed over the whole run, from the first bar of the data and not from the evaluation window, so a dev record contains the train drops as well (H1001: 0.125 on dev, of which 0.05 is new) and the dev part cannot be taken apart, because dev data cannot be loaded. And it grows with how often a rule decides: the monthly equal-weight benchmark drops 0.025 over train, a daily rule about one slot per member that stops trading while its signal is on.

What to do: if a hypothesis file names a level of `dropped_weight` that would make a run invalid, give it as a number and say what it counts ("more than N slots", or a share per decision). H1001 registered "more than a few percent of one day's portfolio in total", got 7.5%, and left its readers to argue about whether that is a few.

Added by the Skeptic of H1001 on 2026-11-19 (train data, same dataset ids):

- **The field changed meaning.** Since commit b74ae59 `dropped_weight` in a record is summed over the evaluation window only, and `dropped_weight_before_window` holds the rest. `harness_version` is 1 before and after, so a record does not say which meaning it carries: H1001-r01 and H1001-r02 are the only records with the old one. For H1001-r01 both meanings give 0.075, because the strategy dropped nothing before 2019-07-01; H1001-r02's 0.125 is cumulative from the first bar.
- **Confirmed by a second route.** A plain loop over the daily bars that shares no code with the engine counts the same three slots on the same three days (0.075), and 0.32 for the equal-weight universe re-equalised every bar.
- **Set the level from the benchmark, before registering.** Inside H1001's train window its own registered benchmark drops 0.175: seven members stop trading there and a fully invested daily rule holds a target on each at its last bar. So "a few percent in total" was a level no correct run of a daily rule on this universe could be sure to meet. The drops also change no return, since the engine sets such a target to zero, which is what a rule that knew would have done. Before naming a level of `dropped_weight` that voids a run, compute it for the benchmark on the same schedule (that needs no look at the rule's returns) and register a number above it.

Not established: what the two dev slots of H1001 were.
