---
title: "The engine's net Sharpe ratios for a daily 40-coin rule equal those of an independent loop holding units and cash to 0.0003, and the gap is how costs are paid"
kind: fact
area: engine
source: "Skeptic review of H1001 on 2026-11-19: `evaluate_strategy` (run record H1001-r01) against a plain Python loop over the 1,963 train daily bars; binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-19
---

The loop holds a number of units of each coin and a USDT balance, decides at each close, takes the membership of the following day from `market.member`, fills at the next open, charges 12, 15 or 25 bps per side by the tier at the traded bar, values a coin without a bar at its last close, and computes the Sharpe ratio by hand. It shares with the library only the reading of the open, close, member and tier arrays. Over H1001's train window (2019-07-01 to 2022-12-31):

| | Engine | Loop |
|---|---:|---:|
| Strategy net Sharpe ratio | 0.99041 | 0.99072 |
| Benchmark (equal weight, every bar) net Sharpe ratio | 0.32928 | 0.32947 |
| Difference | 0.66113 | 0.66125 |
| Difference at double cost | 0.48204 | 0.48231 |
| Dropped weight, strategy / benchmark, all bars | 0.075 / 0.32 | 0.075 / 0.32 |

The one difference in method: the engine removes costs as a proportional cut of the whole portfolio (`returns = (1 + gross) * (1 - cost) - 1`), the loop pays them out of cash, so the loop's coin positions are a few basis points larger after each trade. That is worth 0.0001 to 0.0003 of Sharpe ratio here and grows with costs.

What to do: a Skeptic's second route for a trading claim can be this kind of loop (about 100 lines, 8 seconds for six runs); agreement to the third decimal is what to expect, and a gap in the second decimal means a difference in timing, membership or costs worth finding. The engine's fully invested portfolios pay costs without holding cash for them, which the loop shows as a cash balance a few basis points below zero; that is an approximation, not a leak.

Not established: agreement on hourly bars, with hold rows (weekly or monthly rebalancing), or for a rule that concentrates in few coins.
