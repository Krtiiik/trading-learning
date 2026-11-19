# Time-series: literature notes

Collected by the Literature scout on 2026-11-18. Question of this run: what is the published evidence on time-series momentum (trend following) in cryptocurrency returns at daily to weekly horizons? The notes supply the motivation for one hypothesis ("time-series momentum on daily bars"), so they go deep on that one pattern and do not survey the family.

How to read an entry:

- Numbers are the paper's own, in its units, with the table or section they come from. Arithmetic of mine is marked "(my arithmetic)".
- "Opened" says which version I read. Where the published version was behind a paywall or a bot check I read the working paper and say so; the published numbers may differ.
- "Sample end" is checked against the split: a sample ending by 2022-12-31 is clean evidence for the train segment; anything later is flagged.
- Every source in sections 1 to 3 ends by 2022-03-05, so none overlaps the dev or test segment. The flagged ones are all under "Unverified leads".

Sections 1 to 3 are ordered by how strong the evidence is for a long-or-flat rule on daily bars.

A second run on 2026-11-19 added sections 4 to 7 on the family's other sub-angles (reversal, volatility, calendar effects, intraday momentum and volume), with their own leads and gaps at the end of the file. Read "How the second run differs" at the top of section 4 before using them: far fewer of its sources could be opened in full.

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

---

# Second run (2026-11-19): reversal, volatility, calendar effects, intraday momentum and volume

Question of this run: what is published on the time-series family's sub-angles other than trend, so that about seven more hypotheses can be registered across them and across daily and hourly bars?

**How the second run differs.** Most journal articles on these sub-angles are behind publisher paywalls or bot checks, and every PDF link I tried answered with a binary file instead of readable text, which I did not retry. What I could read in full are seven open sources, six of them arXiv papers and one a practitioner research article. They carry sections 4 to 7. Everything of which I read only an abstract is under "Unverified leads (second run)", grouped by sub-angle, with what the abstract states. Three consequences:

- The numbered entries lean on arXiv preprints, several not peer reviewed. The better-known journal results (intraday momentum, overreaction, volume causality) are leads, not entries.
- Numbers in sections 4 to 7 were read through a text extraction of the HTML version of each paper, not from the typeset tables. Where the extraction itself looked inconsistent I say so. Check a number against the paper's table before quoting it in a hypothesis file.
- Almost all intraday evidence is Bitcoin, sometimes Ethereum. Nothing below is a test on some 40 coins.

Sample end dates: every source in sections 4 to 7 ends by 2022-10 and is clean for the train segment. Flagged sources are all in the leads.

## 4. Short-horizon reversal in a coin's own returns

### 4a. Hourly and sub-hourly Bitcoin returns are negatively autocorrelated

**Claim.** A Bitcoin return over the last 10 minutes to one hour is followed, on average, by a return of the opposite sign over the next such period.

- **Reference (hourly).** Tartakovsky, E., Plesovskikh, K., Sarmakeeva, A. and Bibik, A. (2020). "Autocorrelation of returns in major cryptocurrency markets." arXiv:2003.13517. <https://arxiv.org/abs/2003.13517>. Not peer reviewed; the first author is at a trading firm.
- **Opened.** The full paper in its HTML rendering.
- **Sample.** Bitfinex BTC/USD 2014-07-01 to 2019-07-01; Bitfinex ETH/USD and ETH/BTC 2016-03-09 to 2019-07-01; Bitmex XBT/USD perpetual swap 2017-10-12 to 2019-07-01. Bars of 5 minutes, 1 hour, 1 day and 1 week (Section 5).
- **Method.** Pearson autocorrelation at several lags, Ljung-Box test up to 30 lags, and the lag-1 autocorrelation in a rolling one-year window (Sections 4 and 5).
- **Direction and size.** At 5 minutes and 1 hour, autocorrelation is significant on all four markets (Ljung-Box p-values of zero at every lag, Section 5.2). For BTC/USD and the Bitcoin swap the low-order autocorrelations are negative (Section 5.1). For ETH/USD and ETH/BTC the first-order coefficient is positive and the second-order negative (Section 5.1). The rolling lag-1 coefficient on hourly bars is described as negative on every market over time (Section 5.3), which does not agree with the positive first-order result for the Ethereum pairs two sections earlier. All four markets show a significant positive autocorrelation at lag 16 on hourly bars (Section 5.1), which the paper does not explain. Coefficient sizes are shown only in charts; the text gives no numbers.
- **Costs.** None. The authors say the findings alone are not enough to extract profit.
- **Sample end.** 2019-07-01. Clean.

Second source, shorter horizon:

