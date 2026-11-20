---
id: H4001
title: Bitcoin's return over the last hour predicts the other universe members' return over the next hour, with the same sign
family: cross-market
origin: literature
claim: predictive
status: registered

motivation: >
  If news reaches Bitcoin first and the other coins with a delay, the others' next return has
  the sign of Bitcoin's last one. The published evidence is thin and split, and the Literature
  scout could read ABSTRACTS ONLY for this question (research/literature/cross-market.md,
  "Unverified leads", sub-angle 1). For: Wang and Ngene (2020), intraday data, find that
  Bitcoin's returns help forecast other coins' returns in rising and in falling markets (the
  abstract gives neither the sampling interval nor a sign nor dates; published 2020, so the
  sample ends by then). Guo et al. (2024, Binance data) find that lagged returns of other
  coins predict a coin's return and name slow diffusion of information as the reason, which
  is the mechanism that gives the positive sign registered here; their sample dates are
  unknown, so they are cited for the mechanism and not as clean evidence. Against: Sifat et
  al. (2019; hourly and daily, 2017-08 to 2018-09) find causality in both directions between
  Bitcoin and Ethereum that traders can barely exploit, and Bacao et al. (2018) find that
  transmission happens within the period. The direction "positive" is therefore the reading
  of the diffusion story, not a number quoted from a table, and the scout's own conclusion is
  that the prior at a one-hour horizon is small or zero. No train data on the relation was
  looked at before registration.
sources:
  - "Wang, J. and Ngene, G. M. (2020). Does Bitcoin still own the dominant power? An intraday analysis. International Review of Financial Analysis 71: 101551. Abstract only. Coins, sampling interval and dates not in the abstract; published 2020. https://doi.org/10.1016/j.irfa.2020.101551"
  - "Sifat, I. M., Mohamad, A. and Mohamed Shariff, M. S. B. (2019). Lead-Lag relationship between Bitcoin and Ethereum: Evidence from hourly and daily data. Research in International Business and Finance 50, 306-321. Abstract only. Sample: Bitcoin and Ethereum, hourly and daily, 2017-08 to 2018-09. A published null. https://doi.org/10.1016/j.ribaf.2019.06.012"
  - "Bacao, P., Duarte, A. P., Sebastiao, H. and Redzepagic, S. (2018). Information Transmission Between Cryptocurrencies: Does Bitcoin Rule the Cryptocurrency World? Scientific Annals of Economics and Business 65(2), 97-117. Abstract of the working paper only. Five coins; dates not in the abstract; published 2018. A published null. https://doi.org/10.2478/saeb-2018-0013"
  - "Guo, L., Sang, B., Tu, J. and Wang, Y. (2024). Cross-cryptocurrency return predictability. Journal of Economic Dynamics and Control 163: 104863. Abstract only. Binance data; SAMPLE DATES UNKNOWN (working paper December 2021), so used for the mechanism only. https://doi.org/10.1016/j.jedc.2024.104863"

prediction:
  direction: positive
  size: "about 0.02"
  unit: pooled slope (a member's return over the next hourly bar per unit of Bitcoin's return over the last hour; 0.02 means 2% of Bitcoin's move follows)

primary_test:
  experiment: trading.experiments.h4001
  granularity: 1h
  params:
    leader: BTCUSDT
    lookback_bars: 1
    skip_bars: 0
    horizon_bars: 1
    start: "2019-07-01"
  description: >
    At the close of every hourly bar t the signal of each point-in-time universe member other
    than Bitcoin is Bitcoin's close-to-close return over exactly the hour of bar t (NaN when
    the previous hour has no bar, and for a coin whose own bar t is missing or had no trade).
    It is set against the coin's return from the open of bar t+1 to the open of bar t+2
    (evaluate_predictor, method panel, horizon 1): the slope of the pooled regression over
    all member coin-bars labelled 2019-07-01 or later, with errors from 30 time blocks that
    allow coins to move together. The p-value is one-sided (slope above zero).

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.01

