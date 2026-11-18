---
id: H1001
title: Holding a coin only while its close is above its 20-day average beats holding every universe member, on Sharpe ratio after costs
family: time-series
origin: literature
claim: trading
status: registered

motivation: >
  Time-series momentum (trend): a coin's return is higher after its price closed above its own
  moving average than after it closed below, so holding it only in the first state gives a
  better risk-adjusted return than holding it always. Detzel et al. (sample to 2018-01-31)
  report for Bitcoin an annualised Sharpe ratio of 2.29 for the 20-day rule against 1.92 for
  buy-and-hold (1.90 against 1.45 in the second half of their sample) and 1.64 against 1.33
  for Ripple, with a maximum drawdown of 64 to 70 percent against 89.5 percent and about the
  same mean return: the gain is in risk. Liu and Tsyvinski (to 2018-05-31) find that Bitcoin's
  weekly return predicts its return one to three weeks ahead. Liu, Tsyvinski and Wu (to
  2018-12-31, cross-sectional) find momentum at one to four weeks and none at eight or more,
  in large coins and in the long leg. Hudson and Urquhart (to 2017-12-31) find the profit of
  moving-average rules on the long side. Against it, Wei et al. (to 2022-03-05, the only
  source that covers most of our train window) find that classic moving-average rules do not
  survive selection and that only a one-week price-to-average ratio keeps working, and none
  of the sources tests a per-coin rule across a 40-coin universe with changing membership.
  All of this is taken from the Literature scout's notes in research/literature/time-series.md
  (sections 1a, 1b, 1c, 2a, 2b, 3); every sample ends before 2023.
sources:
  - "Detzel, A., Liu, H., Strauss, J., Zhou, G. and Zhu, Y. (2021). Learning and predictability via technical analysis: Evidence from bitcoin and stocks with hard-to-value fundamentals. Financial Management 50(1), 107-137. Read by the scout as the 2018 working paper (Tables 6, 8, 9). Sample: Bitcoin daily 2010-10-27 to 2018-01-31, Ripple 2013-11-12 to 2018-01-31. https://doi.org/10.1111/fima.12310"
  - "Liu, Y. and Tsyvinski, A. (2021). Risks and Returns of Cryptocurrency. Review of Financial Studies 34(6), 2689-2727. Read by the scout as NBER Working Paper 24877 (Tables 14 to 18). Sample: Bitcoin 2011-01-01 to 2018-05-31, Ripple and Ethereum to 2018-05-31. https://www.nber.org/papers/w24877"
  - "Liu, Y., Tsyvinski, A. and Wu, X. (2022). Common Risk Factors in Cryptocurrency. Journal of Finance 77(2), 1133-1177. Read by the scout as NBER Working Paper 25882 (Table 4, Section 3.2). Sample: 1,707 coins, weekly, 2014 to 2018-12-31. Cross-sectional, used for the horizon only. https://www.nber.org/papers/w25882"
  - "Hudson, R. and Urquhart, A. (2021). Technical trading and cryptocurrencies. Annals of Operations Research 297, 191-220. Sample: Bitcoin, Litecoin, Ripple, Ethereum, daily, to 2017-12-31 (out-of-sample check to 2018-06-30). https://link.springer.com/article/10.1007/s10479-019-03357-1"
  - "Wei, M., Kyriakou, I., Sermpinis, G. and Stasinakis, C. (2024). Cryptocurrencies and Lucky Factors: The value of technical and fundamental analysis. International Journal of Finance and Economics 29(4), 4073-4104. Sample: twelve large coins, daily, 2015-08-08 to 2022-03-05. Evidence of decay. https://doi.org/10.1002/ijfe.2863"
  - "Moskowitz, T. J., Ooi, Y. H. and Pedersen, L. H. (2012). Time series momentum. Journal of Financial Economics 104(2), 228-250. Sample: 58 futures and forwards, 1965 to 2009, no crypto. The parent result and the name. https://doi.org/10.1016/j.jfineco.2011.11.003"

