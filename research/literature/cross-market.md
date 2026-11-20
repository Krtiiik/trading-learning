# Cross-market and external: literature notes

Collected by the Literature scout on 2026-11-19. Brief of this run: published evidence on links between cryptocurrencies and between crypto and other markets that could predict crypto spot returns, across four sub-angles: (1) Bitcoin-to-altcoin lead-lag, (2) links to equities, the dollar, rates, gold, volatility and macro announcements, (3) market-wide state variables built from crypto prices alone, (4) on-chain and sentiment data, including whether a free, point-in-time series exists for each.

How to read an entry:

- Numbers are the paper's own, in its units, with the table or figure they come from. Arithmetic of mine is marked "(my arithmetic)".
- "Opened" says which version I read. **Access was poor in this run**: every PDF I requested came back unreadable, and most publisher pages refused the connection. The numbered sections therefore hold only sources whose full text I read as an HTML page (PubMed Central, PLOS, the arXiv HTML mirror). I read them through a text-extraction tool, not by eye, so check a number against the paper's table before it goes into a registration.
- Everything I could read only as an abstract is under "Unverified leads", as the brief asked, grouped by sub-angle. For sub-angle 1 that is all there is.
- "Sample end" is checked against the split: a sample ending by 2022-12-31 is clean evidence for the train segment; anything later, or unknown, is flagged.
- Every source in the numbered sections ends by 2022-12-21. The flagged ones are all under "Unverified leads".

Coverage in one glance:

| Sub-angle | Opened in full | Abstract only | Verdict of the evidence |
| --- | --- | --- | --- |
| 1. Bitcoin-to-altcoin lead-lag | 0 | 5 | One strong positive claim (Guo et al.), two published nulls at hourly and daily horizons |
| 2. Equities, dollar, rates, gold, macro news | 3 (sections 3, 4, 5) | 6 | Reaction to macro surprises inside minutes; no published test of "previous US session predicts next-day crypto" found |
| 3. State variables from crypto prices | 1 (section 8) | 1 | Descriptive only; no predictive test found |
| 4. On-chain and sentiment | 4 (sections 1, 2, 6, 7) | 7 | Several positive results, all on data that is not free and point-in-time |

Sections are ordered by how strong the evidence is for something we could test.

## 1. Twitter opinion polarization and exchange volume precede Bitcoin returns by a day (sub-angle 4)

**Claim.** A rise in the polarization of opinion in Bitcoin tweets, and a rise in exchange trading volume, are each followed by a higher Bitcoin return on the next day.

