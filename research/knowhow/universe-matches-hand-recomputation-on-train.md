---
title: "The stored point-in-time universe equals an independent recomputation at all 63 train reconstitutions and never reads the bar of its own date"
kind: fact
area: data
source: "Data steward check on 2026-11-18: binance/spot/1d id 2d6763395242, binance/universe id 88f9a7cf72c7 (`uv run trading verify --quality`: both ok)"
trust: high
date: 2026-11-18
---

Recomputed without `build_universe`: a plain loop over the per-symbol daily bars, summing `quote_volume` over the 30 bars labelled D-30 to D-1, requiring a bar on each of those days, dropping pairs for which `exclusion(symbol)` is not None, taking the top 40, tier 1 for BTC and ETH, tier 2 for the next ten. For 2021-06-01 (bars 2021-05-02 to 2021-05-31) and for every other reconstitution from 2017-10-01 to 2022-12-01 the stored table has the same symbols, the same order and the same tiers: 63 of 63, lookback volumes equal to 8e-16 relative.

Timing, measured three ways:

- `build_universe` fed only bars labelled before D reproduces the stored rows dated D at 63 of 63 reconstitutions.
- Scrambling the bars of 2021-06-01 (volume times a random 0 to 1000, close times 0.01 to 100), or dropping them, leaves the rows dated 2021-06-01 identical; scrambling 2021-05-31 changes them (control).
- The check can fail: a window ending on D instead of D-1 gives another member set at 19 and another order at 49 of the 63 reconstitutions (at 2021-06-01 RUNE would replace TLM and 13 ranks would move).

What research receives is the same thing: in `load_market("1d", 2022-12-31)` the `member` row of each of the 1,963 labels equals the latest reconstitution dated at or before the label, `member_next` at 2021-05-31 is the June set, and the cached panels equal the Store's bars in every cell (open, high, low, close, quote volume; 183 coins).

The volatility net decided nothing on train (the recomputation has no net and still matches); the calmest member-month has a daily return standard deviation of 1.2% (BTC, March 2019) against a threshold of 0.5%. The table itself is well formed over the whole history: 110 reconstitutions, each on the 1st, consecutive months, ranks 1 to n, no duplicate rows, never more than 40.

Not established: anything value-level after 2022-12-31, and that the 182 member bases are all ordinary coins (none is on the exclusion list and none reads as pegged or leveraged, which is a reading of names, not a measurement).
