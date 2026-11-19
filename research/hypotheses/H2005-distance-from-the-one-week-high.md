---
id: H2005
title: Universe members that close nearer to their high of the past seven days earn more over the next seven days than members that close further below it
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  Fičura (2023; CoinMarketCap, weekly, June 2017 to December 2022) tests the "high-momentum"
  signal of George and Hwang (2004) on coins: the distance of the last close from the highest
  price of the past k weeks. For the one-week high he reports a positive relation with the
  next week's return among large and liquid coins (capitalisation above 50 million dollars and
  weekly volume above 5 million dollars; t = 4.93) and a negative one among small, illiquid
  coins (t = -9.03), and says the signal predicts better than plain past return. The
  point-in-time universe is the large and liquid side. The evidence is one working paper by
  one author, read by the Literature scout in abstract and introduction only
  (research/literature/cross-sectional.md, Section 7); no source reports costs or a long-only
  result, so this is registered as a predictive claim, not a rule. The signal is correlated
  with one-week momentum by construction; nothing here claims information beyond past return.
sources:
  - "Fičura, M. (2023). Impact of size and volume on cryptocurrency momentum and reversal. FFA Working Paper 3/2023, Prague University of Economics and Business. Sample: CoinMarketCap coins, weekly, June 2017 to December 2022. Read by the scout: abstract and introduction. https://wp.ffu.vse.cz/artkey/wps-202301-0003_impact-of-size-and-volume-on-cryptocurrency-momentum-and-reversal.php"
  - "George, T. J. and Hwang, C.-Y. (2004). The 52-week high and momentum investing. Journal of Finance 59(5), 2145-2176. Sample: US stocks, 1963 to 2001, no crypto. The parent signal; cited for the definition only."

prediction:
  direction: positive
  size: "about 0.03"
  unit: mean rank information coefficient (Spearman, across universe members, per daily bar)

primary_test:
  experiment: trading.experiments.h2005
  granularity: 1d
  params:
    high_days: 7
    horizon_days: 7
    start: "2019-07-01"
  description: >
    At the close of every daily bar t the signal of a coin is close[t] divided by the highest
    high of its last 7 daily bars (t-6 to t; all 7 must exist, otherwise no signal). Across
    the point-in-time universe members with a signal, the Spearman rank correlation between
    the signal and the return from the open of bar t+1 to the open of bar t+8 is computed for
    every bar labelled 2019-07-01 or later (evaluate_predictor, method rank_ic, horizon 7,
    at least 5 scored coins). The estimate is the mean of these daily coefficients; the
    p-value is one-sided (mean above zero) from a Newey-West t-test that allows for the
    overlapping seven-day horizons.

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
    2019-07-01`: train 3.51 years, standard error 0.0148, minimum detectable effect 0.037;
    dev 2.00 years, standard error 0.0196, minimum detectable effect 0.049. The deviation of
    0.2 for one day's coefficient across 40 coins is an assumption made without looking at
    data (independent ranks would give 1/sqrt(39) = 0.16; coins that move in groups make it
    larger). The predicted 0.03 is a little below what train detects with 80% power: a
    rejection will mean "smaller than about 0.04", not "absent".

data:
  - binance/spot/1d
  - binance/universe
---

# H2005: closing near the one-week high predicts a higher return next week

## Registered design

Written on 2026-11-19, before the experiment was run on any real data and before I loaded any train data in this session.

- **Signal.** `close[t] / max(high[t-6 .. t])`, between 0 and 1; a coin at its seven-day high has 1. The source measures the distance of the week's closing price from the highest price of the past k weeks with k = 1; seven daily bars ending at the signal bar is that window on daily bars. Whether the source's high is an intraday high or a highest close the scout's notes do not say; the bar's high is the "highest price" and is the convention taken here.
- **Horizon: 7 days**, the source's one-week holding period. The source forms the signal once a week; here it is formed at every daily close and the overlap is handled by the Newey-West errors. That is a difference in sampling, not in the claim.
- **Start: 2019-07-01**, when the point-in-time universe first has 40 members (`universe-is-smaller-than-40-before-mid-2019.md`). A rank across 2 to 19 coins is a different and noisier statistic.
- **Short history.** A lookback of 7 days is always full for a member (`new-members-have-short-history.md`: membership needs 30 daily bars). A coin with a missing bar in the window has no signal and is not ranked.
- **Predicted size.** The source gives a t-statistic, not a coefficient. A t of 4.93 over roughly 290 weeks with a weekly coefficient spread of 0.1 to 0.2 would be a mean coefficient of 0.03 to 0.06 (my arithmetic, a rough conversion of a regression t into a rank coefficient). Our 40 coins are a narrower and more homogeneous group than "above 50 million dollars", so I take the low end: about 0.03.
- **Overlap with the other cross-sectional Researcher.** One- to four-week momentum is tested under H2001 to H2004. This signal ranks coins much as the one-week return does; if both come out the same way that is one finding, not two.
- **What would count as the test having been done wrongly:** fewer than about 1,250 daily coefficients in the train window (it has 1,280 bars, the last 8 without a full horizon); a look-ahead refusal.

## Results

## Verdict
