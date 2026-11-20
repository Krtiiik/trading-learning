---
title: "A renamed coin drops out of the point-in-time universe for one to several months and its history starts again"
kind: pitfall
area: data
source: "Start and end months of symbols in the archive listing; which pairs are renames is from the model's memory and unverified"
trust: medium
date: 2026-11-18
---

When Binance renames a coin it ends one symbol and starts another: MATIC to POL (2024-09), RNDR to RENDER (2024-07), FTM to S (2025-01), EOS to A (2025-05), MKR to SKY (2025-09), BTT to BTTC (2022-01), ERD to EGLD (2020-09), LEND to AAVE (2020-10), BCC to BCHABC to BCH (2018-11, 2019-11), and others. Some are also redenominated at the swap (BTT 1:1000, ERD 1000:1, LEND 100:1, MKR 1:24000).

The Store treats the two symbols as two coins. The new one needs 30 daily bars before it can rank, so the coin is missing from the universe for at least one reconstitution (measured below), and a held position in the old symbol is sold at its last close by the engine. This affects a few coin-months and biases nothing in a known direction, but a strategy's turnover around a rename is overstated. Stitching renames into one history (a lineage table with ratios) is possible and not done; it would need each swap's terms from a reliable source.

Measured by the Data steward on 2026-11-18 for the renames that hit a train member (binance/universe id 88f9a7cf72c7; the dates are measured, the pairing of old and new symbol is still from memory):

| Old pair (rank in its last month) | Last bar | New pair | First bar | Reconstitutions without either |
|---|---|---|---|---|
| BCCUSDT (5) | 2018-11-20 | BCHABCUSDT, BCHSVUSDT | 2018-11-16 | 1 (2018-12) |
| BCHABCUSDT (5) | 2019-11-28 | BCHUSDT | 2019-11-28 | 1 (2019-12) |
| ERDUSDT (38) | 2020-08-31 | EGLDUSDT | 2020-09-03 | 3 (2020-10 to 2020-12), after a September in which ERD is a member without bars |
| LENDUSDT (22) | 2020-10-12 | AAVEUSDT | 2020-10-15 | 1 (2020-11) |
| NPXSUSDT (29) | 2021-04-05 | PUNDIXUSDT | 2021-04-09 | never a member again on train |
| BTTUSDT (29) | 2022-01-17 | BTTCUSDT | 2022-01-25 | never a member again on train |

So it is one month when the new pair ranks at once, and longer or for good when it does not; twice the coin was the fifth most traded. LUNAUSDT-2022 (rank 5, last bar 2022-05-13) is not a rename, but the same thing happens: the new LUNAUSDT joins in 2022-07 and LUNCUSDT in 2022-11. The other cost is to lookbacks: the new pair has no bars before its first, so a signal that needs more history than it has is undefined for a coin that has in fact traded for years (see the note on short histories).
