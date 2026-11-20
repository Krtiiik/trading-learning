---
id: H2001
title: Among universe members, coins with a higher return over the past 21 days earn more over the next 7 days
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  Cross-sectional momentum at one to four weeks. Liu, Tsyvinski and Wu (sample to 2018-12-31)
  sort about 1,700 coins every week on past return: the top quintile beats the bottom by 2.7,
  3.3, 4.1 and 2.5 percent a week for lookbacks of 1, 2, 3 and 4 weeks (t = 2.0 to 2.7), by
  nothing for 8 weeks or more, the profit is in the winners (4.3 percent a week against 0.2 for
  the 3-week sort) and in coins above median size (spread 4.2 percent, t = 2.57, against 0.6
  below median). Begusic and Kostanjcar (to January 2019) find winners minus losers of +0.26
  percent a day in the liquid third of coins only, and reversal in the illiquid third. Ficura
  (to 2022-12, abstract and introduction only) finds that last week's return predicts the next
  week's positively among large, liquid coins (t = 2.33) and negatively among the rest. Against
  it, Dobrynskaya and Dubrovskiy (to 2020-11-01) find a momentum factor that is not significant
  over 2014 to 2020 (t = 0.95), damaged in 2019 and 2020 by extreme returns of past losers, and
  equal-weighted tests over the whole market find nothing. Our 40 members are the large, liquid
  end of those samples, where the published sign is positive. All of this is taken from the
  Literature scout's notes in research/literature/cross-sectional.md (sections 1a, 1b, 1c and
  "Failures and decay"); every sample ends by 2022-12-31.
sources:
  - "Liu, Y., Tsyvinski, A. and Wu, X. (2022). Common Risk Factors in Cryptocurrency. Journal of Finance 77(2), 1133-1177. Read by the scout as NBER Working Paper 25882 (Tables 4, 7, A.2). Sample: 1,707 coins above 1 million dollars, weekly, 2014 to 2018-12-31. https://www.nber.org/papers/w25882"
  - "Begusic, S. and Kostanjcar, Z. (2019). Momentum and liquidity in cryptocurrencies. arXiv:1904.00890 (working paper; Tables 1, 2). Sample: 711 coins, daily, January 2015 to January 2019. https://arxiv.org/abs/1904.00890"
  - "Ficura, M. (2023). Impact of size and volume on cryptocurrency momentum and reversal. FFA Working Paper 3/2023, Prague University of Economics and Business (abstract and introduction read by the scout). Sample: CoinMarketCap, weekly, June 2017 to December 2022. https://wp.ffu.vse.cz/artkey/wps-202301-0003_impact-of-size-and-volume-on-cryptocurrency-momentum-and-reversal.php"
  - "Dobrynskaya, V. and Dubrovskiy, M. (2022). Cryptocurrencies meet equities: risk factors and asset pricing relationships. HSE Working Paper WP BRP 86/FE/2022 (Table 3). Sample: 1,986 coins, weekly, 2014-01-06 to 2020-11-01. Evidence of decay. https://wp.hse.ru/data/2022/02/24/1749596434/86FE2022.pdf"

prediction:
  direction: positive
  size: "about 0.03"
  unit: mean rank information coefficient (Spearman correlation across universe members between the signal and the return over the next 7 days)

primary_test:
  experiment: trading.experiments.h2001
  granularity: 1d
  params:
    lookback_days: 21
    horizon_days: 7
    start: "2019-07-01"
  description: >
    At the close of every daily bar t labelled 2019-07-01 or later, each point-in-time universe
    member (market.member at t) with a close at t and at t-21 is scored with
    close[t] / close[t-21] - 1. The forward return is open[t+8] / open[t+1] - 1: seven days from
    the next bar's open. For each bar with at least 5 scored members that have a forward return
    the Spearman rank correlation across those members is computed; the estimate is its mean
    over bars (evaluate_predictor, method rank_ic, horizon 7). The p-value is one-sided (mean
    above zero) from a t-test with Newey-West errors, 12 lags, which allow for the seven-day
    overlap of consecutive forward returns.

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
    bar's rank correlation is an assumption, not a measurement: 40 independent coins give
    1/sqrt(39) = 0.16, and coins that move together make it larger, so 0.2 (at 0.16 the train
    figure is 0.029, at 0.3 it is 0.055). The predicted 0.03 is a little below what train
    detects with 80% power: a true effect of that size passes a one-sided 5% test roughly two
    times in three (my arithmetic from the standard error). A rejection therefore means "below
    about 0.04", not "absent". min_size 0.01 instead of the template's 0.2 because the unit is
    a rank correlation, not a Sharpe ratio: a weekly rank correlation below 0.01 is too small
    to matter for any use.

