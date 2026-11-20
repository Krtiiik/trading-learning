---
id: H2003
title: Among universe members, coins with a lower volatility of daily returns over the past 30 days earn more over the next 7 days
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  The low-volatility effect in large coins. Kaya and Mostowfi (35 large coins, 2017-01-01 to
  2021-06-30, long only, with costs) rank coins by historical volatility over 1, 3, 6 or 12
  months and hold the least volatile for 1 to 12 months: those portfolios earn about 4.4 to
  9.7 percent a month, the most volatile ones -2 to -7 percent (never significant), and the
  long-short spread is mostly 1 to 6 percent a month. The statistics are weak (54 months, a
  grid of 64 combinations without a correction, t-values mostly below 2). In the whole market,
  Liu, Tsyvinski and Wu (to 2018-12-31) find the quintile with the highest standard deviation
  of daily returns in the formation week earning -0.4 percent in the next week against 1.3 to
  2.6 for the others, a spread of -1.7 percent that is not significant (t = -1.24), and
  Kakushadze (to 2018-08-18) a negative coefficient on an intraday volatility measure in daily
  regressions (t about -2.5). Three sources opened by the scout point the same way, none
  strongly. Abstracts the scout could not get behind report the opposite sign for
  idiosyncratic volatility in the broad market (Zhang and Li) and a failure of the
  low-volatility strategy over about 1,000 coins (Burggraf and Rudolf); both are unverified
  leads and a reason to test the direction rather than assume it. Taken from
  research/literature/cross-sectional.md, sections 8a, 8b and their "Transfer"; every sample
  ends by 2022-12-31.
sources:
  - "Kaya, O. and Mostowfi, M. (2022). Low-volatility strategies for highly liquid cryptocurrencies. Finance Research Letters 46, 102422 (Table 1). Sample: 35 coins, daily, 2017-01-01 to 2021-06-30. https://digitalcollection.zhaw.ch/bitstream/11475/23853/3/2022_Kaya-Mostowfi_Low-volatility-strategies-cryptocurrencies_frl.pdf"
  - "Liu, Y., Tsyvinski, A. and Wu, X. (2022). Common Risk Factors in Cryptocurrency. Journal of Finance 77(2), 1133-1177. Read by the scout as NBER Working Paper 25882 (Table 7). Sample: 1,707 coins above 1 million dollars, weekly, 2014 to 2018-12-31. https://www.nber.org/papers/w25882"
  - "Kakushadze, Z. (2018). Cryptoasset Factor Models. arXiv:1811.07860 (working paper; Table 1). Sample: 362 coins, daily, to 2018-08-18. https://arxiv.org/abs/1811.07860"

prediction:
  direction: negative
  size: "about -0.03"
  unit: mean rank information coefficient (Spearman correlation across universe members between past volatility and the return over the next 7 days)

primary_test:
  experiment: trading.experiments.h2003
  granularity: 1d
  params:
    lookback_days: 30
    horizon_days: 7
    start: "2019-07-01"
  description: >
    At the close of every daily bar t labelled 2019-07-01 or later, each point-in-time universe
    member (market.member at t) with a close on each of the bars t-30 to t is scored with the
    sample standard deviation of its last 30 daily close-to-close returns. The forward return
    is open[t+8] / open[t+1] - 1: seven days from the next bar's open. For each bar with at
    least 5 scored members that have a forward return the Spearman rank correlation across
    those members is computed; the estimate is its mean over bars (evaluate_predictor, method
    rank_ic, horizon 7). The p-value is one-sided (mean below zero) from a t-test with
    Newey-West errors, 12 lags, which allow for the seven-day overlap of forward returns.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.01

power:
  mde_train: 0.037
  mde_dev: 0.049
  note: >
    From `uv run trading research mde mean --deviation 0.2 --per-year 365 --overlap 7 --start
    2019-07-01`: train 3.51 years, standard error 0.0148, minimum detectable effect 0.0368; dev
    2.00 years, standard error 0.0196, minimum detectable effect 0.0487. The deviation of one
    bar's rank correlation is an assumption: 1/sqrt(39) = 0.16 for 40 independent coins, raised
    to 0.2 because coins move together. For this signal it may well be higher: volatile coins
    tend to be the ones that move most with the market, so the rank correlation should swing
    with the market's direction (at 0.3 the train figure is 0.055). The predicted 0.03 is below
    what train detects with 80% power; a true effect of that size passes a one-sided 5% test
    about two times in three at a deviation of 0.2 and less than half the time at 0.3 (my
    arithmetic). A rejection means "below about 0.04 to 0.06", not "absent". min_size 0.01
    (in size, the sign being negative) because the unit is a weekly rank correlation, not a
    Sharpe ratio.

