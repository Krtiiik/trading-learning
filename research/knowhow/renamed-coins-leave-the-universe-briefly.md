---
title: "A renamed coin drops out of the point-in-time universe for one or two months"
kind: pitfall
area: data
source: "Start and end months of symbols in the archive listing; which pairs are renames is from the model's memory and unverified"
trust: medium
date: 2026-11-18
---

When Binance renames a coin it ends one symbol and starts another: MATIC to POL (2024-09), RNDR to RENDER (2024-07), FTM to S (2025-01), EOS to A (2025-05), MKR to SKY (2025-09), BTT to BTTC (2022-01), ERD to EGLD (2020-09), LEND to AAVE (2020-10), BCC to BCHABC to BCH (2018-11, 2019-11), and others. Some are also redenominated at the swap (BTT 1:1000, ERD 1000:1, LEND 100:1, MKR 1:24000).

The Store treats the two symbols as two coins. The new one needs 30 daily bars before it can rank, so the coin is missing from the universe for one or two reconstitutions, and a held position in the old symbol is sold at its last close by the engine. This affects a few coin-months and biases nothing in a known direction, but a strategy's turnover around a rename is overstated. Stitching renames into one history (a lineage table with ratios) is possible and not done; it would need each swap's terms from a reliable source.
