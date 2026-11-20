---
id: H2002
title: Among universe members, coins with a lower return on one day earn more on the next day
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  Daily cross-sectional reversal. Bianchi, Babiak and Dickerson (sample 2017-03-01 to
  2022-03-01, the 100 most liquid pairs each month, prices aggregated over more than 80
  exchanges) sort pairs into deciles on the day's return: losers beat winners the next day by
  2.2 percent equal-weighted and 0.6 percent value-weighted (p = 0.001), which the authors
  read as the reversal sitting in smaller pairs. On Binance USDT pairs alone (2018-10-01 to
  2022-03-01) their low-volume version of the strategy earns 0.187 percent a day gross
  equal-weighted and 0.059 value-weighted (not significant), a tenth of the aggregate result,
  and is negative after costs. Kakushadze (to 2018-08-18) finds a negative coefficient on the
  previous day's return in daily cross-sectional regressions (t about -34 over 362 coins, -17
  over 127), without saying whether it holds in large coins. The scout's notes also say that
  in large, liquid coins the past-return effect turns into continuation at one week (Ficura)
  and, by an abstract nobody here has read behind (Zaremba et al., an unverified lead), at one
  day too. So the published sign is negative and the prior for a top-40 universe on one
  exchange is a small or absent effect. Taken from research/literature/cross-sectional.md,
  sections 3a, 3b and their "Transfer"; every sample ends by 2022-12-31.
sources:
  - "Bianchi, D., Babiak, M. and Dickerson, A. (2022). Trading volume and liquidity provision in cryptocurrency markets. Journal of Banking & Finance 142, 106547. Read by the scout as Sveriges Riksbank Working Paper 413 (Tables 2, 5, 7). Sample: 100 most liquid USD pairs each month, daily, 2017-03-01 to 2022-03-01; Binance USDT pairs 2018-10-01 to 2022-03-01. https://doi.org/10.1016/j.jbankfin.2022.106547"
  - "Kakushadze, Z. (2018). Cryptoasset Factor Models. arXiv:1811.07860 (working paper; Tables 1, 2). Sample: 362 coins with one year of data, 127 with two, daily, to 2018-08-18. https://arxiv.org/abs/1811.07860"

prediction:
  direction: negative
  size: "about -0.015"
  unit: mean rank information coefficient (Spearman correlation across universe members between the day's return and the next day's return)

primary_test:
  experiment: trading.experiments.h2002
  granularity: 1d
  params:
    lookback_days: 1
    horizon_days: 1
    start: "2019-07-01"
  description: >
    At the close of every daily bar t labelled 2019-07-01 or later, each point-in-time universe
    member (market.member at t) with a close at t and at t-1 is scored with
    close[t] / close[t-1] - 1. The forward return is open[t+2] / open[t+1] - 1: one day from the
    next bar's open. For each bar with at least 5 scored members that have a forward return the
    Spearman rank correlation across those members is computed; the estimate is its mean over
    bars (evaluate_predictor, method rank_ic, horizon 1). The p-value is one-sided (mean below
    zero) from a t-test with Newey-West errors, 7 lags.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.005

power:
  mde_train: 0.014
  mde_dev: 0.018
  note: >
    From `uv run trading research mde mean --deviation 0.2 --per-year 365 --overlap 1 --start
    2019-07-01`: train 3.51 years, standard error 0.0056, minimum detectable effect 0.0139; dev
    2.00 years, standard error 0.0074, minimum detectable effect 0.0184. The deviation of one
    bar's rank correlation is an assumption: 1/sqrt(39) = 0.16 for 40 independent coins, raised
    to 0.2 because coins move together. The predicted size equals what train detects with 80%
    power, so this test is adequately powered and a null result is informative: it would say
    the daily reversal among the 40 members is below about 0.014 in rank correlation, if it
    exists. min_size 0.005 (in size, the sign being negative) because the unit is a daily rank
    correlation: below that nothing could be built on it.

data:
  - binance/spot/1d
  - binance/universe
---

# H2002: among universe members, coins with a lower return on one day earn more on the next day

## Registered design

Written on 2026-11-19, before the experiment was run on any real data. The signal code ran on the synthetic Store only (`tests/test_crosssection_tools.py`).

**What is tested.** Whether a day's return orders the 40 point-in-time universe members by their return on the following day, in reverse. A predictive claim only. A trading claim is not supported by the sources: a rule that holds yesterday's losers turns its whole position over every day, 24 to 50 bps a day at our costs, against a published gross of 6 to 19 bps a day on Binance for both legs together (the scout's arithmetic, section 3 "Transfer"; see also `research/knowhow/costs-kill-short-horizon-reversal.md`).

**What part of the published result this can test.** The published reversal is large when pairs are weighted equally over the 100 most liquid pairs of 80 exchanges, a quarter of that when weighted by value, and a tenth of it on Binance alone (in the low-volume version, the only one the scout's notes give per exchange). Our universe is the liquid end on one exchange, so this tests the weak end of the published effect: whether any reversal is left among the 40 most traded Binance USDT pairs. It cannot test the reversal in small or illiquid pairs, which is where the sources locate most of it.

**Where each choice comes from.**

- *Signal: the close-to-close return of one daily bar; horizon: the next day.* The design of Bianchi, Babiak and Dickerson (sort on the day's return, hold for the next day; their day also ends at 00:00 UTC). Kakushadze uses open-to-close returns, which for a market that never closes is the same thing.
- *Direction: negative*, the published sign in both sources opened, although the prior for large coins is weak.
- *Predicted size -0.015.* The Binance figure of 0.187 percent a day between extreme deciles, with an assumed cross-sectional standard deviation of daily returns of 4 percent and 3.5 standard deviations between the extreme deciles' mean scores, corresponds to a rank correlation of about -0.013; the value-weighted aggregate figure of 0.6 percent to about -0.04 (my arithmetic; the dispersion is an assumption). The prediction is at the low end.
- *Start 2019-07-01.* The universe has 40 members only from that date (`universe-is-smaller-than-40-before-mid-2019.md`). The window lies inside the Binance sample of the main source (to 2022-03-01), so the train run is close to a replication on our universe, not an out-of-sample test.

**Bid-ask bounce is not separated.** The return that makes the signal ends at the close of bar t and the forward return starts at the open of bar t+1, which on daily bars is the same instant and nearly the same price (median 0.04 percent apart over all train members' bars per `daily-bars-agree-with-raw-files-and-hourly-bars.md`, 0.02 for members per H1001's Skeptic review). A close that printed at the bid makes the day's return too low and the next day's too high, which looks like reversal. So a negative estimate could be bounce in part, and for thin members in 2019 and 2020 (`low-ranked-members-were-thin-before-2021.md`) that part need not be small. None of the sources measures it. A negative result here is evidence of a negative rank correlation in these bars, not of a tradable reversal.

**What I knew before registering.** I did not load, plot or summarise train or dev data. I read the Data steward's notes and H1001's file with its Skeptic review (train results of a per-coin trend filter). No choice above depends on those.

**What would count as the test having been done wrongly.** The run record's `n` is not 1,278 on train (1,280 bars from 2019-07-01, less the 2 whose horizon runs past the end); the look-ahead check fails; `ic_std` is far from the assumed 0.2 (then the minimum detectable effect is wrong and the Results must restate it).

## Results

## Verdict