- **Reference.** Garcia, D. and Schweitzer, F. (2015). "Social signals and algorithmic trading of Bitcoin." *Royal Society Open Science* 2: 150288. DOI [10.1098/rsos.150288](https://doi.org/10.1098/rsos.150288). Preprint arXiv:1506.01513.
- **Opened.** The arXiv version as HTML: <https://ar5iv.labs.arxiv.org/html/1506.01513>. The publisher's page refused the connection. The supplementary material (coefficients of the vector autoregression, long-only variants) was not opened.
- **Sample.** Bitcoin, daily, closing value of the CoinDesk price index at 23:59 GMT, 2011-02-01 to 2014-12-31; backtests on the Bitfinex BTC/USD rate. Signals: exchange volume summed over about 80 markets, on-chain transaction count, downloads of the Bitcoin client, Google search volume, daily tweet count, emotional valence of tweets, opinion polarization of tweets. All non-return signals are first-differenced and standardised.
- **Method.** A vector autoregression with one daily lag fitted on data up to 2014-01-01, impulse responses with bootstrapped intervals, then trading strategies evaluated on a leave-out period after that date (its exact dates are not stated in the text I read; the price series ends 2014-12-31, a year of falling prices).
- **Direction and size.** Polarization and exchange volume have a significant positive effect on the return one day after a shock, which decays quickly (Fig. 3A); the cumulative effects of polarization, valence and exchange volume reach about 0.5 percent within a day (Fig. 3D). Valence leads polarization and volume rather than returns directly (Fig. 3B and 3C). Google search volume, tweet count and on-chain transaction count do not come out as leading returns.
- **Trading result (Table 1, leave-out period).** Annualised Sharpe ratio: combined strategy (majority vote of three signals) 1.77, polarization 1.01, valence 0.64, exchange volume 0.57, a price-momentum benchmark 0.91, buy-and-hold -0.77. Mean daily return as tabulated: 0.32 for the combined strategy against -0.16 for buy-and-hold (percent, as I read the table).
- **Costs.** Considered. With equal costs for buying, selling and borrowing between 0 and 0.3 percent of traded capital, the combined strategy stops being profitable above about 0.25 percent (Fig. 5).
- **Shorting.** The strategies go long and short. In a falling year the short side carries the profit: the paper says a short-only variant earns more than the long-only one (supplement, not opened).
- **Sample end.** 2014-12-31. Clean.
- **Transfer.** Testable only in part. The Twitter signals are not testable: there is no free historical tweet archive (see "Free point-in-time series"). The exchange-volume half is testable here as a predictive claim on daily bars: the standardised day-on-day change in aggregate quote volume (Bitcoin's, or the point-in-time universe's) against the next day's return, predicted sign positive. As a long-or-flat trading claim it is weaker than the table suggests, because the published profit is from 2014 and leans on shorting. One sample year, one coin.

## 2. Search attention and price feed each other; attention leads in bubbles (sub-angle 4)

**Claim.** Rising search interest in Bitcoin is followed by rising prices, and rising prices by rising search interest; the effect of attention is conditional on whether the price is above or below its recent trend.

### 2a. Kristoufek 2013

- **Reference.** Kristoufek, L. (2013). "BitCoin meets Google Trends and Wikipedia: Quantifying the relationship between phenomena of the Internet era." *Scientific Reports* 3: 3415. DOI [10.1038/srep03415](https://doi.org/10.1038/srep03415).
- **Opened.** The full text on PubMed Central: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3849639/>.
- **Sample.** Bitcoin against the dollar on Mt. Gox, 2011-05-01 to 2013-06-30. Google Trends weekly (113 observations, prices averaged to weeks), Wikipedia page views daily (788 observations).
- **Method.** Google Trends: a vector autoregression with one weekly lag on log differences. Wikipedia: a vector error-correction model with seven daily lags. A dummy splits each attention series by whether the price is above or below its moving average (4 weeks for Google, 7 days for Wikipedia).
- **Direction and size.** A 10 percent shock to search queries is followed by a price about 0.8 percent higher in the first week and about 1.2 percent in the second, then nothing (Fig. 4). The reverse also holds: a 10 percent price shock raises searches by about 0.8 percent in total. For Wikipedia, views respond to prices; views lead prices only once split by trend: more views push the price further up when it is above trend and further down when it is below (Fig. 5). For Google the response is almost entirely in the above-trend state.
- **Costs.** Not considered. No out-of-sample test and no trading rule.
- **Sample end.** 2013-06-30. Clean, but it is two years of one early exchange.

### 2b. Kristoufek 2015: the same author, wavelets, longer sample

- **Reference.** Kristoufek, L. (2015). "What Are the Main Drivers of the Bitcoin Price? Evidence from Wavelet Coherence Analysis." *PLOS ONE* 10(4): e0123923. DOI [10.1371/journal.pone.0123923](https://doi.org/10.1371/journal.pone.0123923).
- **Opened.** The published article: <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0123923>.
- **Sample.** CoinDesk Bitcoin price index, 2011-09-14 to 2014-02-28 (the text also mentions April 2014 as the end; the paper is not consistent). Google Trends weekly, rebuilt to daily by chaining three-month downloads; Wikipedia views daily.
- **Finding.** Co-movement of price and search interest is strongest at long scales. Until mid-2012 prices lead interest; in the bubble of early 2013 interest leads prices at scales of about 30 to 100 days; in the decline that followed the correlation turns negative at shorter scales with interest still leading.
- **Limits.** Wavelet coherence only: "leads" is a phase relation in co-movement, not a forecast. No regression of future returns, no out-of-sample test.
- **Sample end.** 2014-02-28 (or 2014-04). Clean.

**Transfer for section 2.** Not testable as published: Google Trends is not a point-in-time series (see "Free point-in-time series"), and the author's own chaining of three-month downloads shows the problem. A Wikipedia page-view version may be testable if the Data steward confirms the series; the registrable claim would be the conditional one of 2a: "a rise in daily views while the price is above its 7-day average is followed by a positive return; below it, by a negative one". The evidence is Bitcoin only and ends in 2014.

## 3. Macro announcements: Bitcoin falls on inflation surprises within minutes; no announcement premium (sub-angle 2)

**Claim.** Bitcoin's price falls when US inflation comes in above the survey forecast; it does not react to growth news, and its return in the announcement window is zero on average.

- **Reference.** Pinchuk, M. "Bitcoin Does Not Hedge Inflation." Working paper dated 2021-05-30, posted as arXiv:2301.10117 in January 2023. <https://arxiv.org/abs/2301.10117>. Not peer reviewed as far as I could see.
- **Opened.** The full paper as HTML: <https://ar5iv.labs.arxiv.org/html/2301.10117>.
- **Sample.** Bitcoin, Ethereum, Ripple, Litecoin, Cardano and Bitcoin Cash at 1-minute frequency (exchange not named in what I read); Bitcoin from March 2013; all series to 2021-05-12. Announcements: CPI and PPI for inflation; GDP, personal consumption expenditure, payrolls, unemployment, ISM manufacturing, construction spending and retail sales for growth. FOMC announcements are not in the sample. A surprise is the release minus the mean Bloomberg survey forecast, in standard deviations.
- **Method.** Event study: the return from 10 minutes before to 20 minutes after each release, regressed on the surprise.
- **Direction and size.** Bitcoin: -0.238 percent (about -24 bps) per one-standard-deviation inflation surprise, t = -2.44, adjusted R-squared 0.025, 195 announcements (Table 6). Bitcoin Cash about -18 bps, significant at 5 percent; Ripple about -11 bps and the other coins not significant. No significant response to growth news apart from one consumption series (Table 7). No relation to the move in the 5-year Treasury yield in the same window (Table 9).
- **The null inside it.** Returns in the announcement window are centred on zero: no announcement premium (Table 4, Section 2). The paper does not look at drift before announcements.
- **Costs.** Not considered.
- **Sample end.** 2021-05-12. Clean.
- **Transfer.** Testable only in part. The surprise needs survey forecasts, which we do not have. The 30-minute reaction is over before an hourly bar closes: CPI is released at 08:30 New York time, half past the hour in UTC, so by the time we see the bar and trade at the next open the published effect has happened. What is testable is the paper's null as a calendar-type hypothesis on hourly bars: "the hour containing a CPI release, and the hours after it, have no higher mean return than the same hour on other days". That needs a file of release dates (the statistics office publishes its schedule; it is not in the Store). An effect of 24 bps per standard deviation is also the size of one of our round trips.

## 4. FOMC days: an unexpected rate rise lowers Bitcoin and Ethereum; the plain FOMC-day mean is positive but untested (sub-angle 2)

**Claim.** On FOMC announcement days the returns of Bitcoin and Ethereum fall with the unexpected part of the rate change.

- **Reference.** Kyriazis, A., Ofeidis, I., Palaiokrassas, G. and Tassiulas, L. (2023). "Monetary Policy, Digital Assets, and DeFi Activity." arXiv:2302.10252. <https://arxiv.org/abs/2302.10252>. Working paper.
- **Opened.** The full paper as HTML: <https://ar5iv.labs.arxiv.org/html/2302.10252>.
- **Sample.** Daily returns of a Bitcoin index (NYSE Bitcoin Index), an Ethereum index (S&P), two broad crypto indices (S&P, with and without Bitcoin and Ethereum) and the Nasdaq, 2018-01-01 to 2022-12-21; 43 FOMC announcement days. I did not check at what time of day these indices fix their daily value.
- **Method.** Regression of the announcement-day return on the change in the policy rate and on its unexpected part, taken from fed funds futures, following Bernanke and Kuttner.
- **Direction and size (Table 3).** A one-percentage-point unexpected rise goes with a Bitcoin return lower by about 26.3 percent (t about -2.45) and an Ethereum return lower by about 30.3 percent (t about -2.49); adjusted R-squared about 11 percent. With heteroskedasticity-robust errors the Bitcoin coefficient is no longer significant, and the authors say 43 observations may be too few.
- **Unconditional FOMC-day returns (Table 2).** Mean return on announcement days: Bitcoin 0.32 percent (standard deviation 4.24), Ethereum 1.41 (4.81), the broad index without Bitcoin and Ethereum 1.89, Nasdaq 0.04. The paper does not test these against other days. Against zero they give t of about 0.5 for Bitcoin and 1.9 for Ethereum (my arithmetic, 43 days).
- **Costs.** Not considered.
- **Sample end.** 2022-12-21. Clean: inside the train segment, to its last days.
- **Transfer.** Testable only in part. The surprise needs fed funds futures, which we do not have. The calendar version is testable on daily and hourly bars with a file of FOMC dates (public, fixed a year ahead; not in the Store): "the mean return on FOMC days differs from other days" or, on hourly bars, "the hours after the 19:00 UTC statement (18:00 in summer) differ". The published means are small against their dispersion, so the prior is a null for Bitcoin and a weak positive for the rest.

## 5. No stable link from gold or financial stress to Bitcoin (sub-angle 2, a published null)

**Claim.** Bitcoin's price has no lasting relation to gold or to a financial stress index; it is not a safe haven.

- **Reference and access.** Kristoufek (2015), as in 2b.
- **Sample.** CoinDesk Bitcoin price index, 2011-09-14 to 2014-02-28; the Cleveland Fed Financial Stress Index; gold priced in Swiss francs.
- **Finding.** Financial stress leads the Bitcoin price upward in one episode only, the Cypriot crisis of early 2013, at a scale of about 30 days. Otherwise no reliable relation. For gold there is practically none; the two regions of significant coherence near 60 days lie mostly outside the reliable area.
- **Limits.** Wavelet coherence, not a forecast test. The sample ends before institutional money arrived; the rise of the correlation with equities after 2020 (see the leads on Iyer 2022) is not covered.
- **Sample end.** 2014-02-28. Clean.
- **Transfer.** Testable here as a predictive claim with a predicted null or, registered the other way, a deliberately weak prior: the return of GLD (or SPY, TLT) on session D against the crypto return over the following day. The ETF bar dated D is final at about 21:00 UTC (20:00 in summer), three to four hours before the crypto bar dated D closes, so the clean daily design is "ETF return of session D, trade at the open of crypto bar D+1"; an hourly design can act at the first hourly open after the US close. A financial stress index or VIX is not in the Store.

## 6. On-chain usage leads price only at long horizons and fades; mining follows price (sub-angle 4)

**Claim.** More use of Bitcoin for transactions goes with a higher price in the long run, with usage leading; hash rate and difficulty follow the price.

- **Reference and access.** Kristoufek (2015), as in 2b.
- **Sample.** Daily series from Blockchain.info, 2011-09-14 to 2014-02-28: coins in circulation, transactions excluding exchange activity, output volume, the ratio of trade to exchange volume, hash rate, difficulty.
- **Finding.** Non-exchange transactions are positively related to the price at long scales with transactions leading; the relation weakens and is no longer significant from January 2013. The trade-to-exchange ratio is negatively related to the price in the long run, strong but not significant at 5 percent, with no clear leader; at short scales the price leads it. Hash rate and difficulty move with the price with the price leading, and that also weakens over time.
- **Limits.** Coherence only; horizons of months; no forecast test; no costs.
- **Sample end.** 2014-02-28. Clean.
- **Transfer.** Testable only in part, and only for Bitcoin: transaction counts and hash rate are computed from the chain and exist as free series (see "Free point-in-time series"), but the published relation is slow (scales near 128 days), had already faded inside the paper's sample, and says nothing about altcoins. Garcia and Schweitzer (section 1) also find that the on-chain transaction count does not lead daily returns. The prior for a daily or hourly predictor built from transaction counts is a null.

## 7. Twitter volume and sentiment for altcoins at 3-hour sampling: weak out of sample (sub-angle 4)

**Claim.** The number of tweets about an altcoin and their sentiment predict its return (measured in Bitcoin) over the next 3 to 24 hours.

- **Reference.** Steinert, L. and Herff, C. (2018). "Predicting altcoin returns using social media." *PLOS ONE* 13(12): e0208119. DOI [10.1371/journal.pone.0208119](https://doi.org/10.1371/journal.pone.0208119).
- **Opened.** The full text on PubMed Central: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6279012/>.
- **Sample.** 181 altcoins, 131 kept; prices in Bitcoin from an aggregator, sampled every three hours; 426,520 tweets (at most 100 per query). Training 2017-03-21 to 2017-05-05, test 2017-05-09 to 2017-06-04: 71 days in all.
- **Method.** One linear regression per coin of the return 3 to 24 hours ahead on tweet count and four sentiment scores; the five coins with the best training fit are studied further; Bonferroni correction.
- **Direction and size.** The best training R-squared is 0.242 (Ethereum, 3 hours). On the test period every R-squared falls: the highest are 0.107 and 0.062, both for micro-caps; Ethereum's is 0.025 at 24 hours; 16 of 40 predictions stay significant. The best lag differs by coin and between training and test. Pooled over coins, tweet count and neutral sentiment are significant; the text I read does not give the sign.
- **Costs.** Not considered; no trading test.
- **Sample end.** 2017-06-04. Clean.
- **Transfer.** Not testable: no free historical tweet data, returns are against Bitcoin, most of the coins are micro-caps outside a top-40 universe, and the sample is ten weeks in a bull market. It is useful as a prior: the one intraday multi-coin sentiment study I could open loses most of its fit out of sample.

## 8. Dispersion of coin returns shrinks in large market moves (herding), at hourly but not daily frequency (sub-angle 3)

**Claim.** In large market moves coin returns bunch together more than a linear relation predicts (herding), visible in hourly data.

- **Reference.** Yarovaya, L., Matkovskyy, R. and Jalan, A. (2021). "The effects of a 'black swan' event (COVID-19) on herding behavior in cryptocurrency markets." *Journal of International Financial Markets, Institutions and Money* 75: 101321. DOI [10.1016/j.intfin.2021.101321](https://doi.org/10.1016/j.intfin.2021.101321).
- **Opened.** The full text on PubMed Central (<https://pmc.ncbi.nlm.nih.gov/articles/PMC8612810/>), first 100,000 characters of about 138,000; the remainder (appendix and references, by position) was not read.
- **Sample.** Hourly closes, 2019-01-01 to 2020-03-13, for three to seven coins in each of four quote currencies (dollar, euro, yen, won): Bitcoin, Ethereum, Litecoin and a few others.
- **Method.** Cross-sectional absolute deviation of coin returns regressed on the absolute market return and its square (Chang, Cheng and Khorana); a negative coefficient on the square indicates herding; separate terms for rising and falling markets.
- **Finding.** Herding in the dollar, euro and yen markets, none in the won market (Table 2); present in rising and falling markets for the dollar (Table 3); not amplified by the COVID crash; declining toward the end of the sample. The authors say that the same test on daily data gave insignificant results.
- **Limits.** Contemporaneous only. The paper does not test whether dispersion or herding predicts later returns, and neither did any other source I could open.
- **Sample end.** 2020-03-13. Clean.
- **Transfer.** Not a published predictive claim, so it cannot motivate a `literature` hypothesis about returns by itself. What transfers is the measurement: cross-sectional absolute deviation of hourly returns across the point-in-time universe is a ready-made state variable, and the paper's remark about frequency says to build it from hourly bars. A hypothesis that low dispersion predicts returns would be `exploration` unless the lead under sub-angle 3 below is opened and confirms it.

## Free point-in-time series: what I could establish

The brief's test: a series is usable only if its past values are not revised and it can be had without an account or key. I did not call any data endpoint; this is from provider pages only.

| Series | Free, no account or key | Past values fixed | What I read |
| --- | --- | --- | --- |
| Crypto Fear and Greed index (alternative.me) | Yes: the page documents an open endpoint with JSON or CSV output and the full history on request; attribution is required | **Not established.** The page says nothing about revisions and has no change log | <https://alternative.me/crypto/fear-and-greed-index/>. Bitcoin only. Components and weights: volatility 25, momentum and volume 25, social media 15, surveys 15 (stated as currently paused), dominance 10, Google Trends 10. With surveys paused and a Reddit input announced but not live, the definition has changed over time and the page does not say how. Half of it is computed from price and volume, which we already have. Start of history not stated on the page (February 2018, from memory) |
| Coin Metrics community data (per-asset CSV files) | Yes for the archive: a public repository of CSV files, updated daily, licence CC BY-NC 4.0 (non-commercial) | **Not established.** Nothing on revisions; the page warns that the set of assets and metrics can change at any time | <https://github.com/coinmetrics/data>. I could not confirm which metrics are in the free files (active addresses, transaction count, MVRV, NVT are what I expect, from memory); the documentation site redirected to another host and I did not follow it |
| Stablecoin supply (DefiLlama) | Yes: the documentation calls the free interface open with no authentication, with historical total and per-coin circulating supply | **Not established.** Nothing on revisions or on how far back history goes | <https://api-docs.defillama.com/llms-free.txt>. Supply is reconstructed from chains, so history is presumably rebuilt when a coin or chain is added (my inference, not stated) |
| Bitcoin chain statistics (Blockchain.com charts: transactions, hash rate, difficulty) | **Not established.** The page I reached lists access by key and pay-per-request and did not describe a free tier | Not established | <https://www.blockchain.com/explorer/api/charts_api>. Counts taken from the chain are in principle reproducible by anyone, apart from the most recent blocks |
| Google Trends | Free in a browser | **No, by construction.** Google's own help page says the figures come from a sample of searches, have random noise added, are normalised to the time range and location of the request, and are scaled 0 to 100 within it. The value for a past week therefore depends on when and over what window it is requested | <https://support.google.com/trends/answer/4365533>. Kristoufek (2015) had to chain three-month downloads to get a daily series |
| Wikipedia page views | Not checked in this run (from memory: a public interface without a key, from mid-2015) | Not checked | The source used in the 2013 and 2015 papers was a third-party site that, from memory, no longer exists |
| Historical tweets and Twitter sentiment | Not checked in this run (from memory: no free historical access) | n/a | The two Twitter papers opened collected their tweets live |
| Exchange flows, exchange reserves, MVRV-type ratios that rely on labelled addresses | Not found free without an account | Unlikely: they depend on address labels that vendors keep extending (from memory, not verified) | No provider page opened |

**The finding to record.** I could not establish for any on-chain or sentiment series that it is both free without an account and unrevised. Three series are free and keyless (the Fear and Greed index, the Coin Metrics community files, DefiLlama stablecoin supply) but none of their providers states that history is fixed, and the Fear and Greed index has demonstrably changed its ingredients. Google Trends fails the test by design. Before any hypothesis is registered on one of the three, the Data steward would have to show that archived copies of the series from different dates agree on the overlapping past; without that, a test on them is a test on today's version of history.

## Unverified leads

Sources I could read only as an abstract or a listing, or not at all. Nothing here should be cited as evidence until someone reads the paper. Where I report an abstract, that is all that is reported; numbers I saw only in a search-engine summary are marked as such.

### Sub-angle 1: Bitcoin-to-altcoin lead-lag (no source opened in full)

- **Guo, L., Sang, B., Tu, J. and Wang, Y. (2024). "Cross-cryptocurrency return predictability." *Journal of Economic Dynamics and Control* 163: 104863. DOI 10.1016/j.jedc.2024.104863.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/dyncon/v163y2024ics0165188924000551.html)): on Binance data, lagged returns of other cryptocurrencies significantly predict a coin's return; robust to adaptive LASSO and principal components; a long-short portfolio built on past returns of coins earns a sizable out-of-sample return after transaction costs; the authors attribute it to common shocks and limited attention slowing the diffusion of information. A search summary of the 2021 working paper gives 2.16 percent a day for that portfolio; I did not see this figure in a source I opened. The publisher's page is paywalled and two repository pages returned nothing. **Hindsight flag: sample dates unknown; the working paper is from December 2021 but the published version may run later. Treat as overlapping dev until checked.** This is the paper to read first for sub-angle 1: it is on our exchange, at (I believe) daily frequency, and with costs. Transfer caveat until read: the headline is a long-short spread, and which leg carries it is unknown.
- **Sifat, I. M., Mohamad, A. and Mohamed Shariff, M. S. B. (2019). "Lead-Lag relationship between Bitcoin and Ethereum: Evidence from hourly and daily data." *Research in International Business and Finance* 50, 306-321. DOI 10.1016/j.ribaf.2019.06.012.** Abstract only ([EconPapers listing](https://econpapers.repec.org/RePEc:eee:riibaf:v:50:y:2019:i:c:p:306-321)): hourly and daily data, August 2017 to September 2018; error-correction, Granger, ARDL and wavelet tests give varied results that mostly point to causality in both directions; the authors conclude that intraday traders can barely exploit the price discovery between the two at hourly or daily frequency. **A published null for exactly our two granularities.** Sample end 2018-09, clean. A full-text copy answered with an access error.
- **Bação, P., Duarte, A. P., Sebastião, H. and Redzepagic, S. (2018). "Information Transmission Between Cryptocurrencies: Does Bitcoin Rule the Cryptocurrency World?" *Scientific Annals of Economics and Business* 65(2), 97-117. DOI 10.2478/saeb-2018-0013.** Abstract of the working-paper version only ([EconPapers listing](https://econpapers.repec.org/RePEc:gmf:papers:2018-06)): Bitcoin, Litecoin, Ripple, Ethereum and Bitcoin Cash; vector autoregression with Geweke feedback measures; most transmission happens within the same period, with little lagged effect, and what lagged feedback there is runs mainly from the other coins to Bitcoin. **A second null, and against the assumed direction.** Frequency and dates not in the abstract (daily, to 2018, from memory). Clean by publication date.
- **Wang, J. and Ngene, G. M. (2020). "Does Bitcoin still own the dominant power? An intraday analysis." *International Review of Financial Analysis* 71: 101551. DOI 10.1016/j.irfa.2020.101551.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/finana/v71y2020ics1057521920301952.html)): intraday data; a nonlinear, asymmetric Granger model finds that Bitcoin's returns help forecast other coins' returns in rising and in falling markets; Bitcoin's shocks reach other coins' volatility faster than the reverse. Coins, sampling interval and dates are not in the abstract. Clean by publication date. The positive counterpart to the two nulls above; read it for the sampling interval.
- **Şoiman, F., Dumas, G. and Jimenez-Garces, S. (2022). "The return of (I)DeFiX." arXiv:2204.00251** (a published version exists under DOI 10.1016/j.intfin.2023.101786). Abstract only ([arXiv](https://arxiv.org/abs/2204.00251)): returns of an index of DeFi tokens are exposed to the crypto market, to their own network variables and to investor attention; the crypto market is the strongest driver; a valuation ratio (value locked over market capitalisation) has no predictive power. A search summary reports a coefficient of 0.87 on the one-week lagged Bitcoin return for the index (Table 3) and an insignificant two-week lag; not confirmed in a source I opened. Sample dates not in the abstract; submitted 2022-04, so clean for the preprint.
- **Not relevant after opening:** Plazuelo Pascual et al. (2025), "Price Discovery in Cryptocurrency Markets", arXiv:2506.08718, is about venues (Binance against Uniswap, spot against futures), not about one coin leading another. **Hindsight flag: its sample is September 2023 to September 2024.**
- **Seen only in search summaries, not opened:** Kurihara and Matsumoto, lagged transmission from Bitcoin to small-cap altcoins at 1-minute intervals (*Asia-Pacific Financial Markets*; dates unknown, **flag**); a 2023 paper in *Investment Management and Financial Innovations* reported as finding causality between coins at one minute but not at hourly or daily frequency (dates unknown, **flag**).

### Sub-angle 2: equities, dollar, rates, gold, volatility, macro news

- **Liu, Y. and Tsyvinski, A. (2018/2021). "Risks and Returns of Cryptocurrency."** (reference in `time-series.md`). Abstract of NBER Working Paper 24877 only, for this question (<https://www.nber.org/papers/w24877>): cryptocurrency returns have little or no exposure to common stock market and macroeconomic factors and none to the returns of currencies and commodities; they are predicted by momentum and by proxies for investor attention. The tables behind the exposure result were not read in this run or the previous one. Sample to 2018-05, clean. **The main published null for "traditional markets predict crypto" before 2020.**
- **Benigno, G. and Rosa, C. (2023). "The Bitcoin-Macro Disconnect." Federal Reserve Bank of New York Staff Report 1052, February 2023.** Abstract only (<https://www.newyorkfed.org/research/staff_reports/sr1052>): an intraday event study finds Bitcoin orthogonal to monetary and macroeconomic news, unlike other US asset classes; the authors call this puzzling. **Hindsight flag: sample dates are not on the page; published February 2023, so probably ends in 2022, but treat as unknown.** It contradicts sections 3 and 4 in spirit: one finds a small response to inflation surprises, this one none.
- **Iyer, T. (2022). "Cryptic Connections: Spillovers between Crypto and Equity Markets." IMF Global Financial Stability Note 2022/01.** Summary page only (<https://www.imf.org/en/Publications/global-financial-stability-notes/Issues/2022/01/10/Cryptic-Connections-511776>); the note itself returned an error. Daily returns and volatility of Bitcoin, Tether, the S&P 500 and the MSCI emerging markets index: spillovers from Bitcoin's volatility to the equity indices rose by about 12 to 16 percentage points after the start of the pandemic and from its returns by about 8 to 10; Bitcoin explains about 14 to 18 percent of the variation in equity volatility and 8 to 10 percent of the variation in equity returns; spillovers in the reverse direction rose too. These are same-period connectedness measures, not forecasts. Published January 2022, so the sample ends by 2021: clean. It documents the rise of the crypto-equity link after 2020 and gives no reason to expect a lead from one day to the next.
- **Corbet, S., Larkin, C., Lucey, B., Meegan, A. and Yarovaya, L. (2020). "Cryptocurrency reaction to FOMC Announcements: Evidence of heterogeneity based on blockchain stack position." *Journal of Financial Stability* 46: 100706. DOI 10.1016/j.jfs.2019.100706.** Abstract only ([repository record](https://doras.dcu.ie/25046/)): about volatility spillovers after rate and quantitative-easing announcements; currency-type and mineable assets react, protocol and application tokens largely do not. Nothing on mean returns in the abstract. Clean by publication date.
- **Akyildirim, E., Corbet, S., Lucey, B., Sensoy, A. and Yarovaya, L. (2020). "The relationship between implied volatility and cryptocurrency returns." *Finance Research Letters* 33. DOI 10.1016/j.frl.2019.06.010.** Search summary only: thirty-minute data; the link between crypto and the VIX and its European counterpart strengthens in periods of market stress. Not opened. VIX is not in the Store.
- **Seen only in search summaries:** a 2021 paper in the *Journal of Risk and Financial Management* (14(7), 330) reported as finding no Granger causality between the S&P 500 and Bitcoin at any frequency in normal conditions and partial two-way causality in the March 2020 crash; a 2019 paper in *Entropy* (21(11), 1116) on information flow between Bitcoin and other assets by transfer entropy. Both pages refused the connection.
- **From memory, not searched for lack of time: day-of-week and weekend effects.** Caporale and Plastun (2019, *Finance Research Letters*) on a Monday effect in Bitcoin; Aharon and Qadan (2019, same journal) likewise; Baur, Cahill, Godfrey and Liu (2019, same journal) finding no stable time-of-day or day-of-week effect. None confirmed in this run. All have samples ending before 2020.

### Sub-angle 3: market-wide state variables from crypto prices

- **"Herding in different states and terms: evidence from the cryptocurrency market." *Journal of Asset Management* (2022). DOI 10.1057/s41260-022-00265-1.** Search summary only; the publisher redirected to a login page and I have not confirmed the authors. Reported: after a day with a positive market return, days of high cross-sectional dispersion have a higher market return than days of low dispersion, significantly; after a negative day the difference is negative. This is the only lead I found in which a dispersion measure is related to returns conditional on a lagged market state, and from the summary I cannot tell whether dispersion and return are measured on the same day. Sample dates unknown; published 2022.
- Other herding papers surfaced in search (not opened: a bot check or a refusal): Haykir and Yagli (2022, *Financial Innovation*, "Speculative bubbles and herding in cryptocurrencies"), reported as finding that herding diminishes in bubbles; several studies on dispersion measures with mixed results on whether herding exists at all.

### Sub-angle 4: on-chain and sentiment

- **Griffin, J. M. and Shams, A. (2020). "Is Bitcoin Really Untethered?" *Journal of Finance* 75(4), 1913-1964. DOI 10.1111/jofi.12903.** Abstract only ([EconPapers listing](https://econpapers.repec.org/RePEc:bla:jfinan:v:75:y:2020:i:4:p:1913-1964)): in the 2017 boom, purchases of Bitcoin with Tether are timed after market falls and are followed by sizable rises in the Bitcoin price; the flow comes from one entity, clusters below round prices and induces asymmetric autocorrelation in Bitcoin returns. Sample 2017 to early 2018 (from memory), clean. It rests on flows traced on the blockchain to one exchange, hourly: not a series we have.
- **Ante, L., Fiedler, I. and Strehle, E. (2021). "The influence of stablecoin issuances on cryptocurrency markets." *Finance Research Letters*.** Search summary only (the working paper came back unreadable): 565 issuances of at least 1 million dollars, seven stablecoins, April 2019 to March 2020; a falling market in the week before an issuance, positive abnormal returns in the 24 hours around it; issuance size does not matter. Clean.
- **Kristoufek, L. (2021). "Tethered, or Untethered? On the interplay between stablecoins and major cryptoassets." *Finance Research Letters* 43: 101991. DOI 10.1016/j.frl.2021.101991**, and its follow-up in *Financial Innovation* 8: 37 (2022). Search summary only (certificate error on one copy, login redirect on the other): no sign that stablecoin issuance pushes other coins' prices up; issuance follows price rises. **A null for "stablecoin supply growth predicts returns"**, against Griffin and Shams. Clean by publication dates.
- **Hoang, L. T. and Baur, D. G. "Effects of Bitcoin Exchange Reserves on Bitcoin Returns and Volatility." SSRN 3902504** (I searched for it under a journal title I remembered, "Loaded for bear", and could not confirm that title). Search summary only: daily data from 20 exchanges; changes in exchange reserves are negatively related to current and future Bitcoin returns; extreme negative returns are followed by rising reserves the next day. Dates unknown (the working paper is from 2021). The series comes from a commercial provider.
- **Fear and Greed index as a predictor.** Cavalheiro, Vieira and Thue (2024), *Review of Behavioral Finance* 16(5), 819-835: abstract seen in a search summary only, reporting that the index Granger-causes Bitcoin and Ethereum returns, with feedback from returns to the index. Huang et al. (2024), *Corporate Ownership and Control* 21(2), 121-131: monthly data, a positive short-run effect of index changes on returns. **Hindsight flag for both: sample dates unknown and both were published in 2024; treat as overlapping dev.** Note that a quarter to a half of the index is itself computed from Bitcoin's price, volume and volatility.
- **Liu and Tsyvinski, investor attention.** Abstract-level here (see sub-angle 2). From memory, not confirmed: Google searches for "Bitcoin" and Twitter post counts predict weekly returns one to two weeks ahead with a positive sign, and the relative volume of searches for "Bitcoin hack" predicts negatively.
- **Not found at all:** a peer-reviewed out-of-sample test of active addresses, MVRV or NVT as return predictors. One targeted search returned vendor material and a master's thesis only.

## Where I found nothing

- **No published test of "the previous US session predicts the next crypto day"** (S&P 500, Nasdaq, sector ETFs, Treasuries, gold or the dollar on session D against crypto on D+1) in any source I could open or see summarised. The closest are contemporaneous: connectedness measures (Iyer) and announcement-window reactions (sections 3 and 4). A hypothesis of this form would be `exploration`, or `literature` with a predicted null resting on Liu and Tsyvinski's exposure result once that is read.
- **No published test of market breadth, average pairwise correlation or Bitcoin's share of volume as a predictor** of market or altcoin returns. Sub-angle 3 has descriptive herding studies only.
- **No source opened in full for sub-angle 1.** The five leads split three ways: one positive across coins on Binance (Guo et al.), one positive intraday and nonlinear (Wang and Ngene), two nulls at exactly hourly and daily horizons (Sifat et al.; Bação et al.).
- **Nothing on beta catch-up or on contagion in crashes** as a tradable lag: not searched specifically for lack of time.
- **Nothing on weekend effects driven by closed traditional markets**: not searched; memory-only leads are listed above.
- **No free series shown to be point-in-time** for any on-chain or sentiment variable (see the table).

## What transfers to our setup

Setup: spot only, long or flat, the point-in-time universe (40 USDT pairs on Binance, monthly reconstitution), daily and hourly crypto bars in UTC, daily ETF bars, signal at a bar's close and trade at the next open, 12 to 25 bps per side.

- **Timing against the ETF bars.** An ETF bar dated D is final at about 21:00 UTC (20:00 in summer). A daily crypto design must use it for the crypto bar D+1, which opens three to four hours later; an hourly design can act at the first hourly open after the US close. On Saturdays, Sundays and US holidays there is no new ETF bar, so a daily signal is stale by up to three days: any hypothesis has to say what it does then.
- **What the Store lacks for sub-angle 2.** No VIX or other implied-volatility series (the index is not an ETF; an ETF on VIX futures would be a proxy, with a history from about 2011, from memory). No dollar series (an ETF on the dollar index, UUP, would be the proxy to add). No short-rate or yield series beyond what TLT and IEF returns imply. No calendar of FOMC, CPI or payroll dates, and no survey forecasts or futures to compute surprises. The calendar files are small, public and known in advance; the surprise data is not free.
- **Published reactions to macro news are faster than our bars.** Section 3's effect lives in a 30-minute window that sits inside one hourly bar. Only slower forms (the rest of the day after an announcement, or a pre-announcement drift nobody has published for crypto) are tradable at the next open.
- **Sizes against costs.** The only cost-aware result opened (section 1) breaks even at about 25 bps per trade, the top of our range, on a long-short rule in a falling year. Section 3's effect is 24 bps per standard deviation of surprise, one round trip at our cheapest. Expect predictive claims pooled across coins to be the testable form, not trading claims.
- **Long or flat.** Where direction is reported, the usable half is mixed: Garcia and Schweitzer's profit in 2014 was on the short side; the conditional attention effect of section 2a is symmetric; the lead-lag papers do not say (abstracts only).
- **Universe.** Sections 1 to 6 are evidence on Bitcoin alone (plus Ethereum in section 4). Nothing opened tests a cross-market or sentiment signal across a liquidity-ranked universe of some 40 coins.
- **Frequency.** For lead-lag between coins the two published nulls are at hourly and daily horizons, and one search summary puts the effect at the one-minute scale. If the Researcher registers "Bitcoin's return in hour t predicts the universe's return in hour t+1", the literature's prior is small or zero at that horizon, and that should be the stated expectation.

## Suggested registrations, with their support

For the Researcher: what each could be, and how well the notes back it. None of this was tested.

| Hypothesis | Granularity | Support | Origin it can honestly claim |
| --- | --- | --- | --- |
| Change in aggregate quote volume today predicts tomorrow's return, positive | daily | Section 1 (opened; Bitcoin, to 2014) | literature |
| Bitcoin's return in one bar predicts other coins' returns in the next | hourly and daily | Leads only: Guo et al. and Wang and Ngene for, Sifat et al. and Bação et al. against | literature only after Guo et al. is read; until then the abstracts support a two-sided prior |
| A coin's return is predicted by the lagged return of the rest of the universe | daily | Guo et al., abstract only, sample dates unknown (flagged) | as above |
| Mean return on FOMC days (or the hours after the statement) differs from other days | daily and hourly | Section 4 (opened; means reported, not tested); needs a date file | literature, with a weak prior |
| No abnormal return around CPI releases | hourly | Section 3 (opened; a null on a 30-minute window); needs a date file | literature, predicted null |
| The previous US session's return (SPY, QQQ, GLD, TLT) predicts the next crypto day | daily | None found; section 5 and the Liu and Tsyvinski abstract point to a null before 2020 | exploration, or literature with a predicted null |
| Low cross-sectional dispersion of hourly returns predicts the market's next return | hourly | Section 8 measures it but tests nothing; one unopened lead | exploration |
| Fear and Greed extremes, stablecoin supply growth, active addresses | daily | Leads only; no series shown to be point-in-time | not registrable until the Data steward clears a series |