- **Reference.** Tang, Y., Arias-Calluari, K., Harré, M. S. and Alonso-Marroquin, F. (2024). "Stylized Facts of High-Frequency Bitcoin Time Series." arXiv:2402.11930. <https://arxiv.org/abs/2402.11930>.
- **Opened.** The full paper in its HTML rendering.
- **Sample.** BTC/USD from Reuters Datascope, 10-minute returns, analysed in two periods: 2019-04-02 to 2020-12-31 and 2021-01-01 to 2022-05-09 (Section V; the abstract and introduction give looser ranges).
- **Direction and size.** The autocorrelation of 10-minute returns is negative at short lags in both periods, then oscillates around zero from about 30 to 200 minutes, and beyond that is about 0.002 in absolute value (Section V.2). No lag-by-lag table.
- **Costs.** None.
- **Sample end.** 2022-05-09. Clean.

- **Corroboration at abstract level only** (see leads): De Nicola 2021 reports negative first-order autocorrelation at one, two and four hours on Bitcoin, stronger after larger moves.
- **Transfer.** Testable here as a predictive claim on hourly bars: the return of bar t against the return of bar t+1, per coin or pooled over the point-in-time universe, predicted sign negative. Two warnings for registration. The evidence is Bitcoin; the one paper that looks at Ethereum finds the opposite sign at lag 1, so a pooled test over 40 coins is an extension the literature does not cover. And no source reports a size, so the predicted size has to be declared without a published number. As a trading claim (long for one hour after a down hour, otherwise flat) it is testable but starts with a handicap: a round trip costs 24 to 50 bps (my arithmetic from 12 to 25 bps per side), against an average hourly move that is itself a fraction of a percent, and no source claims a profit after costs.

### 4b. Daily returns: no stable autocorrelation of either sign

**Claim (a null).** A coin's daily return does not reliably predict its next daily return, in either direction.

- **Source.** Tartakovsky et al. (2020), as in 4a.
- **Result.** On daily bars no autocorrelation of any order clearly exceeds its confidence band (Section 5.1); the Ljung-Box results differ by market (never significant for the Bitcoin swap, unstable for BTC/USD, mostly significant for ETH/BTC; Section 5.2); the rolling lag-1 coefficient behaves differently on every market (Section 5.3). On weekly bars the rolling lag-1 coefficient is positive most of the time on all markets, which agrees with section 2.
- **Fits with what is already on file.** Liu and Tsyvinski's daily coefficient for Bitcoin is positive (0.06) and loses significance under bootstrap (section 2a).
- **Sample end.** 2019-07-01. Clean.
- **Transfer.** Testable here as published: a pooled daily regression of the next day's return on today's. The literature's prior is "nothing or weakly positive in large coins", not reversal. Abstract-level leads point the same way for our universe: daily reversal is reported as an effect of small, illiquid coins, with the largest coins showing daily momentum instead (Zaremba et al. 2021; Bianchi, Babiak and Dickerson 2022), and a contrarian rule after one-day overreactions is reported as unprofitable (Caporale and Plastun 2019). A daily reversal hypothesis on the point-in-time universe would be registered against the published direction.

## 5. Volatility

### 5a. The leverage effect is inverted: volatility rises more after gains than after losses

**Claim.** In crypto, next-period volatility is higher after positive returns than after negative returns of the same size, the opposite of equities.

- **Reference.** Brini, A. and Lenz, J. (2024). "A Comparison of Cryptocurrency Volatility-benchmarking New and Mature Asset Classes." arXiv:2404.04962. <https://arxiv.org/abs/2404.04962>.
- **Opened.** The HTML version, the first 100,000 of about 144,000 characters (through the per-coin results; I did not read the end).
- **Sample.** 87 coins (the 100 largest by capitalisation less stablecoins) from the Binance API, 5-minute prices, 2020 to October 2022; 42 Nasdaq technology stocks for comparison (Sections 1 and 3.2). No exact start and end day is given.
- **Method.** Daily realised variance from 5-minute returns, split into the part from positive and the part from negative returns; panel heterogeneous-autoregressive models forecasting realised variance 1, 5, 22 and 66 days ahead, with a term for "yesterday's return was negative" (Section 3). In sample only.
- **Direction and size.** The variance from positive returns dominates the forecast for crypto: coefficient 1.262 (t about 10.2) one day ahead, against -0.142 (t about -1.7) for the variance from negative returns (Table 3). The negative-day term is negative for crypto, -0.261 (t about -2.8) one day ahead and -0.076 (t about -3.9) at 22 days, where equities have a positive one (0.115 one day ahead) (Table 4). Per coin, the negative-day term is significant for most coins at 22 and 66 days and almost always negative (Section 4.5). The effect is described as stronger in 2020-21 than in 2021-22 (Section 4.4). Jumps go the conventional way: negative jumps raise later volatility, positive jumps lower it (Table 5). The extraction showed two oddities in the tables (a 66-day row repeating the 1-day values in Table 4, and an implausible t-statistic in Table 3), so check the numbers against the paper.
- **A weaker result on Bitcoin alone.** Kunimoto and Kakamu (reference in 6b), daily Bitcoin 2013-01-01 to 2019-08-31, estimate the correlation between return shocks and volatility shocks at 0.048 with a 95 percent interval of -0.047 to 0.141 (Table 4): positive, as the inverted effect predicts, but not distinguishable from zero.
- **Costs.** Not relevant; nothing is traded.
- **Sample end.** October 2022 (Brini and Lenz); 2019-08-31 (Kunimoto and Kakamu). Both clean.
- **Transfer.** Testable only in part. These are claims about volatility, not about returns: neither paper tests whether the asymmetry forecasts a coin's return. What can be tested here is the volatility claim itself, on realised variance built from hourly bars (24 returns a day instead of 288, so noisier than the paper's measure): next-day realised variance is higher after an up day than after a down day with the same realised variance. Our glossary defines a predictive claim as a signal that forecasts returns, so a Researcher has to decide whether this is a hypothesis or a know-how note. The sample matches our universe unusually well (Binance, large coins). The original result, Baur and Dimpfl 2018, is a lead (abstract only).