data:
  - binance/spot/1d
  - binance/universe
---

# H2001: among universe members, coins with a higher return over the past 21 days earn more over the next 7 days

## Registered design

Written on 2026-11-19, before the experiment was run on any real data. The signal code ran on the synthetic Store only (`tests/test_crosssection_tools.py`).

**What is tested.** Whether the past 21-day return orders the 40 point-in-time universe members by their return over the next 7 days. It is a predictive claim: no portfolio, no costs. A positive result would say the signal carries information, not that a rule built on it beats a benchmark after costs.

**What part of the published result this can test.** The sources report a long-short quintile spread over 700 to 1,700 coins, value-weighted, with the profit in the winners and in the larger coins. We have no market capitalisation and no shorting. The rank correlation within the 40 most traded USDT pairs tests the one part that should transfer: the ordering by past return inside the large, liquid group. It cannot say which leg carries it, and the published size (percent a week between extreme quintiles of the whole market) does not transfer.

**Where each choice comes from.**

- *Lookback 21 days.* The published range is 1 to 4 weeks; 3 weeks is the peak in Liu, Tsyvinski and Wu (4.1 percent a week, t = 2.742). The others use 2 weeks (Begusic and Kostanjcar) and 1 week (Ficura). No other value was or will be tried under this id.
- *Horizon 7 days.* The holding period of Liu, Tsyvinski and Wu and of Ficura.
- *No day skipped between signal and entry.* None of the sources skips one. On daily bars the next open is the instant the signal bar closes.
- *Evaluated at every daily bar*, not once a week: the same question asked on each day, with the overlap handled by the Newey-West errors. It uses all the data and does not depend on which weekday a week ends.
- *Start 2019-07-01.* The universe has 40 members only from that date (`research/knowhow/universe-is-smaller-than-40-before-mid-2019.md`); before it a rank correlation is over 2 to 39 coins. The start also puts the whole train window after the sample of the main source (2018-12-31), though inside Ficura's.
- *Short history.* Membership needs 30 daily bars, so a 21-day lookback is full for every member (`new-members-have-short-history.md`); a coin without a close at either end is not scored.
- *Predicted size 0.03.* A quintile spread of 4 percent a week over the whole market, with an assumed cross-sectional standard deviation of weekly returns of 20 percent and 2.8 standard deviations between the extreme quintiles' mean scores, corresponds to a rank correlation of about 0.07 (my arithmetic; the dispersion is an assumption). Less than half of that is predicted, because the one source that covers 2019 and 2020 reports the factor no longer significant and because 40 coins are a narrower cross-section.

**A limit of the test.** A member whose pair stops trading within the 7 days has no forward return and drops out of that bar's correlation. Nine train members stop trading during a month of membership (`members-stop-trading-mid-month.md`), one of them (LUNAUSDT-2022) after a collapse: a past loser whose last week is then not counted. That is at most 7 bars per such coin out of about 51,000 member-bars.

**What I knew before registering.** I did not load, plot or summarise train or dev data. I read the Data steward's notes (counts of bars, members and volumes on train) and H1001's file with its Skeptic review, which reports train results of a per-coin trend filter (a time-series rule), among them that coins passing through the universe did worse than its fixtures. No choice above depends on those.

**What would count as the test having been done wrongly.** The run record's `n` is not 1,272 on train (1,280 bars from 2019-07-01 to 2022-12-31, less the 8 whose horizon runs past the end); the harness's look-ahead check fails; `ic_std` is far from the assumed 0.2 (then the minimum detectable effect above is wrong and the Results must restate it).

## Results

## Verdict