prediction:
  direction: positive
  size: "about 0.25"
  unit: difference in annualised net Sharpe ratio (strategy minus benchmark)

primary_test:
  experiment: trading.experiments.h1001
  granularity: 1d
  params:
    lookback_days: 20
    rebalance: bar
    benchmark: equal_weight_same_schedule
    start: "2019-07-01"
  description: >
    At the close of every daily bar each point-in-time universe member that has a bar (the
    membership in force when the bar closes, market.member_next) gets an equal slot of 1/N.
    A slot holds its coin when the coin's close is above the mean of its last 20 closes (the
    bar's own close included), and cash otherwise. The benchmark is the same slots with
    every one filled: the equal-weight universe rebalanced at every bar. Both run through
    the same engine (trade at the next open) and the library's costs from the first bar of
    the data. The estimate is the strategy's annualised net Sharpe ratio minus the
    benchmark's over the bars of the segment labelled 2019-07-01 or later
    (evaluate_strategy, statistic sharpe). The p-value is one-sided (strategy above
    benchmark) from the paired circular block bootstrap of that difference, 2000 draws,
    seed 1001. The same difference at double cost is reported alongside.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5
    min_size: 0.2

power:
  mde_train: 1.03
  mde_dev: 1.36
  note: >
    From `uv run trading research mde sharpe-difference --correlation 0.7 --start 2019-07-01`:
    train 3.51 years, standard error 0.41, minimum detectable effect 1.03; dev 2.00 years,
    standard error 0.55, minimum detectable effect 1.36. The predicted 0.25 is a quarter of
    what train detects with 80% power, so this test is underpowered and was known to be
    before it ran. If the true difference is 0.25 the chance of a train p-value at or below
    0.10 is roughly a quarter (my arithmetic from the standard error). A rejection will
    therefore mean "not large enough to see in 3.5 years", not "absent"; and a train
    estimate large enough to pass (about 0.5 or more) would probably overstate the true
    effect. The correlation of 0.7 is an assumption, not a measurement; see "Registered
    design" for why, and for the figures at 0.8 and 0.87.

data:
  - binance/spot/1d
  - binance/universe
---

# H1001: holding a coin only while its close is above its 20-day average beats holding every universe member

## Registered design

Written on 2026-11-18, before the experiment was run on any real data. The experiment module was exercised on the synthetic Store only (`tests/test_h1001.py`).

### The rule

At the close of each daily bar `t`:

1. The eligible coins are the point-in-time universe members in force when the bar closes (`market.member_next`) that have a bar at `t`. There are `N` of them. Each gets a slot of `1/N`.
2. A coin's signal is on when `close[t] > mean(close[t-19 .. t])`: its close is strictly above the simple mean of its last 20 daily closes, the signal bar's own close included.
3. The target weight is `1/N` for an eligible coin whose signal is on and 0 for every other coin. The rest of the portfolio is cash at 0%.
4. The target is traded at the open of bar `t+1`, which for daily bars is the instant bar `t` closes.

A slot whose coin is flat stays in cash; it is not shared out among the coins that are on. So the weights lie between 0 and `1/N`, a row sums to the share of eligible coins whose signal is on, and the strategy is long or flat coin by coin, which is the form of the published rule.

### Where each choice comes from

