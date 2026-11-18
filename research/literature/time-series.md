# Time-series: literature notes

Collected by the Literature scout on 2026-11-18. Question of this run: what is the published evidence on time-series momentum (trend following) in cryptocurrency returns at daily to weekly horizons? The notes supply the motivation for one hypothesis ("time-series momentum on daily bars"), so they go deep on that one pattern and do not survey the family.

How to read an entry:

- Numbers are the paper's own, in its units, with the table or section they come from. Arithmetic of mine is marked "(my arithmetic)".
- "Opened" says which version I read. Where the published version was behind a paywall or a bot check I read the working paper and say so; the published numbers may differ.
- "Sample end" is checked against the split: a sample ending by 2022-12-31 is clean evidence for the train segment; anything later is flagged.
- Every source in the numbered sections ends by 2022-03-05, so none overlaps the dev or test segment. The flagged ones are all under "Unverified leads".

Sections are ordered by how strong the evidence is for a long-or-flat rule on daily bars.

## 1. Price above its moving average: long, otherwise cash (5 to 100 days)

**Claim.** A coin's return is higher on days after its price closed above its own moving average than on days after it closed below, so holding the coin only in the first state gives a better risk-adjusted return than buy-and-hold.

This is the pattern closest to what we can trade: it is long or flat by construction, uses daily data, and the main paper reports the cost that would erase it.

### 1a. Detzel, Liu, Strauss, Zhou and Zhu: the main positive result