### 5b. Volatility is persistent and follows the clock, which is the precondition for volatility-managed exposure

**Claim.** A coin's volatility tomorrow is well predicted by its recent volatility and by the calendar (weekday, hour), so exposure can be scaled against it in advance.

- **Sources.** Hansen, Kim and Kimbrough (reference in 6a) and Kunimoto and Kakamu (reference in 6b).
- **Size.** Persistence of log-volatility for daily Bitcoin 2013 to 2019: 0.918, 95 percent interval 0.890 to 0.942 (Kunimoto and Kakamu, Table 4). Adding weekday effects to a volatility model for 2017-01-01 to 2021-07-31 improves its log-likelihood in and out of sample for both Bitcoin and Ether (Hansen et al., Section 6, Table 2). The calendar pattern itself is in section 6.
- **What is missing.** Volatility-managed exposure pays only if expected return does not rise in step with volatility. That is the finding of the parent paper for equity factors and currency carry (Moreira and Muir 2017, a lead: I read its abstract only), and I found no source I could open that tests it on crypto, for a long-only position or otherwise. A paper on the cross-section (Lee and Wang, a lead with an unknown sample end) states that coins with higher realised variance have lower returns in the following weeks, which would favour scaling down in high volatility if it also holds through time; nobody I could read tests that.
- **Sample end.** 2021-07-31 and 2019-08-31. Clean.
- **Transfer.** Testable only in part, and as our own extension rather than a replication. Long or flat without leverage means exposure can be scaled down but not up: weight = min(1, target volatility / recent realised volatility). The published design (Moreira and Muir) scales in both directions and compares Sharpe ratios and alpha; ours would compare the capped rule with buy-and-hold of the same coin or universe. A predictive version is also possible and has more power: does a coin's recent realised volatility predict its next day's or week's return, sign negative? Origin `literature` is defensible only for the persistence half; the return half has no opened crypto source behind it, so say so in the hypothesis file.

## 6. Calendar effects

### 6a. Weekends are quiet: lower volatility and lower volume on Saturday and Sunday

**Claim.** Volatility and trading volume are lower at weekends than on weekdays, most of all on Saturday.

- **Reference.** Hansen, P. R., Kim, C. and Kimbrough, W. (2021). "Periodicity in Cryptocurrency Volatility and Liquidity." arXiv:2109.12142. <https://arxiv.org/abs/2109.12142>. From memory, not confirmed: later published in the *Journal of Financial Econometrics*.
- **Opened.** The full paper in its HTML rendering.
- **Sample.** BTC and ETH against USD on Coinbase Pro and against USDT on Binance, plus WETH/USDC on Uniswap V2; 1-minute bars, realised variance from 5-minute returns; main sample 2020-10-01 to 2021-06-01, an extended one from 2019-01-01, and 2017-01-01 to 2021-07-31 on Coinbase Pro for the volatility models (Sections 3 and 6).
- **Direction and size.** Volatility and volume are lower at weekends, most markedly on Saturdays; volume varies more than volatility on the centralised exchanges; the pattern is described as stable over time; the confidence bands are wide because the main sample has about 35 weeks (Section 5.1, Figure 3). The paper studies volatility, volume and illiquidity only: it does not examine mean returns by day or hour, and its volatility models keep the mean constant.
- **Agreeing sources.** Kunimoto and Kakamu (6b), daily Bitcoin 2013 to 2019: log-volatility coefficient relative to Wednesday -0.332 on Saturday (95 percent interval -0.598 to -0.074) and -0.394 on Sunday (-0.660 to -0.126); Thursday is higher at 0.289 (0.028 to 0.544) (Table 4). Petukhina, Reule and Härdle (2021), "Rise of the Machines? Intraday High-Frequency Trading Patterns of Cryptocurrencies", *European Journal of Finance*, arXiv:2009.04200 <https://arxiv.org/abs/2009.04200>, opened in full: 11 coins at 5 minutes, but only 2018-07-01 to 2018-08-31; absolute returns peak from about Tuesday to Thursday and drop steeply at weekends, volume and volatility are low at weekends (Figures 8 to 10); no test on mean returns, no numbers in the text.
- **Abstract-level agreement** (leads): Baur, Cahill, Godfrey and Liu 2019 report lower volume at weekends on all seven exchanges they study.
- **Costs.** Not relevant.
- **Sample end.** 2021-07-31 at the latest. Clean.
- **Transfer.** Testable here as a claim about volatility or quote volume on daily or hourly bars (Saturday and Sunday bars against weekday bars, pooled over the point-in-time universe); it is a volatility claim, not a return claim, so the same caveat as in 5a applies. It is the best-supported calendar fact in this file, with three independent samples from 2013 to 2021. Its use for a hypothesis is indirect: it predicts when a volatility-scaled position (5b) would be larger.

