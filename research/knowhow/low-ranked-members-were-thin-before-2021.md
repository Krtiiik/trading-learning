---
title: "Before 2021 the lower ranks of the point-in-time universe traded a few million USDT a day or less"
kind: fact
area: data
source: "Data steward check on 2026-11-18, train reconstitutions only: `quote_volume / 30` in binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-18
---

Mean daily quote volume over the 30-day lookback, in million USDT (train data only):

| Year | Rank 40: lowest month | Rank 40: median month | Tier 3 median | Member-months below 1 M a day | below 5 M a day |
|---|---|---|---|---|---|
| 2019 (from July) | 0.3 | 0.4 | 1.2 | 29% | 65% |
| 2020 | 0.3 | 1.6 | 5.4 | 4% | 32% |
| 2021 | 9.5 | 72 | 104 | 0% | 0% |
| 2022 | 11 | 25 | 44 | 0% | 0% |

The top is far heavier than the bottom: rank 1 trades about 160 times rank 40 (median over reconstitutions), and from 2019-07 BTC and ETH carry 54% of the universe's volume, ranks 3 to 12 carry 30% and ranks 13 to 40 carry 17%.

Why it matters: an equal-weight portfolio puts 2.5% in every member, so 70% of it sits in tier 3 whatever those coins trade. The cost model charges one slippage per tier in every year, so in 2019 and 2020 it is at its most optimistic exactly where 1/N trades most. A result carried by tier-3 trades in 2019 and 2020 needs its double-cost run read with care, and says little about capacity.

Not established: the coins' total liquidity. These are USDT pairs only, and in 2018 to 2020 many coins traded mainly against BTC (from memory, not measured here), so the figures understate what could be traded in the coin but not what could be traded in the pair the Store prices.
