---
id: H1001
title: Holding a coin only while its close is above its 20-day average beats holding every universe member, on Sharpe ratio after costs
family: time-series
origin: literature
claim: trading
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
status: not replicated
skeptic:
  verdict: audited
  date: '2026-11-19'
  reason: 'The recorded status not replicated is sound: registration precedes both runs, the
    experiment never changed, dev ran once, and the dev estimate of +0.124 is below the pre-declared
    +0.331. The train estimate of +0.661 is computed correctly (an independent loop gives
    +0.6612; no look-ahead; it holds across lookbacks of 15 to 50 days, years, coins, double
    cost and a one-bar delay) but it is weak evidence: one test through a one-sided 10% gate,
    where a true null that passes averages the same +0.67.'
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

Added on 2026-11-18 by the Researcher. Every number is quoted from the run records `research/runs/2026-11-18/H1001-r01.json` (train) and `H1001-r02.json` (dev) unless marked "(my arithmetic)". Both runs used binance/spot/1d id 2d6763395242 and binance/universe id 88f9a7cf72c7, and both passed the harness's look-ahead check at three cuts.

### The primary test

| | Train, H1001-r01 | Dev, H1001-r02 |
|---|---:|---:|
| Window | 2019-07-01 to 2022-12-31, 1,280 bars | 2023-01-01 to 2024-12-31, 731 bars |
| Estimate (difference in net Sharpe ratio) | +0.661 | +0.124 |
| One-sided p | 0.0440 | 0.4158 |
| q (Benjamini-Hochberg, one literature hypothesis registered) | 0.0440 | not used on dev |
| Bootstrap standard error; 90% interval | 0.381; +0.03 to +1.29 | 0.485; -0.64 to +0.92 |
| Estimate at double cost (one-sided p) | +0.482 (0.0990) | -0.089 (0.5792) |
| Minimum detectable effect, registered | 1.03 | 1.36 |
| Predicted | about +0.25 | about +0.25 |
| Required on dev: the larger of half the train estimate and 0.2 | | +0.331 |

### Strategy and benchmark inside the window

| | Train: strategy | Train: benchmark | Dev: strategy | Dev: benchmark |
|---|---:|---:|---:|---:|
| Net Sharpe ratio | 0.990 | 0.329 | 0.938 | 0.814 |
| Net Sharpe ratio at double cost | 0.776 | 0.294 (my arithmetic) | 0.677 | 0.766 (my arithmetic) |
| Compound annual growth | +41.6% | -16.4% | +34.1% | +38.6% |
| Volatility a year | 45.9% | 97.5% | 39.8% | 72.6% |
| Maximum drawdown | -53.0% | -91.5% | -46.9% | -59.6% |
| Maximum drawdown at double cost | -58.5% | not in the record | -50.7% | not in the record |
| One-way turnover, times the portfolio a year | 22.4 | 7.5 | 23.5 | 7.5 |
| Cost a year | 9.9% | 3.5% | 10.4% | 3.5% |
| Average weight invested | 0.434 | | 0.465 | |

The benchmark's Sharpe ratio at double cost is the strategy's at double cost minus the double-cost estimate.

### The three reference benchmarks (they decide nothing)

| Net Sharpe ratio (compound annual growth, maximum drawdown) | Train window | Dev window |
|---|---:|---:|
| Buy-and-hold BTC | 0.540 (+12.8%, -76.6%) | 2.018 (+137.6%, -26.2%) |
| Equal-weight universe, rebalanced monthly | 0.465 (-4.2%, -89.9%) | 0.834 (+40.7%, -60.2%) |
| Cash | 0 | 0 |
| Strategy minus buy-and-hold BTC (my arithmetic, no test) | +0.450 | -1.079 |
| Strategy minus monthly equal weight (my arithmetic, no test) | +0.525 | +0.105 |

### Checks against "what would count as the test having been done wrongly"

