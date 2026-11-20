---
id: H4005
title: A rise in the exchange's total quote volume on one day is followed by a higher Bitcoin return on the next day
family: cross-market
origin: literature
claim: predictive
status: registered

motivation: >
  Garcia and Schweitzer (2015; Bitcoin, daily, 2011-02-01 to 2014-12-31) fit a vector
  autoregression with one daily lag on first-differenced, standardised signals and find that a
  shock to exchange trading volume (summed over about 80 markets) has a significant positive
  effect on Bitcoin's return one day later, which decays quickly (their Fig. 3A); the
  cumulative effect of a shock reaches about 0.5 percent within a day (Fig. 3D). On their
  leave-out period a long-short strategy on the volume signal alone has an annualised Sharpe
  ratio of 0.57 (Table 1), with profit that the paper attributes mostly to the short side in a
  falling year. It is the one cost-aware result in the Literature scout's notes for this family
  that needs no outside data (research/literature/cross-market.md, section 1, read by the
  scout in full as the arXiv HTML version; supplement not opened). Against it: one coin, one
  early sample that ends eight years before the train segment does, volume from many exchanges
  where we have one, and the scout's own caveat that the published profit is from 2014.
sources:
  - "Garcia, D. and Schweitzer, F. (2015). Social signals and algorithmic trading of Bitcoin. Royal Society Open Science 2: 150288. Read by the Literature scout as arXiv:1506.01513 (HTML), Fig. 3 and Table 1; supplement not opened. Sample: Bitcoin, daily, 2011-02-01 to 2014-12-31. https://doi.org/10.1098/rsos.150288"

prediction:
  direction: positive
  size: "about 0.01"
  unit: next-day Bitcoin return per unit change in the log of total quote volume (slope of a predictive regression)

primary_test:
  experiment: trading.experiments.h4005
  granularity: 1d
  params:
    clip: 1.0
    horizon_bars: 1
    target: BTCUSDT
  description: >
    Signal at the close of daily bar t: the log of the total quote volume of bar t minus the
    log of the total quote volume of bar t-1, both summed over the same coins (the
    point-in-time universe members in force at bar t that have a bar on both days), limited
    to plus or minus 1.0. Target: BTCUSDT's return from the open of bar t+1 to the open of
    bar t+2. The estimate is the slope of the regression of the target on the signal over
    all bars of the segment with a signal (evaluate_market_predictor, horizon 1); the p-value
    is one-sided (slope above zero) from Newey-West errors. The same regression against the
    equal-weight universe's return is stored as a diagnostic and decides nothing.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.003

power:
  mde_train: 0.0069
  mde_dev: 0.0113
  note: >
    From `uv run trading research mde mean --deviation 0.1224 --per-year 365 --start 2017-10-01`:
    train 5.25 years, standard error 0.0028, minimum detectable effect 0.0069; dev 2.00 years,
    standard error 0.0045, minimum detectable effect 0.0113. The deviation is the standard
    deviation of BTCUSDT's next-day return on train (0.040) divided by that of the clipped
    signal (0.33): the standard error of a slope is their ratio over the square root of the
    number of days. The predicted 0.01 is the published 0.5 percent per one-standard-deviation
    shock spread over a standard deviation of 0.35 (0.014 per unit), taken down because the
    source is one early sample. It is above what train can detect and about what dev can, so
    a train slope near zero would mean that an effect of the published size is not there in
    2017 to 2022; a true effect a third of the published size would be missed about half the time.

data:
  - binance/spot/1d
  - binance/universe
---

# H4005: a rise in the exchange's total quote volume is followed by a higher Bitcoin return the next day

## Registered design

Written on 2026-11-19, before the experiment was run on real data.

- **Signal.** The source first-differences and standardises daily exchange volume. Here: the day-on-day change in the log of total quote volume (USDT) over the point-in-time universe members, the same coins on both days so that a reconstitution is not read as a volume shock. The log makes the change comparable between 2017 and 2022, when volume differs by orders of magnitude. No standardisation: a constant scale only changes the unit, and a standard deviation over the whole sample would use the future. The whole daily bar t is known at its close (24:00 UTC), which is the open of bar t+1, where the target return starts.
- **Total volume, not Bitcoin's own.** The source sums Bitcoin's volume over all exchanges; we have one exchange and take all of its members, of which BTCUSDT is the largest. This is a choice made before any run and not compared with the alternative.
- **Clip at 1.0.** The Data steward's notes record exchange outages (75 hours in February 2018); a day cut short shows up as a fall and a rebound in volume that are no "shocks" in the source's sense. On train the signal's standard deviation is 0.35 and its extremes are -3.6 and +2.6; 1.0 is about three standard deviations. Chosen from the signal's own distribution, not from its relation to returns.
- **Target: BTCUSDT**, the coin the source is about, with a bar on every train day. The equal-weight universe is a diagnostic.
- **Horizon: one day**, the source's lag. Start: none declared; the signal exists from 2017-10-01 (the first reconstitution), 1,918 train days.
- **Claim: predictive only.** A long-or-flat rule on this signal would switch on roughly every other day, about 180 round trips a year at 24 bps each (BTC, 12 bps a side) or some 40 percent a year in costs; nothing in the source suggests the long side alone carries that. No trading claim is made.

What I looked at before registering: on train, the signal's count, standard deviation by year (0.28 to 0.40), extremes and first-order autocorrelation (-0.19), and the standard deviation of BTCUSDT's next-day return (0.040), for the power calculation and the clip. I did not compute, plot or tabulate any relation between volume and returns.

What would count as the test having been done wrongly: fewer than about 1,900 observations on train; a look-ahead refusal; a signal whose standard deviation is far from 0.33.

## Results

## Verdict
