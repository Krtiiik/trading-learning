---
title: "A coin joins the point-in-time universe with a median of 53 days of history, so a long lookback has no signal for many member-months"
kind: pitfall
area: data
source: "Data steward check on 2026-11-18, train reconstitutions only: binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-18
---

Membership needs 30 daily bars and nothing more, and new listings often rank at once. History is counted as days from a pair's first bar to the 1st of the month of membership:

| Member-months with history shorter than | 60 days | 90 days | 180 days | 365 days |
|---|---|---|---|---|
| All train (1,980 member-months) | 5.2% | 10.3% | 21.7% | 40.6% |
| From 2019-07, when the universe has 40 members (1,680) | 3.7% | 7.7% | 17.1% | 32.9% |

In its first month as a member a coin has a median of 53 days of history; 103 of the 183 train members enter with fewer than 60 days and 158 with fewer than a year. Membership is also short: the median coin is a member at 4 train reconstitutions, 83 of 183 at three or fewer, and only 8 at all 42 from 2019-07 on. A renamed coin counts as a new pair and starts again from nothing (BCH on 2020-01-01 has 34 days of history).

What to do: a hypothesis with a lookback must say, before it runs, what the rule does when the lookback is not full (flat is the natural choice for a long-or-flat rule) and should count the member-months that removes, because the equal-weight benchmark holds those coins anyway. The market panels carry a coin's bars from before it was a member, so a lookback may reach back past the month it joined.

Not established: anything about returns of newly listed coins; this is a count of available bars.