### 6b. Day of the week in returns: three sources, three answers

**Claim.** Bitcoin's mean daily return differs by weekday.

- **Reference.** Kunimoto, N. and Kakamu, K. (2021). "Is Bitcoin really a currency? A viewpoint of a stochastic volatility model." arXiv:2111.15351. <https://arxiv.org/abs/2111.15351>.
- **Opened.** The full paper in its HTML rendering.
- **Sample.** Coin Metrics Bitcoin price in dollars, daily closes at 00:00 UTC, 2013-01-01 to 2019-08-31, 2,434 observations; returns are 100 times the log price change (Section 5).
- **Method.** A stochastic volatility model with weekday and holiday dummies in both the return and the volatility equation, Wednesday as the base day, Bayesian estimation; in sample only (Sections 3 and 4).
- **Direction and size (Table 3, percentage points a day relative to Wednesday, posterior mean and 95 percent interval).** Friday 0.415 (0.107 to 0.728), the only day whose interval excludes zero. Tuesday 0.303 (-0.031 to 0.641), Saturday 0.216 (-0.073 to 0.504), Thursday 0.161 (-0.172 to 0.491), Sunday 0.076 (-0.218 to 0.371), Monday 0.063 (-0.261 to 0.389). Wednesday itself: -0.021 (-0.245 to 0.201). The day after a US holiday: 0.784 (0.015 to 1.606); the day before: 0.302 (-0.402 to 1.018).
- **Conflicting abstract-level evidence** (leads). Caporale and Plastun 2019 report that Bitcoin's Monday returns are significantly higher than other days', with no effect in Litecoin, Ripple or Dash; this paper's Monday estimate, on a longer sample, is the smallest of the six. Aharon and Qadan 2019 report a day-of-the-week effect in Bitcoin returns and volatility for 2010 to 2017 (the abstract does not name the day). Baur et al. 2019, on seven exchanges, report that return anomalies by time of day, weekday and month exist but do not persist over time.
- **Costs.** None.
- **Sample end.** 2019-08-31. Clean.
- **Transfer.** Testable here as a predictive claim on daily bars, with a low prior: one coin, one in-sample model, seven weekdays looked at and one found, and the two best-known journal results name a different day or deny persistence. Before registering, fix which bar "Friday" means: the paper dates a return by a 00:00 UTC close, and I could not tell whether its Friday return covers the UTC day Friday (our bar labelled Friday) or ends at Friday 00:00 (our bar labelled Thursday). As a trading claim it is marginal on its own numbers: about 0.4 percentage points for a one-day hold against a round trip of 24 to 50 bps (my arithmetic).

### 6c. Hour of the day in returns: the two hours before midnight UTC

**Claim.** Bitcoin's mean hourly return is highest late in the UTC evening, when no major stock market is open.

- **Reference.** Padyšák, M. and Vojtko, R. (2022). "Are There Seasonal Intraday or Overnight Anomalies in Bitcoin?" Quantpedia research article, 2022-02-18. <https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/>. Practitioner research, not peer reviewed. A companion working paper by the same authors ("Seasonality, Trend-following, and Mean reversion in Bitcoin") is a lead: I could not open it.
- **Opened.** The article.
- **Sample.** Bitcoin on Gemini, hourly, 2015-10-09 to 2022-02-03, hours in UTC.
- **Direction and size.** The hours named 22:00 and 23:00 have the highest and most economically significant mean returns; 03:00 and 04:00 the weakest; no hour has a significantly negative mean; several positive hourly means are significant at 5 percent. The article shows these in charts and gives no hourly numbers. The rule "buy at 21:00 UTC, sell at 23:00 UTC" earns 33 percent a year with 20.93 percent volatility and a maximum drawdown of -22.45 percent.
- **Costs.** Not mentioned.
- **Sample end.** 2022-02-03. Clean. A later follow-up by the same publisher exists; I did not open it and it would overlap the dev segment.
- **Transfer.** Testable here as a predictive claim on hourly bars: the mean return of the two bars covering 21:00 to 23:00 UTC against the mean of the other bars, per coin or pooled. Use the holding window of the trading rule to define the bars (our bars labelled 21:00 and 22:00), because the article does not say whether an hour's name is its start or its end. Not testable as a trading claim with any chance: 33 percent a year from one round trip a day is roughly 9 bps a trade before costs (my arithmetic), against 24 to 50 bps for the round trip. The evidence is one coin on one exchange we do not use, from a practitioner source, and Baur et al. (lead) report that time-of-day return anomalies in Bitcoin do not persist.