- **Signal: price above its own moving average.** The scout's notes rank this as the best-supported long-or-flat pattern (section 1a, Detzel et al.: long when the price is above its L-day moving average, otherwise Treasury bills, never short). The alternative, the sign of the past return, has weaker support as a trading rule: the scout's reading of Liu and Tsyvinski's quintile tables is that they support "the weeks after a very strong week are better than average", not "the sign of last week's return tells you whether to hold" (section 2a). Whether the paper's average includes the signal day's own price the notes do not say; including it is the usual definition of a simple moving average and is the convention chosen here.
- **Lookback: 20 days.** The literature does not pin this down. The notes ("Lookback for a simple long-or-flat trend rule") narrow it to roughly 7 to 28 days and say so plainly. 20 days is a choice from the middle of that range, made before looking at any data, with two partial supports that the scout read in full: the 20-day rule in Detzel et al. (Sharpe 2.29 against 1.92; turnover 7.95 percent a day; break-even one-way cost 2.36 percent), and the three-week peak of cross-sectional momentum in Liu, Tsyvinski and Wu (Table 4). A third, the 20-day rule of Grobys, Ahmed and Sapkota, is an unverified lead (abstract only) and is not relied on. The case against 20 and for about 7 is Wei et al., the only source reaching 2022, in which only the one-week ratio survives; the case against 7 is cost, since the 5-day rule trades 21.75 percent a day against 7.95 (Detzel et al., Table 8). No value other than 20 was or will be tried under this id.
- **Rebalancing: every bar.** The literature does not pin this down either: no source compares frequencies for one signal ("Rebalancing frequency" in the notes). Daily evaluation, switching whenever the signal flips, is the published convention for moving-average rules (Detzel et al.; Hudson and Urquhart), and it is taken here because it is the convention of the source the rule comes from. Weekly would be the convention of the return-sign papers, which is not this rule.
- **Benchmark: the equal-weight universe rebalanced at every bar (`equal_weight_same_schedule`).** The published comparison is the rule against buy-and-hold of the same coin. Its portfolio form is every slot filled against slots filled only when the signal is on. Both sides then hold the same coins in the same slots, are re-equalised on the same days and pay the same costs for that; they differ by the filter and nothing else. Against buy-and-hold BTC or the monthly equal-weight universe the difference would also contain coin selection and rebalancing frequency, which this hypothesis does not claim anything about. Those two and cash are in every run record as reference benchmarks and will be quoted, but they do not decide anything.
- **Statistic: difference in net Sharpe ratio.** The sources find the gain in risk, not in mean return (Detzel et al., Table 6: mean excess return slightly below buy-and-hold for every window; Hudson and Urquhart, Table 7). A test on mean return would test something the literature did not find.
- **Evaluation start: 2019-07-01.** From the Data steward's note `universe-is-smaller-than-40-before-mid-2019.md`: the universe has no member before 2017-10-01, 2 until the end of 2017, 5 to 18 during 2018 and reaches 40 only on 2019-07-01. A 1/N rule is a different portfolio in each of those stretches, and the claim here is about a filter across the 40-member universe. The start also keeps the whole train window after the end of the main source's sample (2018-01-31). It costs power: 3.5 years instead of 5.25. The engine still runs from the first bar, so the positions held on 2019-07-01 are the ones the rule would have. On dev the start changes nothing.

### Conditions taken from the Data steward's notes

- **Short history: flat.** The average needs a close on each of the last 20 bars; without that the signal is off (`new-members-have-short-history.md`). Membership itself needs a bar on each of the 30 days before the reconstitution, so with a 20-day lookback a member should always have a full lookback at its first decision, and this condition should remove no member-days. That is an inference from the rule as the notes describe it, not something I measured. The market panels carry a coin's bars from before it was a member, so the lookback reaches back past the month it joined.
- **A NaN signal means flat.** A coin without a bar at `t` has no slot (it is not eligible), and a missing close anywhere in the lookback turns the signal off; the last value is never carried forward (`members-stop-trading-mid-month.md`). The engine sells a coin that stopped trading at its last close, which assumes the holder got out before the halt; a target on a coin with no bar at the next open is dropped into cash and counted in `dropped_weight`.
- **Decisions at a close use `market.member_next`**, so the last close of a month already targets the next month's members and never a coin that is about to leave. `evaluate_strategy` refuses any weight on a non-member.
- **Thin low ranks in 2019 and 2020.** In those years rank 40 traded 0.3 to 1.6 million USDT a day and 28 of 40 slots are tier 3 (`low-ranked-members-were-thin-before-2021.md`), while the cost model charges one slippage per tier in every year. A daily rule trades those coins often, so for 2019 and 2020 the double-cost run is closer to a realistic cost than to a stress test. If the estimate is positive at normal cost and not at double cost, I will not call it an effect that survives costs. Nothing here says anything about capacity.
- **Redenominations and renames.** A 20-day lookback from a coin's first membership does not cross either redenomination in the train members' histories (`daily-bars-agree-with-raw-files-and-hourly-bars.md`: BTCST's is 7 months before its first membership, COCOS's 10 months before its return to the universe). A renamed coin is a new pair with at least 30 bars when it joins.

