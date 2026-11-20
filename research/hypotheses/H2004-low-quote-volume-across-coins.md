---
id: H2004
title: Among universe members, coins with a lower quote volume over the past 7 days earn more over the next 7 days
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  The dollar-volume effect. Liu, Tsyvinski and Wu (about 1,700 coins, weekly, to 2018-12-31)
  sort coins on the log of the formation week's average daily dollar volume: the lowest
  quintile earns 4.5 percent in the next week and the highest 1.3, a spread of -3.2 percent
  (t = -2.016); the standard deviation of dollar volume gives -3.0 percent (t = -2.269). They
  note that both are absorbed by their size factor. Volume in coins, volume scaled by
  capitalisation and the Amihud ratio do not predict returns in their tables (Amihud +2.6
  percent, t = 1.478), and Begusic and Kostanjcar (to January 2019) find an illiquidity premium
  only among past losers. For size, which the volume effect goes with, the whole premium is in
  the smallest fifth of the market and the other four quintiles are flat. Our 40 members are
  chosen for being the most traded pairs, so they all sit at the top of those sorts: the
  published tables give little reason to expect a gradient among them. The hypothesis takes
  the published sign and predicts a small effect; the literature's own reading makes a null
  the expected outcome. Taken from research/literature/cross-sectional.md, sections 5 and 6;
  every sample ends by 2022-12-31.
sources:
  - "Liu, Y., Tsyvinski, A. and Wu, X. (2022). Common Risk Factors in Cryptocurrency. Journal of Finance 77(2), 1133-1177. Read by the scout as NBER Working Paper 25882 (Tables 3, 5, 6, 7). Sample: 1,707 coins above 1 million dollars, weekly, 2014 to 2018-12-31. https://www.nber.org/papers/w25882"
  - "Begusic, S. and Kostanjcar, Z. (2019). Momentum and liquidity in cryptocurrencies. arXiv:1904.00890 (working paper; Table 1). Sample: 711 coins, daily, January 2015 to January 2019. https://arxiv.org/abs/1904.00890"

prediction:
  direction: negative
  size: "about -0.02"
  unit: mean rank information coefficient (Spearman correlation across universe members between past quote volume and the return over the next 7 days)

primary_test:
  experiment: trading.experiments.h2004
  granularity: 1d
  params:
    lookback_days: 7
    horizon_days: 7
    start: "2019-07-01"
  description: >
    At the close of every daily bar t labelled 2019-07-01 or later, each point-in-time universe
    member (market.member at t) with a bar on each of the days t-6 to t is scored with the log
    of its mean daily quote volume (USDT) over those 7 bars. The forward return is
    open[t+8] / open[t+1] - 1: seven days from the next bar's open. For each bar with at least
    5 scored members that have a forward return the Spearman rank correlation across those
    members is computed; the estimate is its mean over bars (evaluate_predictor, method
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
    to 0.2 because coins move together; for a characteristic that changes slowly and goes with
    how much a coin moves with the market it may be higher (at 0.3 the train figure is 0.055).
    The predicted 0.02 is about half of what train detects with 80% power: a true effect of
    that size passes a one-sided 5% test about four times in ten (my arithmetic). The test is
    underpowered for the predicted size and was known to be. A rejection means "no gradient
    larger than about 0.04", which is what the published tables suggest for the top of the
    market, and not "no volume effect in crypto". min_size 0.01 (in size, the sign being
    negative) because the unit is a weekly rank correlation, not a Sharpe ratio.

data:
  - binance/spot/1d
  - binance/universe
---

# H2004: among universe members, coins with a lower quote volume over the past 7 days earn more over the next 7 days

## Registered design

Written on 2026-11-19, before the experiment was run on any real data. The signal code ran on the synthetic Store only (`tests/test_crosssection_tools.py`).

**What is tested.** Whether quote volume orders the 40 point-in-time universe members by their return over the next 7 days, in reverse. A predictive claim: no portfolio and no costs.

**What part of the published result this can test.** The published premium is earned by the least traded fifth of about 1,700 coins: micro-caps that are far outside our universe and that we could not buy at the published prices anyway. What can be tested here is only whether the relation continues as a gradient inside the most traded group. The published quintile tables say it does not for size (quintiles 2 to 5 are flat); for dollar volume the scout's notes give the two extreme quintiles only. So this is a weak analogue with a low prior, registered because liquidity is a sub-angle the family should have a documented answer on. We have no market capitalisation, so volume scaled by capitalisation (turnover) cannot be computed, and volume here is one exchange's USDT pair, not the aggregate the source uses: a coin traded mainly elsewhere or against BTC ranks lower here than in the source (`research/knowhow/low-ranked-members-were-thin-before-2021.md`).

**Where each choice comes from.**

- *Signal: log of the mean daily quote volume over 7 days; horizon 7 days.* Liu, Tsyvinski and Wu's definition (log of the formation week's average daily volume times price) and their holding week. Quote volume is volume times price in USDT.
- *Why dollar volume and not its standard deviation or the Amihud ratio.* Dollar volume is the plainest of the three and has a significant published spread. Its standard deviation is by the paper's own account mostly price level and size; the Amihud ratio has a published null with the opposite sign. Neither was or will be tried under this id.
- *Start 2019-07-01.* The universe has 40 members only from that date (`universe-is-smaller-than-40-before-mid-2019.md`). The whole train window is after the source's sample (2018-12-31): an out-of-sample test of the sign.
- *Short history.* Membership needs 30 daily bars, so 7 are always there for a member that still trades.
- *Predicted size -0.02.* The published spread of -3.2 percent a week over the whole market would be a rank correlation of roughly -0.05 if it were a gradient across all quintiles (my arithmetic: an assumed cross-sectional standard deviation of weekly returns of 20 percent, 2.8 standard deviations between extreme quintiles). It is not one, and our members are its flat end, so less than half is predicted.

**Two things known about the signal before running.** The universe is itself chosen on 30-day quote volume, so the signal is close to a coin's rank in the universe and changes slowly; the range is still wide (rank 1 trades about 160 times rank 40, per the Data steward's note). And the less traded members are likely to be the more volatile ones, so this test shares H2003's confound: in a falling market the rank correlation is pushed up and in a rising one down, whatever the truth about a volume premium. The train window from 2019-07 contains both.

**What I knew before registering.** I did not load, plot or summarise train or dev data. I read the Data steward's notes (among them the volume by rank on train) and H1001's file with its Skeptic review, which reports for a trend filter on train that the equal-weight universe did worse among coins that pass through the universe than among its fixtures (benchmark Sharpe ratio 0.12 against 0.84). Coins that pass through are mostly low-ranked by volume, so that is a train observation that leans against this hypothesis's direction. It did not choose the direction (the source did); I record it because I had read it.

**What would count as the test having been done wrongly.** The run record's `n` is not 1,272 on train; the look-ahead check fails; `ic_std` is far from the assumed 0.2 (then the minimum detectable effect is wrong and the Results must restate it).

## Results

## Verdict