### 6d. Hour of the day in volatility and volume: 00:00, 08:00 and 16:00 UTC, and the first minute of every hour

**Claim.** Volatility and volume spike at fixed clock times: at 00:00 and 16:00 UTC, less at 08:00, and in the first minute of each hour.

- **Source.** Hansen, Kim and Kimbrough (2021), as in 6a.
- **Direction and size.** Volatility is high around 16 UTC and lowest near 5 UTC; volume and volatility spike at 0h and 16h with smaller spikes at 8h, on every exchange and both assets (Section 5.2, Figure 4). For BTC/USDT on Binance the first hour of the UTC day and the hour after 16:00 have the highest volatility, and the first hour is especially volatile on Mondays (Figure 6). Binance is about 30 percent less liquid than its average during the East Asian night (Section 5.2.1, Figure 5). Within the hour, volatility peaks in the first minute, with smaller bursts after minutes 15, 30 and 45 and every five minutes; on Binance this is strongest every fourth hour (Section 5.3, Figures 7 and 8). The authors attribute the within-hour pattern to algorithmic trading and conjecture a link to perpetual-futures funding, which Binance settles at 00, 08 and 16 UTC.
- **Agreeing source.** Petukhina, Reule and Härdle (reference in 6a): absolute returns are low at night, rise through the European day and peak in the late afternoon, about 16:00 to 19:00 UTC if the paper's clock is GMT+1 (Figure 7); two months of 2018 only.
- **Costs.** Not relevant.
- **Sample end.** 2021-07-31. Clean.
- **Transfer.** Testable here on hourly bars as a claim about the absolute return or quote volume of the bars labelled 00:00, 08:00 and 16:00 UTC against other bars. The within-hour part is not testable: we have no bars shorter than an hour. No source says these hours have different mean returns, so a return hypothesis built on funding times would be `exploration`, not `literature`. For any rule that trades at a bar's open it is a warning as much as a lead: 00:00 UTC, where every daily rule of ours trades, is one of the most volatile moments of the day.

## 7. Intraday momentum, and volume as a predictor of a coin's own return

I could open no full text on either topic beyond the hourly autocorrelation evidence in 4a. What 4a adds here:

- **Sign differs by coin.** At lag 1 on hourly bars Bitcoin reverses while the two Ethereum pairs continue, in the one paper that reports both (Tartakovsky et al., Section 5.1, sample to 2019-07-01). "Hourly momentum" and "hourly reversal" are therefore both published for large coins, on different coins, and the paper contradicts itself on Ethereum in its rolling analysis.
- **A lag-16 effect.** All four markets show a significant positive autocorrelation at lag 16 on hourly bars (same section). Unexplained and unreplicated; testable here on hourly bars as a predictive claim, but treat it as one chance finding among 30 lags tested until someone finds a second source.

The published patterns for this sub-angle are all abstract-level and are listed in the leads: the first half-hour of the day predicting the last (Shen, Urquhart and Wang 2022), intraday momentum together with reversal (Wen, Bouri, Xu and Zhao 2022), volume predicting returns outside bull and bear regimes (Balcilar et al. 2017), volume predicting extreme returns (Bouri et al. 2019), and the interaction of lagged return and volume (Bianchi, Babiak and Dickerson 2022).

## What transfers to our setup (second run)

Setup as before, plus hourly bars labelled in UTC, signal at a bar's close, trade at the next open.

- **Costs rule out most intraday trading claims before they are run.** A round trip is 24 to 50 bps. The one intraday rule with a published return (6c) earns about 9 bps a trade gross (my arithmetic). No opened source reports an hourly effect that is profitable after costs. Hourly hypotheses from this file should be predictive claims.
- **Half of what is well supported is about volatility, not returns.** Weekend calm (6a), clock-time spikes (6d), the inverted leverage effect (5a) and persistence (5b) are solid as descriptions. Turning them into return hypotheses is our own step, and the origin should say so.
- **Signal at the close, trade at the next open** is harmless for calendar rules (the clock is known in advance) and for daily autocorrelation (the next daily bar opens when the signal bar closes). For hourly autocorrelation it is exactly the published lag-1 design.
- **Day and hour labels need care.** Papers name a day or an hour without saying whether the name is the start or the end of the period (6b, 6c). Our bar label is the opening time. Fix the mapping in the hypothesis file before any run.
- **Long or flat.** Nothing in sections 4 to 7 depends on a short leg; the constraint that binds here is "no leverage" in 5b.
- **The universe is wider than the evidence** again: Bitcoin and sometimes Ether for every intraday and calendar entry; only 5a covers a broad set of Binance coins.

