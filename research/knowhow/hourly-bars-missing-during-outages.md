---
title: "Hourly bars are missing for every coin during exchange outages"
kind: fact
area: data
source: "Hourly train market (to 2022-12-31), dataset binance/spot/1h id a7d21dafe920"
trust: high
date: 2026-11-18
---

The hourly panel's index is the union of bar labels that exist, so an outage is a jump in the index, not a row of NaN. In train there are 26 such jumps, most of 2 to 11 hours (maintenance in 2018 to 2021); the longest runs from 2018-02-08 00:00 to 2018-02-11 04:00 (the outage plus the dropped off-grid bars). Individual coins also miss single hours.

What this means: a "24-bar" lookback is not always 24 hours; use the index when the time span matters. The engine prices a coin without a bar at its last close and returns span the gap correctly. In train 0.3% of all hours are missing, so annualising with 8,760 bars a year overstates the count by that much. Daily bars have no gaps for BTC and ETH.