### Costs and the predicted size, worked out before running

- **Turnover times cost.** If every slot flips as often as Bitcoin's 20-day rule did in Detzel et al. (7.95 percent of the position a day), the strategy trades about 8 percent of the portfolio a day one way. A slot's cost per side averages about 22 bps (2 slots at 12 bps, 10 at 15, 28 at 25; my arithmetic), so the filter costs roughly 1.7 bps a day, about 6 percent a year, and 13 percent a year at double cost. Altcoins may flip more often than Bitcoin did; that is unknown. Re-equalising the slots every day costs extra on both sides, the benchmark on all 40 slots and the strategy on those that are on.
- **Predicted size.** The published gain in gross Sharpe ratio for the 20-day rule is 0.37 (Bitcoin, full sample), 0.45 (Bitcoin, second half) and 0.31 (Ripple). A cost of 6 percent a year is 0.1 to 0.2 of Sharpe ratio if the strategy's volatility is 30 to 60 percent a year (an assumption). That gives 0.2 to 0.3 net if the effect kept its published strength across 40 coins after 2018. The one source that covers those years reports decay, so a smaller number would not surprise; the prediction registered is "positive, about 0.25".
- **Correlation assumed for the minimum detectable effect: 0.7.** The strategy is the benchmark with some slots switched off. If all slots switched together, half the time and independently of the size of returns, the correlation of strategy and benchmark returns would be the square root of one half, 0.71. Forty slots switching at different times make the invested share move smoothly between 0 and 1, which raises it (0.87 if that share were uniform on 0 to 1 and the coins moved as one; my arithmetic). I take the low end, which gives the larger, more cautious minimum detectable effect: 1.03 on train and 1.36 on dev. At 0.8 it would be 0.84 and 1.11, at 0.87 0.68 and 0.90. In every case the predicted 0.25 is well below it.

### What I knew before registering

- I did not load, plot or summarise any train or dev data, and did not run the rule on real data. The experiment module ran on the synthetic Store only.
- `research/LOG.md` reports two train numbers seen while the engine was checked: buy-and-hold BTC from 2017-08 with a Sharpe ratio of 0.72, and the monthly equal-weight universe with 0.52, a maximum drawdown of -92% and costs of 1.2% a year. I read them before writing this file. No choice above depends on them.
- The model writing this has background knowledge of crypto markets after 2022. None of it is used as a reason for anything here; every reason given is a cited source with its sample end, or a Data steward note measured on train.

### What would count as the test having been done wrongly

- The train window in the run record does not start on 2019-07-01 or does not end on 2022-12-31 (1,280 bars).
- `average_weight_invested` is 0 or equals the benchmark's: the filter never or always on.
- `dropped_weight` is more than a few percent of one day's portfolio in total: targets on coins that could not be bought.
- The harness's look-ahead check fails, or `evaluate_strategy` refuses a weight on a non-member.
- The benchmark's metrics do not describe a fully invested portfolio.

If any of these happens the run is not evidence. A mistake in the experiment module found after a run is not repaired under this id: this file stays as it is and a new hypothesis is registered.

## Results

Not run yet.

## Verdict

Not run yet.

## Skeptic review

Added by the Skeptic, if the hypothesis is reviewed.