power:
  mde_train: 0.04
  mde_dev: 0.05
  note: >
    The signal is the same for every coin at a bar, so the pooled slope is in effect the
    regression of the members' average next-hour return on Bitcoin's last-hour return. On
    train from 2019-07-01 (30,678 bars) the standard deviation of Bitcoin's hourly return is
    0.80% and of the members' average next-bar return 1.09% (measured unconditionally; no
    lead-lag statistic was computed). With independent bars that gives a standard error of
    0.0078 and a minimum detectable effect of 0.020 on train, and 0.026 on dev (17,544 bars,
    same volatilities assumed). Hourly returns are fat-tailed (kurtosis 42 for Bitcoin) and
    their volatility clusters, so I double both: 0.04 and 0.05. The predicted 0.02 is half of
    that: a slope this small may be missed, and a rejection then means "below about 0.04",
    not "absent". Economically even 0.04 is 3 bps per standard deviation of Bitcoin's hourly
    return, against 12 to 25 bps per side of cost: this is a predictive claim only.

data:
  - binance/spot/1h
  - binance/universe
---

# H4001: Bitcoin's return over the last hour predicts the other members' return over the next hour

## Registered design

Written on 2026-11-19 before any run. The experiment ran on the synthetic Store only (`tests/test_crossmarket_tools.py`). Before registering I measured two unconditional standard deviations on train for the power calculation (above) and nothing else.

**Origin, honestly.** `literature`, but resting on abstracts the Literature scout could not open in full, with one positive claim whose sign and sampling interval the abstract does not state (Wang and Ngene), a mechanism from a paper whose sample dates are unknown (Guo et al.), and two published nulls at this very granularity. The registered direction is the one the diffusion mechanism implies. The stated expectation is small or zero.

**Timing.** The signal ends at the close of bar t; the forward return starts at the open of bar t+1, as the engine trades, and ends at the open of bar t+2. "The last hour" is one hour of time on the full hourly grid (`n-hour-return-on-the-hourly-grid.md`): the first bar after an outage has no signal. The bar after the signal may itself lie after an outage (26 runs of missing hours on train, none in 2022); those rows stay in, since the rule at bar t cannot know.

**Lagged-price artefacts, and the guard.** A coin whose last trade is old looks as if it followed Bitcoin late. Three things are fixed here against that. (1) The forward return starts at the next bar's open, a different trade from every price in the signal, so the signal and the return share no price and bid-ask bounce in either cannot tie them together; the close-to-close non-synchronicity is excluded by construction. (2) A coin has no signal at a bar in which it did not trade (zero quote volume), because its next open may be a carried price. What cannot be excluded without looking forward is a coin with no trade in bar t+1 (its open is then the previous close): 219 zero-volume member-hours on train (`hourly-bars-missing-during-outages.md`) of 1.4 million. (3) Three diagnostics are written into the run record and decide nothing: the same slope with one more bar between signal and return (Bitcoin's return over the hour before last), within tiers 1 and 2, and within tier 3. Reading fixed now: a positive primary slope that is absent within tiers 1 and 2 and present in tier 3 is suspect as stale prices of thin coins, and I will say so; slow diffusion and stale prices both fade when a bar is skipped, so that diagnostic bounds how long the effect lasts and cannot tell them apart.

**Evaluation start: 2019-07-01**, when the point-in-time universe first has 40 members (`universe-is-smaller-than-40-before-mid-2019.md`); before that the "other members" are 1 to 17 coins. It also puts the whole window after the sample of Sifat et al.

**Predicted size and dev rule.** No source gives a slope. 0.02 is my statement of "small": 2% of Bitcoin's hourly move. `min_size` 0.01 is half of that.

**The test was done wrongly if** the window does not start on 2019-07-01, the number of coin-bars is far from about 39 per bar (1.1 to 1.2 million on train), or the look-ahead check fails.

## Results

## Verdict
