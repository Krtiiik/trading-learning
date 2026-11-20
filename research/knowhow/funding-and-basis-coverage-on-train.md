---
title: "Funding and basis cover no member before 2020, 71% of member-days in 2020 and 92% in 2021 and 2022"
kind: fact
area: data
source: "Data steward count on 2026-11-19 over train (to 2022-12-31): binance/funding id 619020e39d56, binance/premium/1h id 5dd2d25c086b, binance/universe id 88f9a7cf72c7, daily market from binance/spot/1d id 2d6763395242"
trust: high
date: 2026-11-19
---

Share of member-days (a universe member on a daily bar) for which the aligned panel has a value:

| Year | Member-days | With funding | With basis | Members with funding on a day (min to max) |
|---|---|---|---|---|
| 2017 to 2019 | 16,467 | 0% | 0% | 0 |
| 2020 | 14,640 | 70.9% | 70.8% | 3 to 24 in Q1, 24 to 29 in Q2, 28 to 36 in Q3, 37 to 40 in Q4 |
| 2021 | 14,600 | 92.0% | 92.5% | 34 to 40 |
| 2022 | 14,600 | 91.2% | 92.1% | 34 to 39 |

The first payment in the archive is stamped 2020-01-01 00:00 (BTC, ETH, BCH); 12 members have funding in January 2020, 24 from February. So a derivatives hypothesis has at most three train years, and a cross-section of 28 or more coins only from 2020-07 (37 or more from 2020-10). In 2021 and 2022 coverage by liquidity tier is 100% for tier 1, 97.3% for tier 2 and 89.0% for tier 3: the coins without a contract are the small ones, so "members with funding" is not a random subset of the universe.

Of the 183 train members 160 have a funding file and 145 have payments on train. Of the 120 coins that first join the universe from 2020-01 on, 74 have funding when they join (the contract was listed a median of 32 days before), 17 get it later on train (18 days later for JASMY up to 803 for FTT; ICP 427, IOTX 528, INJ 592, ARPA 657) and 29 never on train. The most member-days without funding in 2021 and 2022: ICP 335, SLP 184, CAKE 183, TLM 153, FTT 119, then TFUEL, ANC, the new LUNA and SANTOS with about 92 each.

The two series do not start together for every coin. ICP has basis from 2021-05-11 and funding only from 2022-09-01, TLM basis from 2021-07 and no funding on train: the funding archive lacks their first contract. In 2021 and 2022 480 member-days have basis without funding and 286 funding without basis (most of the latter are the days the basis archive lacks, see the note on the premium index).

What to do: state the start date in the hypothesis (2020-07-01 or later for a cross-section) and pass it to the minimum detectable effect; decide before the run what a rule does with a member that has no contract (the equal-weight benchmark holds it anyway); never fill a missing series with zero.

Not established: coverage after 2022 (not counted, to stay away from test-period memberships); open interest, which was not in the Store when this was measured.
