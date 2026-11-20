---
id: H2006
title: The one-day reversal across universe members is stronger among coins whose volume that day was abnormally low than among coins whose volume was abnormally high
family: cross-sectional
origin: literature
claim: predictive
status: registered

motivation: >
  Bianchi, Babiak and Dickerson (2022; the 100 most liquid USD pairs aggregated over more than
  80 exchanges, daily, 2017-03-01 to 2022-03-01) sort coins each day on that day's return and
  on a volume shock (log volume against its mean over the previous 30 days, scaled by the
  standard deviation of log volume). Losers minus winners over the next day earn, equal
  weighted, 1.22 percent a day within the low-volume third (p = 0.002) against 0.54 within
  the high-volume third (p = 0.003); value weighted, 0.6 percent (p = 0.001) against -0.18
  (p = 0.543). They read it as compensation for providing liquidity. Against a large effect
  here: on Binance USDT pairs alone (2018-10 to 2022-03) the low-volume reversal is 0.187
  percent a day gross and negative after costs, about a tenth of the aggregate result, and
  value-weighted versions do not survive costs anywhere. So this is registered as a predictive
  interaction with a small predicted size, not as a rule. Taken from the Literature scout's
  notes (research/literature/cross-sectional.md, Sections 3a and 4).
sources:
  - "Bianchi, D., Babiak, M. and Dickerson, A. (2022). Trading volume and liquidity provision in cryptocurrency markets. Journal of Banking & Finance 142, 106547. Read by the scout as Sveriges Riksbank Working Paper 413 (Section 2.2, Tables 2, 3, 5, 7). Sample: daily, 2017-03-01 to 2022-03-01. https://doi.org/10.1016/j.jbankfin.2022.106547"

prediction:
  direction: negative
  size: "about -0.02"
  unit: difference of mean rank information coefficients (lowest third of volume shock minus highest third; Spearman, per daily bar)

primary_test:
  experiment: trading.experiments.h2006
  granularity: 1d
  params:
    shock_days: 30
    horizon_days: 1
    start: "2019-07-01"
  description: >
    At the close of every daily bar t each coin has a return (close[t] over close[t-1], minus
    one) and a volume shock: log quote volume of bar t minus the log of the mean quote volume
    of bars t-30 to t-1, divided by the standard deviation of log quote volume over bars t-30
    to t-1 (all 30 needed, each with volume above zero). The point-in-time universe members
    that have both are ranked by the shock; the lowest third and the highest third are taken
    (floor(n/3) coins each). Within each third the Spearman rank correlation between the
    bar's return and the return from the open of bar t+1 to the open of bar t+2 is computed
    (at least 5 coins). The estimate is the mean over the bars labelled 2019-07-01 or later of
    the lowest third's coefficient minus the highest third's
    (crosssection_tools_b.evaluate_rank_ic_by_thirds); the p-value is one-sided (mean below
    zero) from a Newey-West t-test of that daily difference.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.01

power:
  mde_train: 0.029
  mde_dev: 0.038
  note: >
    From `uv run trading research mde mean --deviation 0.41 --per-year 365 --overlap 1 --start
    2019-07-01`: train standard error 0.0115, minimum detectable effect 0.029; dev standard
    error 0.0152, minimum detectable effect 0.038. The deviation is an assumption made without
    data: a rank coefficient across 13 coins has a deviation of about 1/sqrt(12) = 0.29, and
    the difference of two independent ones 0.41. The predicted -0.02 is below what train
    detects with 80% power, so this test is underpowered and was known to be: a rejection will
    mean "smaller than about 0.03 in absolute value", not "absent". A negative estimate is a
    difference in the predicted direction (more reversal after low volume).

data:
  - binance/spot/1d
  - binance/universe
---

# H2006: the one-day reversal is stronger after abnormally low volume

## Registered design

Written on 2026-11-19, before the experiment was run on any real data and before I loaded any train data in this session. The helper it uses was exercised on simulated arrays only (`tests/test_crosssection_tools_b.py`).

- **Volume shock: as published, m = 30** (Section 2.2, Eq. 1 of the source as the scout transcribed it), from quote volume, which is the dollar volume the source uses.
- **From a double sort to a difference of rank coefficients.** The source sorts 100 pairs 3 by 3 and reports portfolio returns. With 40 coins a 3 by 3 sort leaves 4 or 5 coins a cell, so the same interaction is stated here as a rank coefficient inside each third of volume shock (13 coins) and their difference. A reversal is a negative coefficient between today's return and tomorrow's; "stronger after low volume" is a more negative coefficient in the lowest third than in the highest, so the registered direction of the difference is negative.
- **What is not claimed.** That a reversal exists at all in this universe (the unconditional one-day reversal belongs to the other cross-sectional Researcher, H2001 to H2004), or that a volume shock alone predicts returns (the source finds it does not). The two thirds' own coefficients are in the run record and will be quoted, but they decide nothing.
- **Bid-ask bounce.** On daily bars the next open is the same instant as the close that made the signal, so bounce is in both thirds' coefficients; it would cancel in the difference only if it were equal in both, and a coin on a low-volume day may well have a wider spread. A negative estimate therefore cannot separate liquidity provision from bounce. The source has the same limit.
- **Predicted size.** On Binance the source's low-volume reversal is 0.19 percent a day for extreme deciles. With a cross-sectional spread of daily returns of about 4 percent (an assumption) that is a rank coefficient of roughly -0.014 in the low-volume third (my arithmetic), and less in the high-volume third: a difference of -0.01 to -0.02. The aggregate result would suggest several times that. Registered: about -0.02.
- **Start: 2019-07-01**, when the universe first has 40 members, so each third has 13 coins.
- **What would count as the test having been done wrongly:** fewer than about 1,250 daily differences in the train window; thirds of fewer than 12 coins on typical days; a look-ahead refusal.

## Results

## Verdict