- **Reference.** Detzel, A., Liu, H., Strauss, J., Zhou, G. and Zhu, Y. (2021). "Learning and predictability via technical analysis: Evidence from bitcoin and stocks with hard-to-value fundamentals." *Financial Management* 50(1), 107-137. DOI [10.1111/fima.12310](https://doi.org/10.1111/fima.12310).
- **Opened.** The working paper dated 2018-04-11, titled "Bitcoin: Learning, Predictability, and Profitability via Technical Analysis", from an unofficial copy at <https://community.portfolio123.com/uploads/short-url/jS0qs8gndLATbD3WlYQ79thDnzD.pdf>. Of the published version I could read only the abstract (the publisher's reader stopped behind a bot check), and it states the same finding in words: ratios of price to moving average forecast daily Bitcoin returns in and out of sample, and strategies built on them beat buy-and-hold on alpha and Sharpe ratio. All numbers below are from the working paper.
- **Sample.** Bitcoin, daily, 7 days a week, CoinDesk price (Mt. Gox before July 2013, an average of large exchanges after), 2010-10-27 to 2018-01-31, 2,654 daily returns (Section III, Table 6). Ripple from CoinMarketCap, 2013-11-12 to 2018-01-31, as a robustness check (Table 9).
- **Rule.** Hold Bitcoin on day t if the price at t-1 is above its L-day moving average at t-1, otherwise hold Treasury bills; L = 5, 10, 20, 50, 100 (Eq. 9 and 10). Never short. The signal is known at the close of t-1 and earns the close-to-close return of day t.
- **Size (Table 6 Panel A and Table 8 Panel A, full sample, annualised).** Sharpe ratio of buy-and-hold Bitcoin 1.92; of the rule 2.51 (MA5), 2.45 (MA10), 2.29 (MA20), 2.13 (MA50), 2.09 (MA100). Alpha against buy-and-hold 0.24, 0.23, 0.19, 0.14 and 0.11 percent per day, in the same order. Maximum drawdown 89.5 percent for Bitcoin against 64.3 to 70.3 percent for the rules. Mean excess return is slightly lower than buy-and-hold for every window (for example 209.78 against 213.58 percent a year for MA5): the gain is in risk, not in return.
- **Second half only (2014-06-26 to 2018-01-31, Table 6 Panel C and Table 8 Panel B).** Buy-and-hold Sharpe 1.45; rules 2.09, 2.02, 1.90, 1.80, 1.45. MA100 no longer adds anything (alpha 0.04 percent per day, standard error 0.05).
- **Ripple (Table 9).** Buy-and-hold Sharpe 1.33; rules 1.83 (MA5), 1.88 (MA10), 1.64 (MA20), 1.49 (MA50), 1.30 (MA100). Alpha is significant for MA5, MA10 and MA20 only.
- **Costs.** Not deducted, but Table 8 Panel A gives the average daily turnover and the one-way cost that would bring the alpha to zero: turnover 21.75, 12.93, 7.95, 5.01 and 2.68 percent per day; break-even one-way cost 1.12, 1.76, 2.36, 2.74 and 3.96 percent, for MA5 to MA100. Shorter windows earn more before costs and trade much more.
- **Sample end.** 2018-01-31. Clean for the train segment.
- **Transfer.** Testable here as a trading claim on daily bars, almost as published: long when the close is above the L-day mean of closes, flat otherwise, against buy-and-hold of the same coin or the equal-weight point-in-time universe. Two differences to keep in mind. The paper is one coin (plus Ripple), not a 40-coin universe. And its fill is at the signal bar's close while ours is at the next open; for a market that trades around the clock these are the same instant, so nothing is lost. Our 12 to 25 bps per side is about a tenth of the break-even cost reported for MA20 (236 bps), so costs alone should not remove an effect of the published size; double cost should not either.

### 1b. Hudson and Urquhart: many rules, break-even costs, and a failure out of sample

- **Reference.** Hudson, R. and Urquhart, A. (2021). "Technical trading and cryptocurrencies." *Annals of Operations Research* 297, 191-220 (online 2019-08-30). Open access: <https://link.springer.com/article/10.1007/s10479-019-03357-1>.
- **Opened.** The published article and its Tables 2, 6, 7 and 9.
- **Sample.** Daily. Bitcoin from CoinDesk (from 2010-07-18) and from Bitstamp (from 2012-12-01); Litecoin (from 2013-04-28), Ripple (from 2013-08-04) and Ethereum (from 2015-08-07) from CoinMarketCap. All end 2017-12-31 (Section 2). A separate out-of-sample check covers the first six months of 2018 (Section 6.5).
- **Method.** 14,919 rules in five classes, of which 7,980 are moving-average rules with windows of 2, 5, 10, 15, 20, 25, 50, 100 and 200 days, optional percentage bands, 1 to 5 days of confirmation and, in some variants, a fixed 3- or 5-day holding period (Appendix). Positions are long, short or neutral (cash). Bootstrapped p-values with Bonferroni, Holm, Benjamini-Hochberg and Benjamini-Yekutieli corrections.
- **Direction and size.** The average moving-average rule earns a significant positive return on every series: "annualised return" 7.72 percent (CoinDesk), 5.82 (Bitstamp), 6.74 (Litecoin), 8.89 (Ripple), 11.32 (Ethereum) (Table 2). I could not reconcile the scale of this column with the table of buy-and-hold figures (Table 7 gives buy-and-hold "annualised return" 0.1167 for CoinDesk Bitcoin), so read these as relative magnitudes. The profit comes from the long side: the average daily return after a buy signal is 0.33 to 0.65 percent for moving-average rules, after a sell signal -0.06 to 0.00 percent (Table 2); by the paper's count, in 15 of 20 rule-class and coin combinations no rule has a significant return on sell signals (Section 6.1, Table 4).
- **Against buy-and-hold (Table 7).** Only 6.12 percent of all rules beat buy-and-hold on return for CoinDesk Bitcoin, 4.96 percent for Bitstamp, 11.49 for Litecoin, 15.69 for Ripple and 9.01 for Ethereum. On the Sortino and Calmar ratios 28 to 58 percent do. Again the gain is in drawdowns.
- **Costs (Table 6).** Returns are before costs. Average break-even cost of moving-average rules: 54.86 bps (CoinDesk), 50.40 (Bitstamp), 35.44 (Litecoin), 36.01 (Ripple), 78.60 (Ethereum); 22.79 to 38.72 percent of moving-average rules have a break-even above 50 bps. The article does not say, in the parts I read, whether a break-even is per side or per round trip.
- **Multiple testing (Table 8, Section 7).** 20.35 to 50.41 percent of rules stay significant after the corrections.
- **Out of sample (Table 9).** The best in-sample rule per series, run on January to June 2018: negative for both Bitcoin series (annualised return -0.0010 and -0.0091, Sharpe -0.05 and -0.06), positive for Litecoin (0.0775, Sharpe 1.36), Ripple (0.0546, Sharpe 0.74) and Ethereum (0.0631, Sharpe 1.19). The authors read this as Bitcoin having become more efficient. It is six months and one rule per coin, so it is weak evidence either way.
- **Sample end.** 2017-12-31 (2018-06-30 for the out-of-sample check). Clean.
- **Transfer.** Testable only in part: the rule set includes shorting, but the paper itself finds the profit on the long side, so the long-or-flat half is the part worth testing. It does not report results by window length, so it does not help choose a lookback.

### 1c. Wei, Kyriakou, Sermpinis and Stasinakis: most rules do not survive, a one-week ratio does

- **Reference.** Wei, M., Kyriakou, I., Sermpinis, G. and Stasinakis, C. (2024). "Cryptocurrencies and Lucky Factors: The value of technical and fundamental analysis." *International Journal of Finance & Economics* 29(4), 4073-4104. DOI [10.1002/ijfe.2863](https://doi.org/10.1002/ijfe.2863). Open access copy: <https://eprints.gla.ac.uk/302711/1/302711.pdf>.
- **Opened.** The published article (abstract, Sections 1 to 3, the text of Section 4, conclusion). The online appendix with per-coin tables for eight of the twelve coins was not opened.
- **Sample.** Daily prices from Bitstamp and Binance. Main results for Bitcoin, Ethereum, Ripple and Dash, 2015-08-08 to 2022-03-05; eight more coins (Cardano, Avalanche, Binance Coin, Dogecoin, Polkadot, Litecoin, Terra, Solana) in the appendix. Three splits: 50, 75 and 90 percent in sample, the rest out of sample (Section 3).
- **Method.** 7,846 classic rules (moving average, support and resistance, channel breakout, on-balance volume, filter) plus five ratios of log price to its moving average over 1, 2, 4, 10 and 20 weeks, the indicator from Detzel et al. Performance is computed after "average transaction costs from Binance" (Section 3; the figure sits in a footnote that my text extraction lost). The best 15 rules per coin go through predictive regressions, then the Lucky Factors procedure of Harvey and Liu and Hansen's Superior Predictive Ability test, then the out-of-sample periods.
- **Finding.** Many rules look good in sample, but only the one-week price-to-moving-average ratio (the shortest of the five) shows both predictive power and profit in and out of sample, across all three splits and all twelve coins; classic moving-average rules do not. Profits of the rules that looked good in the first split fall sharply in the later ones (Section 4.2 and conclusion). The authors' own summary is that the benefit of technical rules in crypto erodes quickly.
- **Sample end.** 2022-03-05. Clean, and it is the only source here that covers 2018 to 2022.
- **Transfer.** Testable here: its result is a predictive claim (a short price-to-moving-average ratio forecasts the next day's return) on large coins that are in a top-40 point-in-time universe. It argues for a window near one week and against expecting much from 50 days and longer in recent years.

### 1d. Rozario, Holt, West and Ng: a weak practitioner-style check

- **Reference.** Rozario, E., Holt, S., West, J. and Ng, S. (2020). "A Decade of Evidence of Trend Following Investing in Cryptocurrencies." arXiv:2009.12155. <https://arxiv.org/abs/2009.12155>. Not peer reviewed; the authors are affiliated with a crypto derivatives exchange.
- **Opened.** The full arXiv paper (8 pages).
- **Sample.** Bitcoin against the dollar on Bitstamp, resampled to hourly, 2011-09-13 to 2019-12-12.
- **Method and result.** Moving-average crossovers with windows of 1 to 1,000 hours, parameters refitted each year for the best Sharpe ratio and applied to the next year; costs, spread and slippage assumed to be zero (Section 2). They report a 255 percent annualised return for the walk-forward simple-moving-average strategy and say that crossovers of roughly 10 and 40 days do consistently well, with a slight drop in recent years, and that they find no profitable intraday trend strategy (Section 4). In the same paper they also say the parameters fitted on one year do not give predictable Sharpe ratios in the next (Section 3.1).
- **Sample end.** 2019-12-12. Clean.
- **Transfer.** Use only as a lead. No costs, one coin, heavy parameter search, and the paper contradicts itself on stability. It agrees with the others that the useful windows are days to weeks, not hours.

## 2. Short-horizon time-series momentum: the past week predicts the next one to four weeks

**Claim.** A coin's own recent return predicts its next returns with a positive sign at daily and weekly horizons.

### 2a. Liu and Tsyvinski: the original crypto evidence

- **Reference.** Liu, Y. and Tsyvinski, A. (2021). "Risks and Returns of Cryptocurrency." *Review of Financial Studies* 34(6), 2689-2727 ([listing](https://econpapers.repec.org/RePEc:oup:rfinst:v:34:y:2021:i:6:p:2689-2727)).
- **Opened.** NBER Working Paper 24877, August 2018: <https://www.nber.org/papers/w24877>. The published version is behind a paywall and I did not open it; its abstract repeats the claim of a strong time-series momentum effect. All numbers below are from the working paper and may differ from the published tables.
- **Sample.** Bitcoin 2011-01-01 to 2018-05-31, Ripple 2013-08-04 to 2018-05-31, Ethereum 2015-08-07 to 2018-05-31; CoinDesk prices; daily and weekly returns (Section 2).
- **Method.** Regressions of the return h periods ahead on the current return; then weeks sorted into quintiles by that week's return, with the following weeks' returns compared (Section 4.1).
- **Daily, Bitcoin (Table 14 Panel A).** Coefficient of the next day's return on today's: 0.06 (t = 2.96); also significant at 5 days (0.07, t = 3.51) and 6 days (0.08, t = 4.14) ahead. The paper's translation: a one-standard-deviation higher return today (5.55 percent) goes with a 0.33 percent higher return tomorrow. R-squared is 0.00 to 0.01. The bootstrapped t-statistics in the same table are much lower (1.22 for the next day; 2.00 and 2.97 for days 5 and 6).
- **Weekly, Bitcoin (Table 14 Panel B).** Coefficient of the return 1, 2, 3 and 4 weeks ahead on this week's return: 0.19 (t = 3.73, bootstrapped 2.17), 0.22 (4.52; 2.73), 0.21 (4.26; 2.47), 0.09 (1.72; 1.40). R-squared 0.03, 0.05, 0.05, 0.01. A one-standard-deviation higher weekly return (16.64 percent) goes with 3.16, 3.66, 3.49 and 1.50 percent higher returns in weeks 1 to 4. Weeks run Sunday to Sunday at 23:59:59 UTC.
- **Quintiles, Bitcoin weekly (Table 15).** After a week in the top quintile (average formation return 27.44 percent) the next week averages 11.22 percent (t = 3.95, weekly Sharpe 0.45); after a bottom-quintile week (formation -14.95 percent) it averages 2.60 percent (t = 1.69, Sharpe 0.19). The three middle quintiles average 0.27, 1.15 and 3.75 percent: the relation is not monotonic and the effect sits in the top quintile, that is, after very strong weeks. From 2013 on (Table 16) the top quintile's next week is 7.18 percent (t = 2.57) against 2.83 for the bottom. With quintile cut-offs fixed on the first two years only (Table 17): 7.88 percent (t = 2.70) against 3.35.
- **Other coins (Table 18, daily only).** Ripple: positive coefficients at 1 to 5 days (0.06, 0.08, 0.05, 0.04, 0.06), conventional t between 1.83 and 3.59 but bootstrapped t mostly below 2. Ethereum: 0.08 at one day (t = 2.58, bootstrapped 1.67) and a negative coefficient at five days (-0.08, t = -2.63). The authors call the effect weaker for Ethereum.
- **Costs.** Not considered.
- **Sample end.** 2018-05-31. Clean.
- **Transfer.** Testable here as a predictive claim on daily bars: past 7-day return against the return of the following 7 days (or 1 to 4 weeks), coin by coin or pooled over the point-in-time universe. As a trading claim it transfers only in part. The evidence is three coins in a period when every quintile had a positive mean, so "flat after a weak week" gave up return in that sample; what the quintile tables support is "the weeks after a very strong week are much better than average", not "the sign of last week's return tells you whether to hold". A one-day signal is marginal after our costs: 0.33 percent expected for a one-standard-deviation day against 24 to 50 bps for a round trip (my arithmetic).

### 2b. Liu, Tsyvinski and Wu: which horizons carry momentum (cross-sectional evidence)

This paper belongs to the cross-sectional family. It is filed here because it is the cleanest published evidence on the horizon at which crypto momentum lives, and the brief asked for it.

- **Reference.** Liu, Y., Tsyvinski, A. and Wu, X. (2022). "Common Risk Factors in Cryptocurrency." *Journal of Finance* 77(2), 1133-1177. DOI [10.1111/jofi.13119](https://doi.org/10.1111/jofi.13119).
- **Opened.** NBER Working Paper 25882, May 2019: <https://www.nber.org/papers/w25882>. The published version (which I did not open) may use a longer sample and differ in its numbers.
- **Sample.** 1,707 coins with market capitalisation above 1 million dollars, CoinMarketCap volume-weighted prices, start of 2014 to end of 2018, weekly returns built from daily closes; 109 coins qualify in 2014 and 1,583 in 2018; defunct coins included (Section 2).
- **Method.** Each week coins are sorted into value-weighted quintiles on their past 1-, 2-, 3-, 4-, 8-, 16-, 50- and 100-week return; portfolios are rebalanced weekly (Section 3.2).
- **Size (Table 4).** Top minus bottom quintile, excess return per week: 2.7 percent for the 1-week lookback (t = 1.994), 3.3 for 2 weeks (t = 2.442), 4.1 for 3 weeks (t = 2.742), 2.5 for 4 weeks (t = 2.002). For the 3-week sort the top quintile earns 4.3 percent a week (t = 2.956) and the bottom 0.2 percent (t = 0.156): the spread comes from the winners, not from losers falling.
- **Horizons that fail (Section 3.2 and Table 7).** Lookbacks of 8, 16, 50 and 100 weeks give no significant spread; the 16-week spread is 0.4 percent a week and insignificant.
- **Other caveats in the paper.** In Fama-MacBeth regressions, which weight coins equally, momentum is not significant (Section 5.2, Table 13 Panel D). Momentum is a large-coin effect: within coins above the median size the 3-week spread is 4.2 percent a week (t = 2.57), below the median 0.6 percent (t = 0.30) (Table A.2). When Bitcoin is shorted instead of the bottom quintile, the 1-, 2- and 4-week strategies lose significance (Section 5.1, Table 12).
- **Costs.** Not considered; the paper says so for its strategies (Section 3.1).
- **Sample end.** 2018-12-31. Clean.
- **Transfer.** Not a time-series test, so it does not directly support a rule that looks at each coin alone. What transfers is the horizon: momentum in crypto was found at 1 to 4 weeks and not at 8 weeks or more, it was strongest in large coins (which is what a top-40 universe holds), and its profit was in the long leg, so the no-shorting constraint costs little.

## 3. The parent result in other asset classes

- **Reference.** Moskowitz, T. J., Ooi, Y. H. and Pedersen, L. H. (2012). "Time series momentum." *Journal of Financial Economics* 104(2), 228-250. DOI [10.1016/j.jfineco.2011.11.003](https://doi.org/10.1016/j.jfineco.2011.11.003).
- **Opened.** The published article, from a course copy at <https://fairmodel.econ.yale.edu/ec439/jpde.pdf>.
- **Sample.** 58 liquid futures and forwards: 24 commodities, 12 currency pairs, 9 equity indexes, 13 government bonds; January 1965 to December 2009, with strategies evaluated from January 1985; monthly (Section 2.1, Section 3).
- **Claim and size.** An instrument's own excess return over the past 1 to 12 months predicts its next month's return with a positive sign, and the relation partly reverses at longer horizons (abstract; Fig. 1). The benchmark strategy takes the sign of the past 12-month return, holds for 1 month, long or short, with each position scaled to 40 percent annualised volatility (Section 4.1, Eq. 5). Its alpha is about 1.58 percent a month against standard factors (Table 3); the alpha's t-statistic is 6.61 for the 12-month lookback and 1-month holding, the highest in Table 2 Panel A, and 4.34 for a 1-month lookback and 1-month holding. The diversified strategy has an annual Sharpe ratio above 1 (introduction). All 58 instruments have a positive 12-month strategy return, 52 of them significant at 5 percent (Section 4.1).
- **Against always long.** Regressing each instrument's strategy on a strategy that is always long gives a positive alpha in 90 percent of cases, 26 percent of them significant (Section 4.1). This is the closest the paper comes to a long-or-flat comparison.
- **Costs.** Results are gross (Fig. 2 is labelled gross Sharpe ratio); costs are not deducted.
- **Sample end.** December 2009. No crypto.
- **Transfer.** Not testable here as published: it needs shorting, volatility scaling to a fixed target with leverage, and monthly horizons across asset classes. It gives the name, the design (lookback and holding period chosen separately, sign of past return as the signal) and a prior that trend effects are general. Its 12-month lookback has no support in the crypto papers above, where the effect is found at 1 to 4 weeks and has faded by 8 weeks.

## Failures, decay and dependence on costs

Collected in one place, because they set the prior for the hypothesis:

- **Bootstrapped significance is much weaker than conventional.** In Liu and Tsyvinski's daily regressions the next-day coefficient has t = 2.96 conventionally and 1.22 bootstrapped (Table 14); the weekly coefficients survive (2.17 to 2.73).
- **Not every coin.** Ethereum shows a negative coefficient at five days in Liu and Tsyvinski (Table 18). Ripple's MA50 and MA100 rules add nothing in Detzel et al. (Table 9).
- **Longer windows decay first.** In the second half of Detzel et al.'s sample MA100 has no alpha (Table 8 Panel B). Liu, Tsyvinski and Wu find nothing at 8 weeks and beyond. Wei et al. find only the one-week ratio survives through March 2022.
- **Out of sample.** Hudson and Urquhart's best in-sample rules lose money on Bitcoin in the first half of 2018 (Table 9).
- **Data snooping.** Wei et al. conclude that the classic rule families have no genuine value once selection is accounted for, with one exception.
- **Return against risk.** Where a comparison with buy-and-hold is reported, trend rules earn about the same or less raw return and improve the Sharpe ratio and drawdown (Detzel et al. Table 6; Hudson and Urquhart Table 7). A hypothesis that predicts a higher raw return than buy-and-hold is not what the literature found.
- **Costs.** Of the sources opened, only Wei et al. deduct costs. The two papers that report break-evens put them well above our 12 to 25 bps: 112 to 396 bps one way for Bitcoin moving-average rules to January 2018 (Detzel et al. Table 8), and 35 to 79 bps on average for moving-average rules on five series to 2017 (Hudson and Urquhart Table 6). Both come from the early, strongest years; a smaller effect in later years would have a lower break-even.
- **A published null** on momentum in crypto (Grobys and Sapkota 2019) is listed under unverified leads because I could read only its abstract.

## What transfers to our setup

Setup: spot only, long or flat, the point-in-time universe (40 USDT pairs on Binance, monthly reconstitution), daily bars, signal at a bar's close and trade at the next open, 12 to 25 bps per side.

- **Long or flat is not a handicap for this pattern.** The best-supported rule (Section 1a) is long or cash by design. Where long and short sides are reported separately, the profit is on the long side (Hudson and Urquhart Table 2; Liu, Tsyvinski and Wu Table 4).
- **Signal at the close, trade at the next open** matches the papers' close-to-close convention, because the next daily bar opens at the instant the signal bar closes.
- **The universe is wider than the evidence.** Almost all time-series evidence is on Bitcoin, plus Ripple, Ethereum, Litecoin and (in Wei et al.) nine more large coins. None of the papers tests a per-coin trend rule across some 40 coins with changing membership. Liu, Tsyvinski and Wu's finding that momentum is stronger in larger coins is the only support for expecting it across a top-40 universe, and it is cross-sectional.
- **Most samples end in 2017 or 2018.** Only Wei et al. reach 2022. Much of the train segment is therefore post-sample for the positive results, and the one source that covers it reports decay. A train estimate well below the published sizes would be consistent with the literature.
- **The benchmark matters.** The published gain is risk-adjusted and against buy-and-hold of the same coin. Against buy-and-hold BTC or the equal-weight point-in-time universe, expect the claim to hold, if at all, in Sharpe ratio or drawdown rather than in mean return.
- **Costs.** At the published turnover of a 20-day rule, 7.95 percent of the position per day (Detzel et al. Table 8), 12 to 25 bps per side costs about 1 to 2 bps per day, or roughly 3.5 to 7 percent a year (my arithmetic), against a published alpha of 0.19 percent per day. Costs are not the binding constraint at the published effect size; a 5-day rule trades nearly three times as much.

### Lookback for a simple long-or-flat trend rule

What the sources say, in days:

| Lookback | Evidence | Source |
| --- | --- | --- |
| 1 day | Weak: coefficient 0.06, not significant when bootstrapped; marginal after our costs | Liu and Tsyvinski, Table 14 Panel A |
| 5 to 7 days | Past week predicts weeks 1 to 3 ahead (Bitcoin); MA5 has the highest gross Sharpe (2.51) but 21.75 percent daily turnover; the one-week price-to-average ratio is the only rule to survive to 2022 | Liu and Tsyvinski, Table 14 Panel B; Detzel et al., Tables 6 and 8; Wei et al., Section 4 and conclusion |
| 10 days | MA10 Sharpe 2.45 against 1.92; turnover 12.93 percent a day | Detzel et al., Tables 6 and 8 |
| 14 to 28 days | Cross-sectional momentum significant at 1, 2, 3 and 4 weeks, largest at 3 weeks (4.1 percent a week); MA20 Sharpe 2.29, turnover 7.95 percent a day, break-even cost 2.36 percent | Liu, Tsyvinski and Wu, Table 4; Detzel et al., Tables 6 and 8 |
| 50 to 100 days | Smaller gain (Sharpe 2.13 and 2.09); MA100 has no alpha after mid-2014; not robust in Wei et al. | Detzel et al., Table 8 Panels A and B; Wei et al. |
| 8 weeks and more | No momentum spread (cross-sectional) | Liu, Tsyvinski and Wu, Section 3.2 and Table 7 |
| 12 months | The standard in futures; no crypto evidence in any source opened | Moskowitz, Ooi and Pedersen, Table 2 |

Plainly: the literature narrows the lookback to roughly one to four weeks (7 to 28 days) and does not pin it down further. Shorter windows have the larger gross effect and the most recent support, longer ones in that range trade less. A window of about 20 days sits in the middle of the supported range and has three partial supports: MA20 in Detzel et al., the 3-week peak in Liu, Tsyvinski and Wu (cross-sectional), and the 20-day rule in Grobys, Ahmed and Sapkota (abstract only, see leads). Whichever value is registered should be stated as a choice from this range made before looking at data, not as a number the literature fixes. No source supports a lookback of several months for crypto.

### Rebalancing frequency

- Detzel et al. and Hudson and Urquhart evaluate the signal every day and switch whenever it flips. For a 20-day window that is a turnover of 7.95 percent a day, about one switch every 12 to 13 days on average (my arithmetic from Detzel et al. Table 8).
- Liu and Tsyvinski, and Liu, Tsyvinski and Wu, work on weekly returns and rebalance weekly.
- Moskowitz, Ooi and Pedersen rebalance monthly.
- Hudson and Urquhart include variants with a fixed 3- or 5-day holding period but do not report results by holding period in the article.

Plainly: no source compares rebalancing frequencies for the same signal, so the literature does not pin this down. Daily evaluation is the published convention for moving-average rules and weekly for return-sign momentum; both are legitimate choices to register. The cost evidence says daily evaluation of a 20-day rule is affordable at 12 to 25 bps per side.

## Unverified leads

Sources I could not open in full. Nothing here should be cited as evidence until someone reads the paper; where I read an abstract, that is all that is reported.

- **Grobys, K., Ahmed, S. and Sapkota, N. (2020). "Technical trading rules in the cryptocurrency market." *Finance Research Letters* 32, 101396. DOI 10.1016/j.frl.2019.101396.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/finlet/v32y2020ics1544612319308852.html)): simple moving-average rules on daily prices of the eleven most traded coins, 2016 to 2018; a variable moving-average rule works with a 20-day window; excluding Bitcoin it earns 8.76 percent a year in excess of the average market return. Not opened: the university repository refused the connection and the publisher showed a bot check. Sample end 2018, clean. Worth reading first, since it is the only multi-coin moving-average study and names a window.
- **Grobys, K. and Sapkota, N. (2019). "Cryptocurrencies and momentum." *Economics Letters* 180, 6-10. DOI 10.1016/j.econlet.2019.03.028.** Abstract only ([RePEc listing](https://econpapers.repec.org/RePEc:eee:ecolet:v:180:y:2019:i:c:p:6-10)): 143 coins, 2014 to 2018, no significant momentum payoffs. A search snippet says the paper also finds no strong evidence for time-series momentum in the sense of Moskowitz et al.; I could not confirm that in the paper. Same access problem. If confirmed it is the main published null for this hypothesis. Sample end 2018, clean.
- **Tzouvanas, P., Kizys, R. and Tsend-Ayush, B. (2020). "Momentum trading in cryptocurrencies: Short-term returns and diversification benefits." *Economics Letters* 191, 108728. DOI 10.1016/j.econlet.2019.108728.** Abstract only ([university listing](https://researchportal.port.ac.uk/en/publications/momentum-trading-in-cryptocurrencies-short-term-returns-and-diver/)): formation and holding period momentum on daily data for twelve coins over about three years; a strong effect for short-horizon portfolios that disappears at longer horizons. The full-text links returned an access error. Sample end before 2020, clean.
- **Han, C., Kang, B. and Ryu, J. "Time-Series and Cross-Sectional Momentum in the Cryptocurrency Market: A Comprehensive Analysis under Realistic Assumptions." Working paper.** Not opened (the host returned an access error). From search snippets only: lookback and holding periods of 1 to 56 days, costs and liquidation risk modelled, strong time-series and weak cross-sectional momentum, profits concentrated in rising markets. **Hindsight flag: the snippets give a sample of December 2013 to August 2023, which overlaps the dev segment.** Its claim may be noted; its results must not be used as a reason to expect something.
- **Deprez, N. and Frömmel, M. (2024). "Are simple technical trading rules profitable in bitcoin markets?" *International Review of Economics & Finance* 93(B), 858-874. DOI 10.1016/j.iref.2024.05.003.** Abstract only ([RePEc listing](https://econpapers.repec.org/RePEc:eee:reveco:v:93:y:2024:i:pb:p:858-874)): 75,360 rules from six classes at daily and intraday frequency, selected after costs with a multiple-testing procedure, then tested out of sample as portfolios; they report that the rules beat buy-and-hold out of sample, mainly on risk-adjusted terms. **Hindsight flag: the abstract gives no sample dates and the paper is from 2024, so treat it as overlapping the dev segment until checked.**
- **Published versions of the two Liu and Tsyvinski papers** (*Review of Financial Studies* 2021 and *Journal of Finance* 2022). Paywalled. From memory, not confirmed: the published *Review of Financial Studies* version runs the time-series momentum tests on a value-weighted market index of coins rather than on Bitcoin alone, and the *Journal of Finance* version extends the sample beyond 2018. Both would still end before 2023. The numbers in Sections 2a and 2b are from the working papers.
- **Detzel et al. (2021), published version.** Only the abstract was readable. The working paper's tables (Section 1a) may have changed in publication, and the published version adds evidence from stocks.
- **Svogun, D. and Bazán-Palomino, W. (2022). "Technical analysis in cryptocurrency markets: Do transaction costs and bubbles matter?" *Journal of International Financial Markets, Institutions and Money* 79.** Seen only in a search summary: 69 moving-average and breakout rules, with transaction costs lowering the chance of profit for Ripple and Litecoin and raising it for Bitcoin and Ethereum. Not opened.

## Where I found nothing

- No source I could open tests a per-coin trend rule on a broad, liquidity-ranked universe with changing membership (our point-in-time universe).
- No source compares rebalancing frequencies for a fixed signal.
- No source tests a 12-month time-series lookback on crypto.