data:
  - binance/spot/1d
  - binance/universe
---

# H2003: among universe members, coins with a lower volatility of daily returns over the past 30 days earn more over the next 7 days

## Registered design

Written on 2026-11-19, before the experiment was run on any real data. The signal code ran on the synthetic Store only (`tests/test_crosssection_tools.py`).

**What is tested.** Whether past volatility orders the 40 point-in-time universe members by their return over the next 7 days, in reverse. A predictive claim: no portfolio and no costs.

**What part of the published result this can test.** Kaya and Mostowfi's claim is about a long-only portfolio of the 3 to 9 least volatile of 35 large coins, after costs, and they show "low beats high" weakly, not "low beats the average coin". The rank correlation asks the question that lies under both: is the ordering by volatility related to the ordering by later return, over the whole cross-section of 40. It cannot say whether the effect, if any, sits in the calm coins doing well or the wild ones doing badly (Liu, Tsyvinski and Wu's table suggests the second), and it says nothing about a portfolio after costs. Sub-angle (3) of the family also covers the maximum daily return (lottery effect); it was not chosen because the one source the scout could open on it is a null and the two abstracts disagree on the sign.

**Where each choice comes from.**

- *Signal: standard deviation of daily returns.* The measure of all three sources (Kakushadze's is an intraday range, the nearest thing).
- *Lookback 30 days.* The literature does not pin this down: Liu, Tsyvinski and Wu use the 7 days of the formation week, Kaya and Mostowfi 1, 3, 6 or 12 months and find 6 and 12 the most consistent. 30 days is Kaya and Mostowfi's shortest and lies between the two sources. It was preferred to 6 months for one reason fixed by the data's shape, not its values: membership needs 30 daily bars, so a 30-day window exists for almost every member from its first month, while a 180-day window would leave 17 percent of member-months from 2019-07 unscored (`research/knowhow/new-members-have-short-history.md`) and turn the test into one about seasoned coins. No other value was or will be tried under this id.
- *Horizon 7 days.* Liu, Tsyvinski and Wu's holding week. Kaya and Mostowfi hold for a month or more; a 30-day horizon was not taken because the statistics toolkit is validated for overlaps of about 5 bars and says so for longer ones (`statistics-toolkit-validation.md`), and because it would leave about 40 independent observations on train.
- *Start 2019-07-01.* The universe has 40 members only from that date (`universe-is-smaller-than-40-before-mid-2019.md`). The window overlaps Kaya and Mostowfi's sample (to 2021-06-30) by two years, so the train run is partly a replication.
- *Short history.* The window needs 31 closes. A member in its first month can have exactly 30 bars on the 1st, so it is unscored on its first day or two. A coin with any missing close in the window is unscored, never carried forward.
- *Predicted size -0.03.* Liu, Tsyvinski and Wu's spread of -1.7 percent a week between extreme quintiles, with an assumed cross-sectional standard deviation of weekly returns of 15 to 20 percent and 2.8 standard deviations between the quintiles' mean scores, corresponds to a rank correlation of -0.03 to -0.04 (my arithmetic; the dispersion is an assumption). Kaya and Mostowfi's monthly spreads give a similar or smaller weekly figure.

**A known confound, stated before running.** Volatile coins are mostly high-beta coins, so in a falling market this rank correlation is negative and in a rising one positive whatever the truth about a volatility premium. The mean over a window that contains both rises and falls is the test; a window dominated by one direction would bias it. The train window from 2019-07 holds both (H1001-r01: the equal-weight universe rebalanced monthly grew by -4.2 percent a year over it, falling in late 2019 and in 2022 and rising in 2020 and 2021), so the bias should be small on train. The dev window is more one-sided (H1001-r02: the same benchmark grew 40.7 percent a year), which pushes this rank correlation up, against the prediction; a dev result would have to be read with that in mind.

**What I knew before registering.** I did not load, plot or summarise train or dev data. I read the Data steward's notes and H1001's file with its Skeptic review, which reports for a trend filter on train that the equal-weight universe fell in the second half of 2019 and in 2022 and rose in 2020 and 2021. That is knowledge of the train market's direction by year; it did not choose the direction of this hypothesis (the sources did) or any parameter.

**What would count as the test having been done wrongly.** The run record's `n` is not 1,272 on train; the look-ahead check fails; `ic_std` is far from the assumed 0.2 (then the minimum detectable effect is wrong and the Results must restate it).

## Results

## Verdict
