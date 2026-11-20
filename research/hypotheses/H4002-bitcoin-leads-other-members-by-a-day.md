---
id: H4002
title: Bitcoin's return over the last day predicts the other universe members' return over the next day, with the same sign
family: cross-market
origin: literature
claim: predictive
status: registered

motivation: >
  The daily form of H4001: if information diffuses from Bitcoin to the other coins over more
  than a day, their next daily return has the sign of Bitcoin's last one. The Literature
  scout could read ABSTRACTS ONLY for this question (research/literature/cross-market.md,
  "Unverified leads", sub-angle 1). For: Guo et al. (2024, Binance data, believed daily) find
  that lagged returns of other coins predict a coin's return and attribute it to slow
  diffusion of information, the mechanism behind the positive sign registered here; their
  sample dates are unknown, so they are cited for the mechanism and not as clean evidence.
  Soiman et al. (2022 preprint, so a sample ending by early 2022) are reported, in a search
  summary the scout did not confirm, to find a positive coefficient of 0.87 on the one-week
  lagged Bitcoin return for an index of DeFi tokens. Against: Sifat et al. (2019; hourly and
  daily, 2017-08 to 2018-09) find two-way causality between Bitcoin and Ethereum that
  traders can barely exploit, and Bacao et al. (2018) find that transmission happens within
  the period and that what lagged feedback there is runs mainly from the other coins to
  Bitcoin. The direction is the reading of the diffusion story; the expectation is small or
  zero. No train data on the relation was looked at before registration.
sources:
  - "Guo, L., Sang, B., Tu, J. and Wang, Y. (2024). Cross-cryptocurrency return predictability. Journal of Economic Dynamics and Control 163: 104863. Abstract only. Binance data; SAMPLE DATES UNKNOWN (working paper December 2021), so used for the mechanism only. https://doi.org/10.1016/j.jedc.2024.104863"
  - "Soiman, F., Dumas, G. and Jimenez-Garces, S. (2022). The return of (I)DeFiX. arXiv:2204.00251. Abstract only; the coefficient on lagged Bitcoin is from a search summary, unconfirmed. Submitted 2022-04, so the preprint's sample ends by then. https://arxiv.org/abs/2204.00251"
  - "Sifat, I. M., Mohamad, A. and Mohamed Shariff, M. S. B. (2019). Lead-Lag relationship between Bitcoin and Ethereum: Evidence from hourly and daily data. Research in International Business and Finance 50, 306-321. Abstract only. Sample: 2017-08 to 2018-09. A published null. https://doi.org/10.1016/j.ribaf.2019.06.012"
  - "Bacao, P., Duarte, A. P., Sebastiao, H. and Redzepagic, S. (2018). Information Transmission Between Cryptocurrencies: Does Bitcoin Rule the Cryptocurrency World? Scientific Annals of Economics and Business 65(2), 97-117. Abstract of the working paper only; published 2018. A published null. https://doi.org/10.2478/saeb-2018-0013"

prediction:
  direction: positive
  size: "about 0.05"
  unit: pooled slope (a member's return over the next daily bar per unit of Bitcoin's return over the last day; 0.05 means 5% of Bitcoin's move follows)

primary_test:
  experiment: trading.experiments.h4002
  granularity: 1d
  params:
    leader: BTCUSDT
    lookback_bars: 1
    skip_bars: 0
    horizon_bars: 1
    start: "2019-07-01"
  description: >
    At the close of every daily bar t the signal of each point-in-time universe member other
    than Bitcoin is Bitcoin's close-to-close return over bar t (NaN for a coin whose own bar
    t is missing or had no trade). It is set against the coin's return from the open of bar
    t+1 to the open of bar t+2 (evaluate_predictor, method panel, horizon 1): the slope of
    the pooled regression over all member coin-bars labelled 2019-07-01 or later, with errors
    from 30 time blocks that allow coins to move together. The p-value is one-sided (slope
    above zero).

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.02

power:
  mde_train: 0.14
  mde_dev: 0.19
  note: >
    As in H4001 the pooled slope is in effect the regression of the members' average next-day
    return on Bitcoin's last daily return. On train from 2019-07-01 (1,280 bars) the standard
    deviation of Bitcoin's daily return is 3.8% and of the members' average next-day return
    5.2% (measured unconditionally; no lead-lag statistic was computed). Independent days
    give a standard error of 0.038 and a minimum detectable effect of 0.094 on train and
    0.124 on dev (731 bars, same volatilities assumed); multiplied by 1.5 for fat tails
    (kurtosis 11) and volatility clustering: 0.14 and 0.19. The predicted 0.05 is about a
    third of what train can detect, so this test is underpowered and known to be: a
    rejection means "below about 0.14", which still allows an effect of 0.5% a day after a
    10% Bitcoin day.

data:
  - binance/spot/1d
  - binance/universe
---

# H4002: Bitcoin's return over the last day predicts the other members' return over the next day

## Registered design

Written on 2026-11-19 before any run. The experiment ran on the synthetic Store only (`tests/test_crossmarket_tools.py`). Before registering I measured two unconditional standard deviations on train for the power calculation and nothing else.

**Origin, honestly.** `literature` on abstracts only, as in H4001: a mechanism from a paper with unknown sample dates (Guo et al.), an unconfirmed weekly coefficient (Soiman et al.), and two published nulls of which one covers daily data. The registered direction is the one the diffusion mechanism implies.

**Timing.** Daily bars close at 00:00 UTC for every coin, so signal and return meet at one instant: the signal ends at the close of bar t and the forward return runs from the open of bar t+1 (the same instant) to the open of bar t+2. No member misses a daily bar while it trades.

**Lagged-price artefacts.** At daily granularity a stale last trade is minutes old against a day of movement, so the artefact that matters for H4001 is small here; the same guards apply anyway (the return starts at the next bar's open, no signal for a coin without a trade in bar t), and the same three diagnostics are recorded and decide nothing: one more day skipped, tiers 1 and 2, tier 3. In 2019 and 2020 the lowest ranks traded under a million USDT a day (`low-ranked-members-were-thin-before-2021.md`); a slope found in tier 3 only would be read with that in mind.

**Evaluation start: 2019-07-01**, when the point-in-time universe first has 40 members.

**Predicted size and dev rule.** No source gives a daily slope. 0.05 is my statement of "small"; `min_size` 0.02.

**The test was done wrongly if** the window does not start on 2019-07-01 with 1,280 train bars, the number of coin-bars is far from 39 per bar, or the look-ahead check fails.

## Results

## Verdict