- **Windows**: as registered in both runs (first and last bar above).
- **Filter neither always on nor always off**: the average weight invested is 0.434 on train and 0.465 on dev.
- **Look-ahead check and members only**: passed; `evaluate_strategy` refused nothing.
- **Benchmark fully invested**: on train its invested weight averages 0.9999 and is never below 0.975 (measured with a scratch script on train data after the train run; the dev benchmark I cannot inspect, its volatility and turnover look like a fully invested portfolio).
- **Dropped weight: at the edge of what I registered, and I have to say so.** The train record has `dropped_weight` 0.075 and the dev record 0.125. I had written "more than a few percent of one day's portfolio in total" as a sign of a wrong test without giving a number. After the train run and before the dev run I looked at train data to find the cause (the only time I loaded train data; a scratch script that recomputed the panel and the engine's dropped targets, nothing recorded). The 0.075 is three single slots of 1/40, one day each: ERDUSDT on 2020-09-01, NPXSUSDT on 2021-04-06 and BTTUSDT on 2022-01-18. Each is the day after the pair's last bar: the signal was on at the pair's final close, the target could not be bought the next day, and the engine closed the position at that final close. That is the case the registered design describes under "A NaN signal means flat", not a rule buying what cannot be bought, so I judged the run sound and went on to dev. A strict reader may hold that 7.5% is "more than a few percent" and that by my own wording the runs are not evidence; the criterion was badly worded and I am not the one to settle it. The dev record's number is cumulative from the first bar of the data, so 0.05 was added in 2023 and 2024 (my arithmetic), presumably two more such slots; I cannot check that, because dev data cannot be loaded.
- **Short history**: the same script counted eligible member-days without a full 20-bar lookback on train. There is one, BCCUSDT on 2018-11-20, before the window. Inside the train window the condition removed nothing, as inferred at registration.

### What else the records show

- **Costs were higher than I worked out before running.** I expected about 6% a year from the filter's switches; the record shows 9.9% on train and 10.4% on dev, with the benchmark's own daily re-equalising at 3.5%. Doubling costs lowers the estimate by 0.18 on train and by 0.21 on dev (my arithmetic).
- **The correlation assumed for the minimum detectable effect was about right.** The bootstrap standard errors (0.381 and 0.485) are a little below the 0.41 and 0.55 computed from a correlation of 0.7; put back into the same formula they imply about 0.75 on both segments (my arithmetic).
- **The benchmark with daily re-equalising is weaker on train than the monthly one** (Sharpe 0.329 against 0.465, growth -16.4% against -4.2% a year), and about equal on dev (0.814 against 0.834). The registered comparison is against the daily one, for the reason given in the design. Measured against the monthly equal-weight reference the train difference would be 0.525 instead of 0.661.

## Verdict

**Status: `not replicated`**, as printed by `uv run trading research status H1001` on 2026-11-18:

```
H1001  not replicated  ...
       train p = 0.0440, q = 0.0440 (passes false-discovery control at 10%)
       dev estimate +0.1244 against a required +0.3306 (train +0.6611)
```

What happened. On train the filter raised the net Sharpe ratio from 0.33 to 0.99, an estimate of +0.66 with a one-sided p of 0.044, and it kept most of that at double cost (+0.48, p 0.099). With one literature hypothesis registered, q equals p and the hypothesis became a candidate. On dev the estimate was +0.12 (p 0.42): the predicted sign, but 19% of the train estimate where the rule registered beforehand asks for 50%, and below the registered minimum of 0.2. At double cost the dev estimate is negative (-0.09). The hypothesis did not replicate.

What it means.

- **The train estimate was probably too large.** I predicted about 0.25 and wrote at registration that a train estimate big enough to pass would probably overstate the effect. Train gave 0.66 and dev 0.12. The dev number is the less selected of the two.
- **On dev the rule did what the literature says such rules do, and no more.** It cut volatility (40% against 73% a year) and drawdown (-47% against -60%) and gave up return (34% against 39% a year), for a Sharpe ratio 0.12 higher at normal cost and 0.09 lower at double cost. Following what I registered about thin coins and costs, I do not call that an effect that survives costs.
- **Dev cannot tell a small effect from none.** Its standard error is 0.49, so +0.12 is compatible with zero, with the 0.25 I predicted, and (at 1.1 standard errors, my arithmetic) not far from the train estimate either. "Not replicated" here means the replication rule set before the run was not met. It does not show that the effect is absent, and the minimum detectable effect on dev (1.36) says no dev result of plausible size could have shown that it is present.
- **It is not a way to beat holding BTC.** In the dev window buy-and-hold BTC has a Sharpe ratio of 2.02 against the strategy's 0.94. The hypothesis never claimed otherwise (its benchmark is the same coins without the filter), but a reader looking for a strategy should see that line.
- **The size of the train result depends on the benchmark's schedule.** 0.14 of the 0.66 is the gap between daily and monthly re-equalising of the equal-weight universe on train (my arithmetic from the reference benchmark).

How sure. The train result is one test at p 0.044 with a 90% interval from +0.03 to +1.29: weak evidence of a positive effect of unknown size in 2019 to 2022, in a sample where the benchmark lost 91% at its worst. Its q-value will rise when more literature hypotheses are registered, and the status may then read `rejected` instead of `not replicated`. The dev result is one look at two years. Both rest on a cost model that is at its most optimistic for the low-ranked coins of 2019 and 2020, and on the open question about dropped weight above. I have not re-derived either number by a second route, varied any parameter, or split the result by year or by coin; that is a Skeptic's work, and nothing here was reviewed.

What this does not test, and will not be added here: another lookback (the one-week window of Wei et al.), weekly evaluation, the rule on BTC alone, or another benchmark. Each would be a new hypothesis with a new id, counted in the false-discovery total, and one prompted by these results would have origin `exploration`.

## Skeptic review

Added on 2026-11-19 by the Skeptic. H1001 is `not replicated`, so this is an audit: the verdict is `audited` and changes no status. It asks two questions. (a) Is the train result that made H1001 a candidate real, or an artefact? (b) Is the recorded status sound?

Everything here was run on train data only, through `trading.research.train_data()` and `trading.research.harness.replay`. Dev numbers are quoted from run record H1001-r02 and were not recomputed; there is no way to and there should not be. I read the front matter, the two run records, the experiment module and the library code it calls first, and the Researcher's Results and Verdict only after checks 1 to 7 were done. **Every variation below is an attack. None is registered, none is a better version of anything, and none of these numbers is evidence for any rule.** "Estimate" always means the difference in annualised net Sharpe ratio over 2019-07-01 to 2022-12-31 (1,280 bars) unless a row says otherwise.

### Verdict

**Audited: the recorded status `not replicated` is sound.** The registration commit precedes both runs, the experiment was never changed, dev ran once on the registered specification, and the dev estimate of +0.124 is below the pre-declared requirement of +0.331 (the larger of half the train estimate and 0.2).

**The strongest finding.** The train estimate of +0.661 is computed correctly and I could not break it: a loop that shares no code with the engine gives +0.6612, there is no look-ahead, and it holds across lookbacks of 15 to 50 days, every calendar year left out in turn, every coin left out in turn, double cost and a one-bar delay. What it lacks is weight as evidence. It is one test that passed a gate which, with a single registered hypothesis, is a one-sided test at 10%; a true null that passes that gate has an average train estimate of +0.67, which is the number observed. And the dev rule that then failed it would also fail a true effect of the predicted size 57% of the time. So the train result is not an artefact, the status is the right output of the registered rules, and neither run settles whether the effect exists.

Weak or impossible checks: nothing on dev could be checked beyond the record (its two dropped slots, its benchmark, its sub-periods); the sample ends and numbers of the sources are taken from the Literature scout's notes, not from the papers; what the Researcher's scratch script between the runs did cannot be verified, because it was not kept; the cost model's flat slippage per liquidity tier for the thin coins of 2019 and 2020 was stressed (check 6) but not measured against order books.

### 1. Re-derivation: passes

- `replay("H1001")` against H1001-r01: estimate 0.6611286790380324 and p 0.04397801099450275 in both, n 1,280, double cost +0.4820 (p 0.0990) in both, and every number in `metrics` that the record holds is identical to the last digit. The current code adds two fields the record lacks (see "Infrastructure").
- Second route: a plain Python loop over all 1,963 daily bars that holds units of each coin and USDT, decides at each close from the last 20 closes summed by hand, takes the membership of the following day from `market.member` (not `member_next`), fills at the next open, charges 12, 15 or 25 bps per side by tier out of cash, and computes the Sharpe ratio by hand. It uses the library only to read the open, close, member and tier arrays of the train market.

| | Engine (record) | Loop |
|---|---:|---:|
| Strategy net Sharpe ratio | 0.99041 | 0.99072 |
| Benchmark net Sharpe ratio | 0.32928 | 0.32947 |
| Estimate | 0.66113 | 0.66125 |
| Estimate at double cost | 0.48204 | 0.48231 |
| Strategy total return in the window | +239.0% | +239.3% |
| Strategy cost a year | 9.85% | 9.86% |
| Dropped weight, strategy | 0.075 | 0.075 |

The difference of 0.0001 has one cause: the engine takes costs as a proportional cut of the whole portfolio, the loop pays them from cash. Nothing else differs.

### 2. Look-ahead and leakage: passes

Read line by line: `h1001.panel`, `h1001.slots`, `equal_weight`, `rebalance_labels`, `evaluate_strategy`, `to_weights`, `run_backtest`, `load_market`, `membership_panel`, `build_universe`.

| Input | Why it is knowable at the close of bar t |
|---|---|
| `close.rolling(20, min_periods=20).mean()` | a trailing window, bars t-19 to t; any missing close gives NaN and the comparison is false |
| `close[t] > average[t]` | the bar's own close |
| `member_next[t]` (slots of strategy and benchmark) | the reconstitution in force at t plus one day; a reconstitution dated D reads bars labelled before D (the Data steward's note measures this at 63 of 63). On the last bar of a month it needs that bar's own volume, at the instant it closes. Checked here: `member_next[t]` equals `member[t+1]` on every train row but the last, and differs from `member[t]` only on 56 month-end rows |
| `isfinite(close[t])` and the count N | the bar's own close |
| Benchmark weights | the same `slots` function, nothing else |
| Cost per side | the tier at the label of the bar whose open is traded, set before that bar opened |
| Engine prices | open of t+1, or the last close for a coin without a bar (forward fill only) |
| Evaluation window, bootstrap block | fixed dates; the block length is chosen from the whole return series, which affects inference only |

No whole-sample mean, rank or standard deviation enters the weights. Measured: the panel recomputed on the market truncated at 308 cuts (every seventh bar and every month end) leaves every earlier row bit-identical; multiplying every price after a cut by random noise leaves the rows up to the cut identical (4 cuts) and changes the later ones (control). No weight sits on a non-member or on a coin without a close. The benchmark's row sum is 1 on every bar of the window, over 39 or 40 coins. Open of t+1 against close of t for members: median 0.02% apart, so "next open" is the same instant. As a control for what a leak would look like, shifting the weights one bar earlier (the signal of t+1 used at t) gives an estimate of +6.85; the registered alignment gives +0.66.

One oddity, harmless here: on the final bar of the train data (2022-12-31) `member_next` is December's membership, because the universe table is cut at the segment end; the same row in the dev market holds January's. No trade follows that row on train.

### 3. Neighbouring parameters: passes (20 is on a plateau)

| Lookback (days), daily decisions | 5 | 7 | 10 | 15 | 19 | **20** | 21 | 22 | 25 | 30 | 40 | 50 | 60 | 100 | 200 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Estimate | +0.23 | +0.37 | +0.48 | +0.65 | +0.67 | **+0.66** | +0.67 | +0.68 | +0.66 | +0.76 | +0.82 | +0.60 | +0.45 | +0.16 | 0.00 |
| One-sided p | 0.22 | 0.11 | 0.06 | 0.04 | 0.03 | **0.04** | 0.04 | 0.03 | 0.04 | 0.02 | 0.02 | 0.06 | 0.11 | 0.32 | 0.51 |
| At double cost | -0.22 | +0.01 | +0.19 | +0.44 | +0.48 | **+0.48** | +0.50 | +0.51 | +0.50 | +0.63 | +0.71 | +0.50 | +0.37 | +0.10 | -0.03 |

The registered value is neither the best nor the worst of its neighbourhood; the estimate degrades gradually on both sides, through cost on the short side (a 5-day rule pays 22% a year) and to nothing by 200 days. With `rebalance="week"` (strategy and benchmark both weekly): +0.42, +0.72, +0.75, **+0.70**, +0.72, +0.78, +0.76, +0.46, +0.16 for lookbacks 5, 10, 15, 20, 25, 30, 40, 60, 100. With decisions only at month ends the estimate is +0.04: the rule needs to act within weeks. Evaluation start moved: +0.74 from the first bar, +0.68 from 2018-01, +0.58 from 2019-01, **+0.66 from 2019-07**, +0.63 from 2020-01, +0.59 from 2020-07, +0.58 from 2021-01. The registered start is not a lucky one.

### 4. Sub-periods: weak (no year carries it, a handful of crash days carry much of it)

| Period | Bars | Strategy Sharpe | Benchmark Sharpe | Difference | Strategy return | Benchmark return | Invested | Estimate without this period |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 (from July) | 184 | -2.38 | -2.13 | -0.25 | -22% | -59% | 0.27 | +0.63 |
| 2020 | 366 | +2.16 | +1.53 | +0.62 | +159% | +162% | 0.55 | +0.60 |
| 2021 | 365 | +2.15 | +1.72 | +0.43 | +196% | +261% | 0.51 | +0.70 |
| 2022 | 365 | -1.45 | -1.64 | +0.19 | -43% | -86% | 0.32 | +0.62 |

2020 has the largest difference within a year, but leaving out any one year leaves +0.60 to +0.70, so no year carries it. By half-year the difference is positive in five of seven (largest: first half of 2020 +0.82, first half of 2021 +0.73; negative: second half of 2019 and of 2022). The whole-window +0.66 is about twice the bar-weighted mean of the yearly differences (+0.32): the rest comes from being 27% to 32% invested in the two falling periods and 51% to 55% in the two rising years.

By day it is concentrated. On the benchmark's ten worst bars (2020-03-12 at -44%, 2021-05-19 at -36%, 2022-05-11 at -28%, 2021-06-21, 2022-11-09, ...) the strategy was 27% invested on average against 43% overall. Without the benchmark's five worst bars the estimate is +0.28, without its ten worst +0.23. That needs a yardstick, because deleting crash days hurts any portfolio that is half in cash: the same deletion lowers a time-shifted placebo (check 7) by 0.14 and 0.24 on average, the real rule by 0.38 and 0.44, and 11% of placebos fall by as much as the real rule does. So the rule did step aside before the worst days more than chance timing would, and about a third of its estimate hangs on having done so five times in 3.5 years. This is what the bootstrap's standard error of 0.38 is made of.

### 5. Sub-universes: passes

| Universe (slots re-equalised over the coins that remain, both sides) | Estimate | Strategy Sharpe | Benchmark Sharpe |
|---|---:|---:|---:|
| All members (the registered test) | +0.66 | 0.99 | 0.33 |
| Without BTC and ETH | +0.67 | 0.97 | 0.31 |
| BTC and ETH only (tier 1) | +0.23 | 1.01 | 0.78 |
| Tier 2 only (10 coins) | +0.68 | 0.64 | -0.04 |
| Tier 3 only (28 coins) | +0.62 | 1.04 | 0.42 |
| Top 20 by trailing 30-bar quote volume | +0.54 | 0.80 | 0.27 |
| Bottom 20 | +0.71 | 1.04 | 0.33 |
| The 13 coins that are members at 36 or more of the 42 reconstitutions | +0.39 | 1.22 | 0.84 |
| All other coins | +0.70 | 0.83 | 0.12 |
| Without the 3 coins whose removal hurts most (LUNAUSDT-2022, BANDUSDT, FTMUSDT) | +0.57 | 0.86 | 0.30 |
| Without the 5 such coins | +0.53 | | |
| Without the 10 such coins | +0.44 | | |

Leaving out any single one of the 181 coins that are members in the window gives +0.62 (LUNAUSDT-2022) to +0.68; no coin and no handful carries it. Of the summed difference in gross return between the two portfolios, the best three coins contribute 27% and the best ten 61%; 114 of 181 coins contribute positively. Coin by coin (the rule on one coin against holding it while a member, 55 coins with a year or more of membership): positive for 43, median +0.23. Two things a reader should know. On BTC alone, the coin the main source is about, the difference on train is -0.06. And the estimate is larger among coins that pass through the universe than among its fixtures (+0.70 against +0.39): the equal-weight benchmark has to hold whatever just ranked on volume, and those coins did badly (benchmark Sharpe 0.12), so part of the gain is not holding recent entrants while they fade.

### 6. Costs and execution delay: passes on train (the sign survives both)

- Double cost, from the records: train +0.482 (p 0.099), dev -0.089 (p 0.579). On train the sign survives; on dev it does not.
- Cost multiples on train, both sides: +0.84 at zero cost, +0.66, +0.48, +0.30, +0.12 at one to four times, -0.06 at five. The break-even is about 4.7 times the library's costs. With the strategy alone at double cost and the benchmark at normal cost: +0.45. With every coin charged the tier-3 rate of 25 bps a side: +0.64; at 50 bps a side: +0.43. So the registered worry about thin tier-3 coins in 2019 and 2020 does not undo the train number.
- Execution delayed by one more bar (weights shifted one row; trade at the open two bars after the signal): +0.76 with both sides delayed, +0.77 with the strategy alone delayed (the loop of check 1 gives +0.757 for the first). Two bars: +0.58; three: +0.38; five: +0.35. The estimate does not depend on trading at the instant of the signal.
- In mirror, for the dev result: the two cost levels in H1001-r02 put the dev estimate at zero cost at about +0.34 by straight-line extrapolation (on train the same extrapolation gives +0.840 against a computed +0.840). So the dev shortfall is not an artefact of harsh costs: with no costs at all the dev estimate would have been on the line of +0.33, not clear of it.

### 7. Placebo: passes (the placebos do not work)

| Test | Real | Placebo mean (sd) | Share of placebos at or above the real |
|---|---:|---:|---:|
| Complement rule: hold a slot only while the close is not above the average | | -0.73 | |
| Signal rolled in time by 60 bars or more, all coins together (`circular_shift_test`, 500 draws) | +0.66 | -0.19 (0.34) | 0.004 |
| The same at zero cost | +0.84 | -0.05 (0.35) | 0.002 |
| The same on the 8 coins that are always members | +0.50 | -0.33 (0.39) | 0.014 |
| Each coin's slot switched by another coin's signal (`asset_permutation_test`, 500 draws, the 8 always-members) | +0.50 | +0.26 (0.07) | 0.002 |
| The same number of slots on at each bar, coins drawn at random (200 draws, zero cost) | +0.84 | +0.51 (0.06) | 0 |

A signal with the same persistence at the wrong time loses to the benchmark, as it should, so the test is not manufacturing the result. The last two rows are not placebos that should give zero: coins' trends are alike (two always-members have the same signal on 78% of bars), so another coin's signal carries about half of the effect and the count of coins that are on carries about 60% of it before costs. The rule is mostly a timer of the whole market by breadth, and partly a chooser of coins. Limits of these tools on this universe: `asset_permutation_test` needs a fixed set of coins (a column of the market is a coin that may not have traded yet), which is why it ran on eight; and the rolled signal is 38% invested where the real one is 43%, because a coin listed mid-window has no signal for the earlier bars rolled onto its membership. The placebo p of 0.004 answers a narrower question than the primary test (is the timing better than the same on-off pattern at another time, on these same 1,280 bars and these same crash days) and is not independent evidence.

### 8. Hindsight: passes, with two reservations

- Sources: all six samples end by 2022-03-05 (Detzel et al. 2018-01-31, Liu and Tsyvinski 2018-05-31, Liu, Tsyvinski and Wu 2018-12-31, Hudson and Urquhart 2017-12-31 with a check to 2018-06-30, Wei et al. 2022-03-05, Moskowitz et al. 2009). Wei et al. appeared in 2024 but its sample is inside train. The numbers quoted in the motivation match `research/literature/time-series.md`, which was committed (2435a62) eight minutes before the registration (68febdf). The sources flagged there for samples past 2022 are not cited. I compared against the scout's notes, not against the papers.
- Parameters: 20 days is named in the notes as a choice from the middle of a supported range of 7 to 28 days, with MA20 of Detzel et al. behind it; daily decisions are the convention of the source of the rule; the start date comes from a count of members; `min_ratio` 0.5 is the default and `min_size` 0.2 was registered. Check 3 agrees that nothing was tuned: 20 is unremarkable among its neighbours.
- Nothing in the registration leans on anything after 2022.
- Reservation one: before registering, the Researcher had read two train figures in the log, among them that the monthly equal-weight universe fell 92% at its worst. That is allowed, it is disclosed, and the design did not need it; but it is a fact about train that favours any rule that can sit in cash, and train is where a literature hypothesis is first tested.
- Reservation two, the same kind and not removable: a model that knows what crypto did in 2020 to 2022 proposes a filter whose train gain turns out to rest on the crashes of 2020 to 2022 (check 4). The train test of such a hypothesis is worth less than its p-value says. Dev is the cleaner look, though the same models know 2023 and 2024 as well.

### 9. Process: passes

- `uv run trading research check H1001`: "H1001 is registered (commit 68febdfa19, spec b3c513cc2e1c)". `status`: not replicated, train p 0.0440, q 0.0440, dev +0.1244 against a required +0.3306.
- Order, from `git log --follow`: literature notes 12:14:59, registration 68febdf 12:23:10 (hypothesis file, experiment module and its test in one commit), train record 9589fe2 12:24:23 (run started 12:23:42), catalogue 3746d0d 12:24:48, dev record b840055 12:26:16 (run started 12:26:09), all 2026-11-18 +0100. The experiment module has that one commit and no other. `git diff 68febdf b840055 -- src` is empty: no library code changed between registration and the dev run. Later edits to the hypothesis file are the status line and the body.
- Both records carry spec hash b3c513cc2e1c... and `registered_in` 68febdf; the train run's commit is 68febdf, the dev run's is 3746d0d, which differs from it by the train record, the catalogue and the status line only.
- Dev ran once: H1001-r02 is the only dev record and its `rerun_reason` is null.
- Dataset ids in both records (binance/spot/1d 2d6763395242, binance/universe 88f9a7cf72c7) match `uv run trading verify`, which reports every dataset ok.
- Dev arithmetic: half of 0.6611 is 0.3306, above the registered minimum of 0.2, so 0.3306 is required; 0.1244 is 0.206 short. Correct.

### The statistics

- **Standard error and minimum detectable effect.** The daily returns of strategy and benchmark have a correlation of 0.677 on train (0.7 was assumed). The formula for independent days then gives a standard error of 0.43; the block bootstrap of the record gives 0.381. With 0.381 the minimum detectable effect at 80% power is 0.95 (registered: 1.03). The estimate is 1.74 standard errors; the predicted 0.25 would have been 0.66 of one.
- **The p-value is 0.03 to 0.06, not 0.044 to three digits.** Same test, 30 other seeds: 0.031 to 0.047. With 20,000 draws: 0.039. With the block length set by hand instead of the automatic 9: 0.065 at 1, 0.040 at 5, 0.030 at 22, 0.013 at 60. A stationary bootstrap written for this review: 0.030. Every variant is below 0.10, so the candidate status never hung on the seed or the block; "below 0.05" does.
- **What a one-sided 0.044 from one registered hypothesis is worth.** Benjamini-Hochberg across one hypothesis is a single one-sided test at 10%: a true null becomes a candidate one time in ten. In two-sided terms the result is about 0.08. Simulated with the two recorded standard errors (my own run; it reproduces the Researcher's note): candidates have a mean train estimate of 0.67 if the truth is 0, 0.72 if it is 0.25, 0.80 if it is 0.5. The observed 0.66 therefore says "large enough to pass" and nothing about size.
- **Power of the dev rule.** With the dev standard error of 0.485, the chance that a dev estimate reaches the required 0.33 is 25% if the true difference is 0, 43% if it is the predicted 0.25, 75% if it is the train estimate. The rule separates a null from the predicted effect by 18 points. The dev estimate is 0.54 below the train estimate with a standard error of 0.62 for that gap (0.87 standard errors): the two runs do not contradict each other. `not replicated` records that the pre-declared rule was not met. It is not evidence that the effect is absent.

### The three points the Researcher flagged

**1. `dropped_weight` of 0.075 against "more than a few percent of one day's portfolio in total".** By the letter the criterion is tripped or undecidable: 7.5% is more than most readers' "a few percent". By what it was written to catch ("targets on coins that could not be bought" as the sign of a wrong test) it is not. I confirm the Researcher's account independently: the 0.075 is three slots of 1/40 out of 22,190 targets set in the window, ERDUSDT at the open of 2020-09-01, NPXSUSDT 2021-04-06 and BTTUSDT 2022-01-18, each the day after the pair's last bar, with the signal on at the final close; the loop of check 1 counts the same three. The registration itself describes this mechanism in "A NaN signal means flat". The drops change no return: the engine zeroes such a target, which is what a rule that knew would have done. Removing the three coins from both portfolios altogether gives +0.63. And the criterion could not have been met by a correct run: the registered benchmark, on the same schedule, drops 0.175 in the window (seven members stop trading), so any rule that decides daily on this universe drops up to that much. **My view: the train run is sound evidence, and the fault is in the criterion.** Two things remain true. A validity test without a number was judged by the Researcher after seeing a passing result, which is a judge in their own cause even when, as here, the facts leave little room. And by the registration's last sentence the remedy for a run that "is not evidence" would have been a new hypothesis, so the stricter reading cannot be dismissed as costless; it is simply wrong on the mechanism.

**2. Train data loaded once between the train run and the dev run.** It does not compromise the dev run. The dev test is fixed by the specification, and nothing in it moved: same spec hash in both records, an experiment module with one commit, no library change between registration and the dev record, a dev commit that differs only by the train record and the catalogue. Train data cannot tell anyone what dev holds. The look could affect one thing, the decision to proceed to dev instead of declaring the train run void, and there the Researcher's interest ran toward proceeding, which is the direction that exposed the result to its one dev look; the outcome was negative, so no positive was manufactured. What I cannot verify is the script itself, since it was not kept: I know nothing in the repository changed, not what was looked at.

**3. The benchmark re-equalised every day instead of the monthly reference.** How much: against the monthly equal-weight universe the train estimate is +0.525 (replayed with that benchmark: p 0.064; at double cost +0.325, p 0.158), so 0.136 of the 0.661, a fifth, comes from the choice. Of that gap 0.020 is cost (the daily benchmark pays 3.5% a year against 1.5%) and 0.116 is there before costs: re-equalising daily simply did worse on train (gross Sharpe 0.365 daily, 0.450 weekly, 0.481 monthly), mostly in 2020 and 2021. Against buy-and-hold BTC the difference is +0.450 (p 0.166). Was it legitimate: yes. It was registered before the run with a reason that holds (the strategy's own slots are re-equalised daily, so only this benchmark differs from it by the filter alone), the reference benchmarks are in the record, and the choice did not make the candidate: against the monthly benchmark the p-value would still have passed the 10% gate. But the title's "beats holding every universe member" reads as the passive portfolio, and against that the size to quote is +0.53 on train and +0.105 on dev (from the record), with the train figure no longer below 0.05.

### Infrastructure, seen while reviewing

- `dropped_weight` in a run record changed meaning in commit b74ae59, after both runs: it was summed from the first bar of the data and is now summed over the evaluation window, with `dropped_weight_before_window` beside it. `harness_version` stayed 1, so records do not say which meaning they carry. H1001-r01 is unaffected by luck (nothing was dropped before 2019-07); H1001-r02's 0.125 is the old, cumulative meaning.
- The automatic block length of the bootstrap is unstable: 9 for lookbacks 20, 21 and 25 and 22 for 19 and 22, on return series that are nearly the same, and the p-value moves by a third with it.
- The harness's look-ahead check removes later bars but not later rows of the universe table, so it could not detect a universe built with look-ahead; that rests on the Data steward's separate check.
- The record holds the strategy's dropped weight but not the benchmark's, and no return series: check 4 of the review skill says to "slice the returns in `metrics`", which do not exist there; I recomputed them.