## Unverified leads (second run)

Abstract or listing only unless stated. Nothing here is evidence until someone reads the paper. Grouped by sub-angle; the access problem is given once per group where it is the same.

**Reversal.** Publisher paywalls; the working-paper PDFs answered with an unreadable binary.

- **De Nicola, G. (2021). "On the Intraday Behavior of Bitcoin." *Ledger* 6, 58-80. DOI 10.5195/ledger.2021.213.** Abstract ([journal page](https://ledger.pitt.edu/ojs/ledger/article/view/213)): significant negative first-order autocorrelation of Bitcoin returns at one, two and four hours; larger moves are followed by stronger reversals; a simple trading strategy illustrates it; explanations offered are overreaction and cascading liquidations. The abstract gives no sample dates (a search summary says 2015 to 2018) and nothing on costs. Open access but PDF only. Read this first: it is the direct source for an hourly reversal hypothesis and for "after large moves".
- **Caporale, G. M. and Plastun, A. (2019). "Price overreactions in the cryptocurrency market." *Journal of Economic Studies* (journal inferred from the listing); CESifo Working Paper 6861 (2018).** Abstract ([listing](https://econpapers.repec.org/RePEc:ces:ceswps:_6861)): Bitcoin, Litecoin, Ripple and Dash; after a one-day overreaction the next day's move is larger than after normal days in both directions; a contrarian trading rule is unprofitable; a continuation rule makes money but not significantly more than random trading; the authors see no exploitable opportunity. Sample dates not in the abstract (before 2018). A published null for daily reversal after large moves.
- **Zaremba, A., Bilgin, M. H., Long, H., Mercik, A. and Szczygielski, J. J. (2021). "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets." *International Review of Financial Analysis* 78, 101908. DOI 10.1016/j.irfa.2021.101908.** Abstract ([listing](https://ideas.repec.org/a/eee/finana/v78y2021ics1057521921002349.html)): across more than 3,600 coins, coins with a low return on the last day outperform those with a high one; the reversal comes from illiquidity, and the few largest, most tradeable coins show daily momentum instead. Cross-sectional. Sample dates not in the abstract (before 2021).
- **Bianchi, D., Babiak, M. and Dickerson, A. (2022). "Trading volume and liquidity provision in cryptocurrency markets." *Journal of Banking & Finance* 142, 106547. DOI 10.1016/j.jbankfin.2022.106547.** Abstract ([listing](https://econpapers.repec.org/RePEc:eee:jbfina:v:142:y:2022:i:c:s0378426622001418)): pairs against the dollar on several centralised exchanges, 2017-03-01 to 2022-03-01; profits of a short-term reversal strategy are concentrated in pairs with low trading activity and are larger in smaller, more volatile, less liquid pairs; in a panel regression the interaction of lagged return and volume predicts returns. Sample end 2022-03-01, clean. Also the main lead for volume as a predictor.
- **Corbet, S. and Katsiampa, P. (2020). "Asymmetric mean reversion of Bitcoin price returns." *International Review of Financial Analysis*.** Search summary only: minute, hourly, daily and weekly Bitcoin returns 2010 to 2018, asymmetric reverting patterns. The repository page was behind a bot check.
- **Fičura, M. (2023). "Impact of size and volume on cryptocurrency momentum and reversal." FFA Working Papers 5.003, Prague University of Economics and Business.** Abstract ([page](https://wp.ffu.vse.cz/artkey/wps-202301-0003_impact-of-size-and-volume-on-cryptocurrency-momentum-and-reversal.php)): weekly reversal only in small, illiquid coins and weekly momentum in large, liquid ones. **Hindsight flag: the abstract gives no sample dates and the paper is from 2023; treat it as overlapping the dev segment until checked.** Claim only.
- **Kitron, N. A. and Wengrowicz, J. M. (2026). "Short-horizon mean reversion in cryptocurrency markets: a matched cross-market measurement." arXiv:2608.21888.** Abstract: 15-minute reversal in the sign of returns on 183 Binance pairs, much stronger than in US stocks, strongest after moves driven by aggressive orders, and by the authors' own account too small to cover spot trading costs. **Hindsight flag: the sample runs from 2021 into the dev or test segment.** Claim only.

**Volatility.**

- **Baur, D. G. and Dimpfl, T. (2018). "Asymmetric volatility in cryptocurrencies." *Economics Letters* 173, 148-151. DOI 10.1016/j.econlet.2018.10.008.** Abstract ([listing](https://econpapers.repec.org/RePEc:eee:ecolet:v:173:y:2018:i:c:p:148-151)): in the 20 largest coins positive shocks raise volatility more than negative ones; explained by uninformed buying after gains. Paywalled. Sample ends by 2018, clean. The original of 5a.
- **Moreira, A. and Muir, T. (2017). "Volatility-Managed Portfolios." *Journal of Finance* 72(4), 1611-1644. DOI 10.1111/jofi.12513.** Abstract ([NBER page](https://www.nber.org/papers/w22208)): portfolios that cut exposure when volatility is high earn large alphas and higher Sharpe ratios for the equity market, several equity factors and currency carry, because expected returns do not rise in proportion to volatility. No crypto. The parent of 5b; I did not open the full text.
- **Lee, S. S. and Wang, M. (2025). "Variance Decomposition and Cryptocurrency Return Prediction." *Journal of Financial and Quantitative Analysis* 60(4), 1859-1890. DOI 10.1017/S002210902400022X.** Abstract ([publisher page](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/variance-decomposition-and-cryptocurrency-return-prediction/9995E58095453CB44A3BC3C9C111969F)): from intraday data, coins with higher realised variance have lower returns in the following weeks, driven by the positive-jump and jump-robust parts, more so in small, illiquid coins. Cross-sectional. Open access, but the page served only the abstract. **Hindsight flag: sample dates not in the abstract; unknown until checked.** Claim only.
- **Yang, A. (2025). "Cryptocurrency market risk-managed momentum strategies." *Finance Research Letters* 85, 107879;** and an article on volatility-managed crypto momentum in *Financial Markets and Portfolio Management* (2025, DOI 10.1007/s11408-025-00474-9). Seen only in search results and a reference list; not opened. **Hindsight flag: both from 2025, samples unknown.** They concern momentum portfolios, not a long-only position.

**Calendar effects.** All paywalled except where noted.

- **Caporale, G. M. and Plastun, A. (2019). "The day of the week effect in the cryptocurrency market." *Finance Research Letters* 31 (journal from a secondary citation); CESifo Working Paper 6716 (2017).** Abstract ([listing](https://econpapers.repec.org/RePEc:ces:ceswps:_6716)): no weekday effect in Litecoin, Ripple or Dash; Bitcoin's Monday returns are significantly higher; a trading simulation suggests it could be exploited. Sample dates not in the abstract (before 2018).
- **Aharon, D. Y. and Qadan, M. (2019). "Bitcoin and the day-of-the-week effect." *Finance Research Letters* 31, 415-424. DOI 10.1016/j.frl.2018.12.004.** Abstract ([university page](https://cris.haifa.ac.il/en/publications/bitcoin-and-the-day-of-the-week-effect/)): a day-of-the-week effect in Bitcoin returns and volatility, daily data 2010 to 2017, robust across subsamples. The abstract does not name the day; secondary sources say Monday.
- **Baur, D. G., Cahill, D., Godfrey, K. and Liu, Z. (2019). "Bitcoin time-of-day, day-of-week and month-of-year effects in returns and trading volume." *Finance Research Letters* 31, 78-92. DOI 10.1016/j.frl.2019.04.023.** Abstract ([listing](https://econpapers.repec.org/RePEc:eee:finlet:v:31:y:2019:i:c:p:78-92)): more than 15 million observations from seven exchanges; return anomalies tied to the calendar exist but do not persist over time; volume is consistently lower in local evenings and at weekends. The main published null for calendar effects in returns. Sample ends before 2019.
- **Miralles-Quirós, J. L. and Miralles-Quirós, M. M. (2022). "A new perspective of the day-of-the-week effect on Bitcoin returns: evidence from an event study hourly approach." *Oeconomia Copernicana* 13(3), 745-782. DOI 10.24136/oc.2022.022.** Abstract ([journal page](https://journals.economic-research.pl/oc/article/view/2091)): hourly closes on Kraken, January 2016 to December 2021; mean returns for each of the 24 hours of each weekday; some hourly means are significant, and rules that hold over certain windows after them beat buy-and-hold on the Sharpe ratio. The abstract does not name the hours. Open access but PDF only. Sample end 2021-12, clean. The only source found that crosses weekday with hour, which is exactly what hourly bars can test: read it before registering a weekday-by-hour hypothesis.
- **Shanaev, S. and Ghimire, B. (2022). "A generalised seasonality test and applications for cryptocurrency and stock market seasonality." *Quarterly Review of Economics and Finance*.** Search summary only: argues that conventional seasonality tests are unreliable for crypto; cites a Kumar (2022) study reporting a positive turn-of-the-month effect in Bitcoin, Ethereum and Litecoin, which I could not find.
- **Kaiser, L. (2019). "Seasonality in cryptocurrencies." *Finance Research Letters* 31.** Secondary summary only: ten coins, 2013 to 2018; volume, volatility and spreads lower in January; little in returns.
- **"Turn-of-the-candle effect in bitcoin returns." *Heliyon* (2023).** Search summary only (the open-access page was behind a bot check): positive Bitcoin returns are concentrated in the minute at the turn of each 15-minute candle. **Hindsight flag: published 2023, sample end unknown.** Not testable on hourly bars in any case.
- **Kim, C. and Hansen, P. R. (2026). "The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures." arXiv:2607.09426.** Abstract: on six Binance perpetual contracts, order imbalance at quarter-hour openings predicts returns over about four to twelve hours. Futures, trade-level data we do not hold. **Hindsight flag: sample dates not in the abstract; a 2026 paper.** Claim only.
- **Padyšák, M. and Vojtko, R. (2022). "Seasonality, Trend-following, and Mean reversion in Bitcoin." SSRN working paper.** Not opened (the summary page returned an error). From memory, not confirmed: it also reports that Bitcoin continues after a multi-day high and rebounds after a multi-day low on daily data.

**Intraday momentum and volume.** All paywalled.

- **Shen, D., Urquhart, A. and Wang, P. (2022). "Bitcoin intraday time series momentum." *Financial Review* 57(2), 319-344. DOI 10.1111/fire.12290.** Abstract ([university page](https://research.birmingham.ac.uk/en/publications/bitcoin-intraday-time-series-momentum/)): the day's opening and closing are set by trading volume because Bitcoin has no close; the first half-hour's return positively predicts the last half-hour's; strongest when the first half-hour has high volume or volatility; timing on it gives economic gains, most in downturns; attributed to liquidity provision. Sample dates not in the abstract (before 2021). The accepted manuscript exists in a university repository, which was unreachable or behind a bot check. Read before registering "first hours predict last hours": the paper's day boundaries come from volume, not from 00:00 UTC, and half-hours are below our granularity.
- **Wen, Z., Bouri, E., Xu, Y. and Zhao, Y. (2022). "Intraday return predictability in the cryptocurrency markets: Momentum, reversal, or both." *North American Journal of Economics and Finance* 62, 101733. DOI 10.1016/j.najef.2022.101733.** Abstract ([listing](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html)): Bitcoin 2013-03-03 to 2020-05-31, also Ethereum, Litecoin and Ripple; both intraday momentum and intraday reversal exist, and which one depends on jumps, announcement days, liquidity and the 2020 crisis; a timing strategy beats always-long and buy-and-hold. Nothing on costs in the abstract. Sample end 2020-05-31, clean.
- **Balcilar, M., Bouri, E., Gupta, R. and Roubaud, D. (2017). "Can volume predict Bitcoin returns and volatility? A quantiles-based approach." *Economic Modelling* 64, 74-81. DOI 10.1016/j.econmod.2017.03.019.** Abstract ([listing](https://econpapers.repec.org/RePEc:eee:ecmode:v:64:y:2017:i:c:p:74-81)): daily Bitcoin 2011-12-19 to 2016-04-25; volume predicts returns except in bear and bull regimes (a search summary gives the quantile range 0.25 to 0.75); volume does not predict volatility at any quantile. A causality test: it says volume carries information, not in which direction. Clean.
- **Bouri, E., Lau, C. K. M., Lucey, B. and Roubaud, D. (2019). "Trading volume and the predictability of return and volatility in the cryptocurrency market." *Finance Research Letters* 29, 340-346. DOI 10.1016/j.frl.2018.08.015.** Search summary only: seven coins, daily; volume Granger-causes extreme negative and positive returns in all of them, and volatility in three only. Again no direction. Sample ends by 2018, clean.
- **Zhang, Y., Chan, S., Chu, J. and Sulieman, H. (2020). "On the Market Efficiency and Liquidity of High-Frequency Cryptocurrencies in a Bull and Bear Market." *Journal of Risk and Financial Management* 13(1), 8.** Search summary only (the open-access page refused the request): hourly Bitcoin, Ethereum and Litecoin, 2017-07-11 to 2018-09-19; hourly returns look efficient in the bull phase and less so in the bear phase. Clean.

**Files the fetch tool saved.** Five PDF links (two working-paper copies of Bianchi et al., Balcilar et al., Caporale and Plastun on overreactions, and a file that a search listed for their day-of-the-week paper) answered with a binary that the tool stored in the session's tool-results folder. I did not open them and did not retry.

## Where I found nothing (second run)

- No source I could open tests volatility-managed exposure on crypto, for a long-only position or at all, and none tests whether a coin's own past realised volatility predicts its own next return.
- No full text on volume as a time-series predictor of a coin's own return; the abstract-level results are causality tests without a direction.
- No full text on intraday momentum (first hours predicting last hours).
- No study of a turn-of-the-month effect that I could trace to a source.
- No evidence that funding times (00:00, 08:00, 16:00 UTC) or the US or Asian session opens move mean spot returns; the evidence is on volatility and volume only.
- No "overnight against intraday" analogue beyond the late-evening hours in 6c.
- No intraday or calendar test on a broad, liquidity-ranked universe; outside 5a everything is Bitcoin, sometimes Ether.
