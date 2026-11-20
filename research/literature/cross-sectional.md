# Cross-sectional: literature notes

Collected by the Literature scout on 2026-11-19. Question of this run: what does published work say ranks cryptocurrencies against each other by future return, using only price and volume? The notes survey the family so that about eight hypotheses can be registered across sub-angles (momentum, short-term reversal, volatility and lottery effects, size and liquidity, other price-and-volume characteristics) and across daily and hourly bars.

How to read an entry:

- Numbers are the paper's own, in its units, with the table or section they come from. Arithmetic of mine is marked "(my arithmetic)".
- "Opened" says which version I read and how much of it. Several papers were read as text extracted from the PDF, where table layouts are sometimes scrambled; where I could not read a table reliably I say so and give no number.
- "Sample end" is checked against the split: a sample ending by 2022-12-31 is clean evidence for the train segment; anything later is flagged. **Every source in the numbered sections ends by 2022-12-31.** The only flagged source is under "Unverified leads".
- "Transfer" judges the result against our setup: spot only, long or flat, the point-in-time universe (40 USDT pairs on Binance by 30-day quote volume, monthly reconstitution), daily and hourly bars, signal at a bar's close and trade at the next open, 12 to 25 bps per side.

Three facts about this literature that apply to every section:

1. **Almost all of it sorts 1,000 to 3,000 coins with a market capitalisation above 1 million dollars.** Our 40 coins all sit in the top size and volume group of those sorts. A spread between the extreme quintiles of the whole market says little about ranking within its top group. The sources that restrict themselves to large or liquid coins (Sections 1b, 1c, 2, 4 and 8) carry the most weight for us.
2. **The sign of the past-return effect depends on liquidity.** Illiquid coins reverse, liquid coins continue (Sections 1b, 1c, 3). A study that weights coins equally over the whole market therefore finds reversal, and one that weights by value finds momentum. For a top-40 universe the published prior is continuation at one to four weeks, and at most a weak reversal at one day.
3. **We have no market capitalisation.** A characteristic defined on dollar volume, price or returns can be computed from our bars; one that needs market capitalisation (size itself, volume scaled by capitalisation, value weighting) cannot. Section 5 and 6 say what can be proxied.

Sections are ordered by how strong the evidence is for our universe.

## 1. Cross-sectional momentum at one to four weeks, in large and liquid coins

**Claim.** Coins with the highest return over the past one to four weeks earn more over the next week than coins with the lowest, and the effect is found among large, liquid coins rather than small ones.

### 1a. Liu, Tsyvinski and Wu: the reference result

- **Reference.** Liu, Y., Tsyvinski, A. and Wu, X. (2022). "Common Risk Factors in Cryptocurrency." *Journal of Finance* 77(2), 1133-1177. DOI [10.1111/jofi.13119](https://doi.org/10.1111/jofi.13119).
- **Opened.** NBER Working Paper 25882 (May 2019), <https://www.nber.org/papers/w25882>, as text extracted from the PDF. The published version was not opened and may use a longer sample.
- **Sample and method.** Already filed in [time-series.md](time-series.md), Section 2b: 1,707 coins above 1 million dollars, CoinMarketCap, 2014 to 2018, weekly returns, value-weighted quintiles re-formed every week, no costs (the paper says its strategies ignore trading costs and the feasibility of shorting, Section 3.1).
- **Size (Table 4), value-weighted, excess return per week.** Quintile 5 minus quintile 1: 2.7 percent for the 1-week lookback (t = 1.994), 3.3 for 2 weeks (t = 2.442), 4.1 for 3 weeks (t = 2.742), 2.5 for 4 weeks (t = 2.002). Lookbacks of 8, 16, 50 and 100 weeks: 0.6, 0.4, -0.8 and -1.1 percent, none significant (Table 7).
- **Which leg.** For the 3-week sort the top quintile earns 4.3 percent a week (t = 2.956) and the bottom 0.2 (t = 0.156) (Table 4): the profit is in the winners.
- **Which coins (Table A.2, double sort on size then momentum).** Above-median size: bottom momentum quintile -0.2 percent a week, top 4.0, spread 4.2 (t = 2.57). Below-median size: 3.2 against 3.9, spread 0.6 (t = 0.30). Momentum is a large-coin effect.
- **Caveats.** See time-series.md Section 2b for the equal-weighted regression (not significant) and the variant that shorts Bitcoin. I could not read Tables 12 and 13 reliably from the extracted text and add no numbers from them.
- **Sample end.** 2018-12-31. Clean.

### 1b. Begušić and Kostanjčar: momentum only in the liquid third, with costs, long only

- **Reference.** Begušić, S. and Kostanjčar, Z. (2019). "Momentum and liquidity in cryptocurrencies." arXiv:1904.00890. <https://arxiv.org/abs/1904.00890>. Working paper, not peer reviewed as far as the page shows.
- **Opened.** The full paper in the HTML rendering at <https://ar5iv.arxiv.org/html/1904.00890>.
- **Sample.** 711 coins that at some point had existed for 26 weeks with a market capitalisation of at least 1 million dollars; stablecoins removed; CoinMarketCap daily data; January 2015 to January 2019.
- **Method.** Momentum is the cumulative return over the prior 14 days; illiquidity is the Amihud ratio over the same 14 days. A 3 by 3 sort (30/40/30 percent) on both, equal-weighted, re-formed every 14 days. One horizon only.
- **Size (Table 1, mean daily return).** Winners minus losers: +0.26 percent a day in the liquid third (significant at 5 percent), -0.06 in the middle, -0.33 in the illiquid third. Illiquid losers earn 1.07 percent a day against 0.53 for illiquid winners: reversal there.
- **Long only, with costs (Table 2).** Liquid winners, held long: 0.71 percent a day gross (standard deviation 7.43 percent, information ratio 1.59 against the capitalisation-weighted market), 0.70, 0.65 and 0.60 percent a day at costs of 10, 50 and 100 bps. Illiquid losers do better on paper (1.07 percent a day gross) but the authors warn that spreads would eat into it.
- **Sample end.** January 2019. Clean.

### 1c. Fičura: weekly momentum in large, liquid coins and reversal in the rest, 2017 to 2022

- **Reference.** Fičura, M. (2023). "Impact of size and volume on cryptocurrency momentum and reversal." FFA Working Paper 3/2023, Prague University of Economics and Business. <https://wp.ffu.vse.cz/artkey/wps-202301-0003_impact-of-size-and-volume-on-cryptocurrency-momentum-and-reversal.php>. Working paper.
- **Opened.** Abstract and introduction only (text extracted from the PDF). The results tables were not read, so only t-statistics from the abstract are given.
- **Sample.** CoinMarketCap, weekly, June 2017 to December 2022. Each week coins are split into "large and liquid" (market capitalisation above 50 million dollars and last-week volume above 5 million dollars) and "small and illiquid".
- **Finding.** The past week's return predicts the next week's negatively for small, illiquid coins (t = -7.31) and positively for large, liquid coins (t = 2.33). Long-horizon returns show reversal, not significant for large, liquid coins (t = -1.91 at 26 weeks). The author attributes the reversal mostly to low volume and the momentum mostly to high capitalisation.
- **Costs.** Not seen in the parts read.
- **Sample end.** 2022-12. Clean, and the only momentum source here that covers the whole of 2019 to 2022.

### Failures and decay

- **Momentum premium not significant over 2014 to 2020.** Dobrynskaya, V. and Dubrovskiy, M. (2022), "Cryptocurrencies meet equities: risk factors and asset pricing relationships", HSE Working Paper WP BRP 86/FE/2022, <https://wp.hse.ru/data/2022/02/24/1749596434/86FE2022.pdf> (opened: text extracted from the PDF, Sections 1 to 4). 1,986 coins above 1 million dollars, CoinMarketCap, weekly, 2014-01-06 to 2020-11-01. Their momentum factor (top 30 percent by previous-week return minus bottom 30 percent, capitalisation-weighted) averages 46 percent a year with t = 0.95, a weekly minimum of -121 percent and negative skewness (Table 3). They say the average was significant in 2014 to 2018 and that the damage came from a few weeks in 2019 and 2020 when past losers had extreme returns: a momentum crash through the short leg. A long-only test is not exposed to that crash, but it also means the published long-short spread overstates what remained after 2018.
- **Equal-weighted tests do not find it** (time-series.md Section 2b; and Section 1b above: -0.06 and -0.33 percent a day outside the liquid third).
- **A published null** (Grobys and Sapkota 2019: 143 coins, 2014 to 2018, no significant momentum) is still an unverified lead; see time-series.md.

### Transfer

Testable here as a predictive claim on daily bars: the rank of the past 7-, 14-, 21- or 28-day return against the next 7 days' return, as a rank information coefficient across the point-in-time universe. Also testable as a trading claim: hold the top third or top fifth by past return, re-formed weekly, against the equal-weight point-in-time universe. The published profit is in the long leg and in large, liquid coins, so neither the no-shorting rule nor the universe is a handicap. What does not transfer: value weighting (we would weight equally or by quote volume), and the size of the spread, which comes from sorts over the whole market. The lookback is a choice from 1 to 4 weeks; 3 weeks is the published peak (1a), 2 weeks the only horizon in 1b, 1 week the one in 1c. Costs: a weekly re-formed quintile turns over roughly two thirds of its holdings a week in the one source that reports turnover (Section 2), so about 16 to 33 bps a week at our costs (my arithmetic) against published gross spreads of percent a week.

## 2. A combined trend signal from price and volume indicators

**Claim.** A single score built from many technical indicators of price and volume, over several horizons, predicts next week's return across coins better than past return alone, including among the 100 largest coins and after costs.

- **Reference.** Fieberg, C., Liedtke, G., Poddig, T., Walker, T. and Zaremba, A. (2025). "A Trend Factor for the Cross Section of Cryptocurrency Returns." *Journal of Financial and Quantitative Analysis* 60(7), 3116-3153. DOI [10.1017/S0022109024000747](https://doi.org/10.1017/S0022109024000747). Open access.
- **Opened.** The published article as text extracted from the PDF (Tables 1, 3, 8 and 9 and the surrounding text). The supplement was not opened.
- **Sample.** 3,245 coins above 1 million dollars, CoinMarketCap, April 2015 to May 2022, 423 weekly observations; returns truncated at the 0.5 and 99.5 percentiles (Section on data, Table 1).
- **Method.** Indicators such as moving averages of price and of volume, RSI, stochastic oscillators, CCI, Bollinger bands and MACD are combined into one expected-return score by a cross-sectional machine-learning regression; coins are sorted into value-weighted quintiles on the score and held one week. I did not transcribe the construction: a Researcher who wants the signal itself must read the paper's section on the trend characteristic.
- **Size (Table 3), percent per week.** Lowest quintile 0.12 (t = 0.16), then 0.93, 1.12, 2.72 (t = 3.59), highest 3.98 (t = 4.80); high minus low 3.87 (t = 5.19), annualised Sharpe ratio 1.94. The profit is in the long leg; the lowest quintile earns about zero rather than losing.
- **Large coins (Table 9 Panel B, largest 100 each week).** High minus low 3.40 percent a week gross (t = 4.48); top quintile 3.78 (t = 4.41), bottom 0.38. Among the largest 10 percent the spread is 2.51 percent a week (Table 8). The authors say the effect comes mainly from big and liquid coins.
- **Costs (Table 9).** Turnover about 68 percent of the portfolio a week. With 30 bps on the long and 40 bps on the short leg the spread is 2.90 percent a week (t = 3.89) for all coins and 2.45 (t = 3.22) for the largest 100; the top quintile alone, long only, nets 3.61 (all) and 3.38 (largest 100). Break-even cost 1.41 percent (all) and 1.25 percent (largest 100).
- **Replication of 1a inside this paper.** The authors re-form the Liu, Tsyvinski and Wu sorts (size, price, maximum price, 1- to 4-week momentum, dollar volume, scaled volume, volume volatility) on April 2015 to May 2022 and state that all of them still produce significant spreads; the numbers are in their supplement (Table B.8), which I did not open.
- **Sample end.** May 2022. Clean, although the paper was published in 2025.
- **Transfer.** Testable only in part. The machine-learning score needs market capitalisation for its weighted fit and a re-reading of the paper. What a Researcher can register without it: (a) a predictive claim that an equal-weight composite of a few named trend indicators (say price over its 1- to 4-week moving average, and volume over its moving average) ranks next week's returns in the point-in-time universe; (b) the long-only top group against the equal-weight universe. The largest-100 result is the closest published analogue to our universe, and the long-only, after-cost figure exists.

## 3. Daily cross-sectional reversal

**Claim.** Coins with the lowest return on one day earn more the next day than coins with the highest.

### 3a. Bianchi, Babiak and Dickerson: large gross reversal, gone on Binance after costs

- **Reference.** Bianchi, D., Babiak, M. and Dickerson, A. (2022). "Trading volume and liquidity provision in cryptocurrency markets." *Journal of Banking & Finance* 142, 106547. DOI [10.1016/j.jbankfin.2022.106547](https://doi.org/10.1016/j.jbankfin.2022.106547).
- **Opened.** Sveriges Riksbank Working Paper 413 (May 2022), <https://www.riksbank.se/globalassets/media/rapporter/working-papers/2022/no.-413-trading-volume-and-liquidity-provision-in-cryptocurreny-markets.pdf>, as text extracted from the PDF. The published version was not opened.
- **Sample.** Daily (00:00 UTC) prices and volume of USD pairs aggregated over more than 80 centralised exchanges by CryptoCompare, market capitalisation from CoinGecko, 2017-03-01 to 2022-03-01; each month the 100 most liquid pairs by the previous month's Amihud ratio, each with at least 365 days of history; 179,023 pair-days (Section 2.1).
- **Method.** Each day pairs are sorted into deciles on that day's return; the strategy is long the lowest decile and short the highest for the next day, equal- or value-weighted (Section 2.2).
- **Size (Table 2 Panel A).** Equal-weighted: 2.2 percent a day gross (p = 0.000), daily Sharpe ratio 0.37. Value-weighted: 0.6 percent a day (p = 0.001), daily Sharpe ratio 0.06. The authors read the gap as the reversal sitting in smaller pairs.
- **Costs (Table 5).** 30 bps on the long side and 40 bps on the short. Equal-weighted reversal stays at 1.68 percent a day (p = 0.001); no value-weighted strategy keeps a significant positive return.
- **On Binance alone (Table 7; USDT pairs, 2018-10-01 to 2022-03-01).** The low-volume version of the strategy (Section 4 below), equal-weighted: 0.187 percent a day gross, -0.213 percent net; value-weighted: 0.059 gross (not significant), -0.341 net. On the other four exchanges it is 0.7 to 2.5 percent a day gross. The paper says the returns are significantly smaller on Binance.
- **Sample end.** 2022-03-01. Clean.

### 3b. Kakushadze: the previous day's return as a regression factor

- **Reference.** Kakushadze, Z. (2018). "Cryptoasset Factor Models." arXiv:1811.07860. <https://arxiv.org/abs/1811.07860>. Working paper.
- **Opened.** The full paper in the HTML rendering at <https://ar5iv.labs.arxiv.org/html/1811.07860>.
- **Sample.** CoinMarketCap daily open, high, low, close, dollar volume and capitalisation up to 2018-08-18; 362 coins with a complete year of data, 127 to 129 with two years, 64 to 66 with three.
- **Method.** Daily cross-sectional regressions of open-to-close log returns on the previous day's open-to-close return ("momentum"), log capitalisation, an intraday high-low volatility measure and volume; t-statistics annualised by the square root of 365.
- **Size.** The previous day's return has a negative coefficient in every sample: t about -34.2 (362 coins, Table 1), -16.9 (127 coins, two years, Table 2). The return of two days before is also negative. Size is negative (t about -3.7, Table 1) and the intraday volatility measure negative (t about -2.5); volume averaged over several days predicts nothing.
- **Limits.** No costs and no portfolio returns; the samples are chosen by data availability, not by size, so the paper does not say whether the reversal holds in large coins. The author makes the strategy conditional on cheap shorting of a wide cross-section.
- **Sample end.** 2018-08-18. Clean.

### Transfer

Testable here as a predictive claim on daily bars: the rank of a coin's return on day t against its return from the open of t+1's bar onward. Two cautions set the prior low. First, the published effect is concentrated in small, illiquid pairs and vanishes or turns into momentum in the largest coins (Section 1c; the abstract of Zaremba et al. 2021 under "Unverified leads" says the same for daily data). Second, the one result on Binance alone is about a tenth of the aggregate result gross, and negative after 30 to 40 bps. As a trading claim (hold yesterday's losers) it turns the whole position over every day: 24 to 50 bps a day at our costs (my arithmetic) against a published gross of 6 to 19 bps a day on Binance for a long-short pair of legs. Register it as predictive, expecting a small or zero rank coefficient; a trading claim is not supported.

On part of the reversal being bid-ask bounce: these papers use closing prices and returns from close to close, so the first return after the signal starts at the same price that produced the signal. Our rule of trading at the next open removes nothing on daily bars (the next open is the same instant), so a test here cannot separate bounce from a true reversal. None of the sources opened quantifies bounce; 3a lists spread proxies as conditioning variables only.

## 4. Reversal is stronger after abnormally low volume; a volume shock alone predicts little

**Claim.** The daily reversal of Section 3 is larger for coins whose volume that day was low relative to their own recent average; a low-minus-high sort on the volume shock alone is not a robust predictor.

- **Reference and sample.** Bianchi, Babiak and Dickerson (2022), as in 3a.
- **Volume shock.** Log of the day's volume minus the log of its mean over the previous m = 30 days, divided by the standard deviation of log volume over the same window (Section 2.2, Eq. 1); m = 60 gives similar results in their appendix.
- **Method.** A 3 by 3 double sort each day, first on the day's return, then on the volume shock; the conditional reversal is losers minus winners within the low-volume or the high-volume third.
- **Size (Table 3).** Equal-weighted: 1.22 percent a day within low volume (p = 0.002) against 0.54 within high volume (p = 0.003). Value-weighted: 0.6 percent a day within low volume (p = 0.001) against -0.18 within high volume (p = 0.543). (The introduction quotes 1.26 and 0.65 for the same figures.)
- **Volume shock alone (Table 2 Panel B, Table 5).** No monotonic pattern across deciles; only the highest-shock decile has a significant negative next-day return. The low-minus-high spread is significant only equal-weighted and is zero after costs; value-weighted it is insignificant gross and significantly negative net. The authors count this as evidence against a high-volume return premium in crypto.
- **Costs and Binance.** As in 3a: value-weighted versions do not survive 30 to 40 bps; on Binance the low-volume reversal is 0.187 percent a day gross and negative net.
- **Sample end.** 2022-03-01. Clean.
- **Transfer.** Testable here as a predictive claim, and fully computable from our bars: quote volume gives the shock exactly as defined. The registrable statement is an interaction: the rank coefficient between today's return and tomorrow's is more negative among coins in the lowest third of volume shock than in the highest third. The stand-alone claim "a high volume shock predicts a lower next-day return" is supported only for the top decile and only weakly. As a trading claim it has the same cost problem as Section 3.

## 5. Size and price level: small and low-priced coins earn more

**Claim.** Coins with a lower market capitalisation, a lower price or a lower weekly maximum price earn more the next week.

- **Reference and sample.** Liu, Tsyvinski and Wu, as in 1a.
- **Size (Table 3), value-weighted, per week.** Quintile 5 minus 1 on market capitalisation: -3.4 percent (t = -2.557), with the smallest quintile at 4.7 percent a week (t = 2.958) and the other four between 1.3 and 1.8. On the last-day price: -3.9 percent (t = -2.420), lowest quintile 5.1 percent. On the week's maximum price: -4.1 percent (t = -2.483), lowest quintile 5.3 percent. Coin age: -0.5 percent, not significant (Table 7).
- **Shape.** The whole effect is the bottom quintile; quintiles 2 to 5 are flat. The paper's two-factor model shows the price and maximum-price spreads are the size effect under another name (Section 4).
- **Later confirmation.** Dobrynskaya and Dubrovskiy (Section 1, failures): the size factor (smallest 30 percent minus largest 30 percent) averages 61 percent a year with t = 2.26 over 2014 to 2020, with positive skewness from occasional very high returns of small coins (Table 3). Kakushadze (3b): log capitalisation negative, t about -3.7 in the 362-coin sample, weak or positive in the smaller samples. Fieberg et al. (Section 2) report the size spread still unexplained by their model through May 2022.
- **Costs.** Not considered in any of these.
- **Sample end.** 2018-12-31 (Liu, Tsyvinski and Wu); 2020-11-01 (Dobrynskaya and Dubrovskiy). Clean.
- **Transfer.** Not testable as published. The premium belongs to the smallest fifth of some 1,700 coins, which are far outside a top-40 universe; within the top four quintiles there is no gradient. We also have no market capitalisation. Testable only in part, as a weak analogue: rank the point-in-time universe by 30-day quote volume (a proxy for size, since the paper notes small coins also trade less) or by raw price, and ask whether the lower ranks earn more. The published tables give no reason to expect an effect there, so a registration should predict a small size and treat a null as the expected outcome. For price level, note that a redenomination changes a coin's price rank without changing anything else.

## 6. Dollar volume and its volatility: low-volume coins earn more; turnover and Amihud illiquidity do not predict

**Claim.** Coins with lower dollar volume, and with a lower standard deviation of dollar volume, earn more the next week. Volume in coins, volume scaled by capitalisation and the Amihud ratio do not predict returns.

- **Reference and sample.** Liu, Tsyvinski and Wu, as in 1a.
- **Significant (Tables 5 and 6), value-weighted, per week.** Dollar volume (log of the formation week's average daily volume times price): quintile 5 minus 1 = -3.2 percent (t = -2.016); lowest quintile 4.5 percent, highest 1.3. Standard deviation of dollar volume in the formation week: -3.0 percent (t = -2.269); lowest quintile 4.3, highest 1.3, monotonic. The paper notes that volume volatility is mostly a matter of price level and size, and its size factor absorbs both spreads (footnote 5, Section 4).
- **Not significant (Table 7).** Volume in coins: -0.2 percent (t = -0.170). Volume scaled by market capitalisation (turnover): -1.6 percent (t = -1.332). Amihud illiquidity (average absolute daily return over dollar volume in the formation week): +2.6 percent (t = 1.478).
- **Amihud, another source.** Begušić and Kostanjčar (1b), Table 1: illiquid minus liquid is +0.52 percent a day among past losers (significant), +0.16 in the middle group and -0.07 among winners. An illiquidity premium only where there is also a reversal.
- **Volume shock.** See Section 4: no robust stand-alone effect.
- **Costs.** Not considered by Liu, Tsyvinski and Wu.
- **Sample end.** 2018-12-31; January 2019. Clean.
- **Transfer.** Dollar volume is our quote volume, so the characteristic is exactly computable (from one exchange instead of an aggregate); so are its standard deviation and the Amihud ratio. Turnover is not computable without market capitalisation. But the same objection as in Section 5 applies: the premium is in the lowest-volume fifth of the market, and our universe is selected for being the highest-volume coins. Testable only in part, as a within-universe rank test (predictive claim, daily bars, weekly horizon) with a low prior. The Amihud null is worth registering only if a family needs a documented negative; the published sign is positive and insignificant.

## 7. Distance from the recent high

**Claim.** Among large, liquid coins, a close near the high of the past week predicts a higher return next week; among small, illiquid coins it predicts a lower one.

- **Reference and sample.** Fičura (2023), as in 1c: CoinMarketCap, weekly, June 2017 to December 2022; large and liquid means capitalisation above 50 million dollars and weekly volume above 5 million dollars.
- **Signal.** "High-momentum" after George and Hwang (2004): the distance of the previous week's closing price from the highest price of the past k weeks. The abstract says it predicts better than plain past return.
- **Size.** For the 1-week high: t = 4.93 (positive) among large, liquid coins and t = -9.03 (negative) among small, illiquid coins. Coefficients, portfolio returns and the results for longer k are in tables I did not read.
- **Costs.** Not seen.
- **Sample end.** 2022-12. Clean. Working paper, one author, not peer reviewed: treat as a single, unreplicated source.
- **Transfer.** Testable here as a predictive claim on daily bars: close divided by the highest high of the past 7 days, ranked across the point-in-time universe, against the next 7 days' return. Our universe is the "large and liquid" side, where the published sign is positive. It is correlated with 1-week momentum by construction, so a registration should say whether it claims something beyond Section 1. No source opened tests a long window (a 52-week-high analogue) on crypto.

## 8. Low volatility in large coins

**Claim.** Among large coins, a long-only portfolio of the least volatile coins earns a positive return and the most volatile coins do not.

### 8a. Kaya and Mostowfi: the only test on large coins, long only, with costs

- **Reference.** Kaya, O. and Mostowfi, M. (2022). "Low-volatility strategies for highly liquid cryptocurrencies." *Finance Research Letters* 46, 102422. Open copy: <https://digitalcollection.zhaw.ch/bitstream/11475/23853/3/2022_Kaya-Mostowfi_Low-volatility-strategies-cryptocurrencies_frl.pdf>.
- **Opened.** The published article as text extracted from the PDF.
- **Sample.** 35 coins from CoinMarketCap, daily, 2017-01-01 to 2021-06-30. The paper says they were chosen for a market capitalisation of at least 1 billion dollars on 2017-01-01 and for trading since at least 2016-01-01 (Section 2); selecting on a fixed start date avoids choosing survivors, but the threshold as printed is hard to square with 35 coins, so read the selection rule in the paper before relying on it.
- **Method.** Rank coins by historical volatility over a lookback J of 1, 3, 6 or 12 months; hold the 3, 5, 7 or 9 least volatile coins, equal-weighted, for K = 1, 3, 6 or 12 months; a short portfolio holds the same number of the most volatile. A trading cost of 0.175 percent and a bid-ask spread of 0.5 percent are charged at each rebalancing (Section 2).
- **Size (Table 1, average monthly return).** Long low-volatility portfolios earn about 4.4 to 9.7 percent a month across the grid; the best is the 12-month lookback held 12 months with 3 coins, 9.7 percent a month (t = 1.93). The high-volatility portfolios earn -2 to -7 percent a month, never significant. Long-short spreads are mostly 1 to 6 percent a month, and reach 8.8 percent (t = 2.37) for 3 coins at 12 and 12 months. The paper finds lookbacks of 6 and 12 months the most consistent and more frequent rebalancing no better.
- **Weakness.** The t-statistics are low throughout (the paper marks a t of about 1.3 with one star), there are 54 months of data, and a grid of 64 lookback, holding and portfolio-size combinations is reported without a correction. No comparison with an equal-weight portfolio of all 35 coins is given in the parts I read, so "low volatility beats the average coin" is not shown; "low beats high" is shown weakly.
- **Sample end.** 2021-06-30. Clean.

### 8b. Liu, Tsyvinski and Wu: no volatility effect in the whole market

- Value-weighted quintiles, per week, quintile 5 minus 1 (Table 7): standard deviation of daily returns in the formation week -1.7 percent (t = -1.237), with the most volatile quintile at -0.4 percent a week and the others between 1.3 and 2.6; idiosyncratic volatility over the previous 365 days +0.9 percent (t = 0.682). Neither is significant. Sample end 2018-12-31.
- Kakushadze (3b) finds a negative coefficient on an intraday high-low volatility measure (t about -2.5, Table 1) in daily regressions to August 2018.

### Transfer

Testable here, and long only by construction: each month hold the least volatile third or fifth of the point-in-time universe (volatility from daily returns over 6 or 12 months, as published, or over the formation week as in 8b) against the equal-weight universe. Monthly rebalancing makes costs negligible. As a predictive claim: the rank of past volatility against next-month return, predicted negative. The evidence is one small study with weak statistics plus a wrong-signed but insignificant spread in the broad market, so the prior is modest. Abstracts I could not get behind (see leads) report a positive relation between idiosyncratic volatility and returns in the broad market, the opposite sign; that conflict is itself a reason to register the test with its direction stated.

## 9. Maximum daily return (lottery effect)

**Claim.** Coins with a high maximum daily return over the past week earn less the next week (as in stocks), or more (a "MAX momentum" specific to crypto). The literature disagrees on the sign.

- **Opened: a null.** Liu, Tsyvinski and Wu (1a), Table 7: sorting on the maximum daily return of the formation week, value-weighted, quintile 5 minus 1 = -0.6 percent a week (t = -0.441); quintile returns 1.2, 1.8, 1.3, 3.0, 0.6 percent, no pattern. Sample end 2018-12-31.
- **Abstract only: negative.** Grobys and Junttila (2021) report that the lowest-MAX quintile beats the highest by more than 1.50 percent a week, using the previous week's daily returns and a one-week horizon (see leads).
- **Abstract only: positive.** Li, Urquhart, Wang and Zhang (2021) report that coins with a higher maximum daily return earn more afterwards, stronger in rising markets (see leads).
- **Abstract only: mixed.** Jia, Liu and Yan (2021) report that realised volatility and kurtosis relate positively and skewness negatively to future returns, driven by extreme positive returns (see leads).
- **Transfer.** Testable here as a predictive claim on daily bars: the highest daily return of the past 7 days (or the mean of the two highest), ranked across the point-in-time universe, against the next 7 days' return. Because the only source I could open is a null and the two abstracts point in opposite directions, the literature does not fix a direction. A Researcher must choose one before running and say which source it follows; the stock-market sign (negative) with a small predicted size is the conservative choice. Note the overlap with Section 1: a coin's maximum daily return is strongly related to its 1-week return, which predicts positively in large coins.

## 10. Beta, downside beta, skewness and kurtosis

**Claim.** Market beta, skewness and kurtosis of recent returns do not rank coins by future return; a higher downside beta is priced with a positive premium in cross-sectional regressions.

- **Nulls: Liu, Tsyvinski and Wu (1a), Table 7**, value-weighted, per week, quintile 5 minus 1: beta to the coin market over the previous 365 days -1.3 percent (t = -1.256); beta squared -1.2 (t = -1.191); skewness of daily returns in the formation week +0.5 (t = 0.383); kurtosis +0.6 (t = 0.647); delay (how much lagged market returns add to a coin's R-squared) -0.1 (t = -0.159). The highest-beta quintile earns 0.6 percent a week against 1.6 to 2.0 for the others, which is the direction of a low-beta effect but not significant. Sample end 2018-12-31.
- **Downside beta: Dobrynskaya and Dubrovskiy (2022)**, as in Section 1 (failures). Downside beta is the market beta estimated on weeks when the market return is negative; the priced quantity is downside beta minus ordinary beta. In cross-sectional regressions over 2014 to 2020 the downside-risk premium is positive and significant with respect to both the coin market and the US equity market (Tables 4 and 5; coefficients between 0.10 and 0.31 in the columns I could read, starred at 5 or 1 percent), and the coin-market downside premium loses significance once equity downside risk is included. I could not read the tables cleanly enough to attach each coefficient to its specification. Sample end 2020-11-01. Clean.
- **Costs.** Not considered.
- **Transfer.** Beta, skewness, kurtosis: testable here as predictive claims, all with a published null, so they are candidates for documented negatives rather than for effects. Beta to BTC over 365 daily bars is computable; "low beta earns more" has the published sign but no significance. Downside beta: testable only in part. It can be computed against BTC or the equal-weight universe from daily bars, but the published evidence is a risk premium in a regression over about 2,000 coins, estimated on weekly data, with no portfolio returns and no costs; a positive rank coefficient between downside beta and next-period return within 40 coins is a much weaker and noisier statement. The equity version needs `data.etf`, which makes it a cross-market hypothesis.

## Hourly bars

I found no published cross-sectional study on hourly bars that I could open. What exists at intraday frequency:

- Wen, Bouri, Xu and Zhao (2022) is a time-series study of intraday predictability in Bitcoin (abstract only; see leads). It belongs to the time-series family.
- An early draft by Bianchi and Dickerson reportedly sorts 26 coins every 12 hours on past return and volume (search snippet only; see leads).

A Researcher who needs hourly hypotheses in this family therefore has two honest options. One is to register an hourly version of a daily pattern (the reversal of Section 3, the volume-conditioned reversal of Section 4, or momentum over the past 24 to 168 hours) with origin `literature` and say plainly that the source is daily and the hourly horizon is an extension. The other is to treat hourly work as `exploration`. On hourly bars, as on daily ones, a bar's close and the next bar's open are the same instant, so bid-ask bounce remains in any one-bar reversal signal; skipping one bar between signal and entry is a design choice to state at registration.

## What transfers to our setup, in one table

| Pattern | Section | Computable from our bars | Published sign in large or liquid coins | Profit in the long leg | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1- to 4-week momentum | 1 | Yes | Positive | Yes | Testable as predictive and as long-only trading claim |
| Combined trend score | 2 | Simplified version only | Positive, largest 100 | Yes | Testable only in part |
| 1-day reversal | 3 | Yes | Weak or absent; negative net on Binance | Not reported | Testable as predictive; trading claim not supported |
| Reversal times volume shock | 4 | Yes | Low-volume reversal stronger | Not reported | Testable as predictive interaction |
| Size, price level | 5 | Price yes, size no | No gradient outside the smallest fifth | Yes, but in micro-caps | Not testable as published; weak proxy test |
| Dollar volume, its volatility | 6 | Yes | No gradient outside the lowest fifth | Yes, but in micro-caps | Testable only in part |
| Turnover | 6 | No | Null | n/a | Not testable |
| Amihud illiquidity | 6 | Yes | Null | n/a | Testable as a documented negative |
| Distance from 1-week high | 7 | Yes | Positive | Not reported | Testable as predictive |
| Low volatility | 8 | Yes | Low beats high, weakly | Yes | Testable as long-only trading claim |
| Maximum daily return | 9 | Yes | Sign disputed; null in the source opened | Not reported | Testable as predictive, direction to be chosen |
| Beta, skewness, kurtosis | 10 | Yes | Null | n/a | Testable as documented negatives |
| Downside beta | 10 | Yes | Positive premium (regression, whole market) | Not reported | Testable only in part |

## Unverified leads

Sources I could not open in full. Nothing here should be cited as evidence until someone reads the paper; where I read an abstract, that is all that is reported.

- **Zaremba, A., Bilgin, M. H., Long, H., Mercik, A. and Szczygielski, J. J. (2021). "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets." *International Review of Financial Analysis* 78, 101908. DOI 10.1016/j.irfa.2021.101908.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/finana/v78y2021ics1057521921002349.html)): daily prices of more than 3,600 coins; coins with a low return the day before outperform those with a high one; the effect is tied to illiquidity, and the few largest, most tradeable coins show daily momentum instead. The abstract gives no dates and no sizes. Paywalled. Worth reading first: it is the peer-reviewed source for the daily reversal and for its absence in large coins.
- **Shen, D., Urquhart, A. and Wang, P. (2020). "A three-factor pricing model for cryptocurrencies." *Finance Research Letters* 34, 101248. DOI 10.1016/j.frl.2019.07.021.** Search summary only: more than 1,700 coins, April 2013 to March 2019, a market, size and reversal factor model; reversal returns grow as coins get smaller. Not opened. Fičura (1c) describes it as equal-weighted with no capitalisation filter.
- **Dobrynskaya, V. (2023). "Cryptocurrency Momentum and Reversal." *Journal of Alternative Investments* 26(1), 65-76 (SSRN 3913263).** Library record and search summary only: about 2,000 coins, 2014 to 2020, sorting and holding periods from 1 week to 2 years; momentum up to 2 to 4 weeks, significant reversal beyond about a month, driven by past losers. Not opened (the link I tried led to a different paper by the same author, used above).
- **Grobys, K. and Sapkota, N. (2019). "Cryptocurrencies and momentum." *Economics Letters* 180, 6-10.** Abstract only, as recorded in time-series.md: 143 coins, 2014 to 2018, no significant momentum. Fičura's introduction adds that it reports a significant monthly reversal; not confirmed.
- **Zhang, W. and Li, Y. (2020). "Is idiosyncratic volatility priced in cryptocurrency markets?" *Research in International Business and Finance* 54, 101252. DOI 10.1016/j.ribaf.2020.101252.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/riibaf/v54y2020ics0275531920301926.html)): idiosyncratic volatility is positively related to expected returns in portfolio sorts and Fama-MacBeth regressions, robust to controls for size, momentum, liquidity, volume and price. No sample dates in the abstract. Opposite in sign to the low-volatility claim of Section 8.
- **Li, Y., Urquhart, A., Wang, P. and Zhang, W. (2021). "MAX momentum in cryptocurrency markets." *International Review of Financial Analysis* 77, 101829. DOI 10.1016/j.irfa.2021.101829.** Abstract only ([university listing](https://research.birmingham.ac.uk/en/publications/max-momentum-in-cryptocurrency-markets/)): higher maximum daily return goes with higher future returns; stronger in market upturns and at low sentiment. No dates or sizes. The open manuscript at the University of Reading repository answered with a bot check.
- **Grobys, K. and Junttila, J. (2021). "Speculation and lottery-like demand in cryptocurrency markets." *Journal of International Financial Markets, Institutions and Money* 71, 101289. DOI 10.1016/j.intfin.2021.101289.** Abstract only ([repository record](https://jyx.jyu.fi/jyx/Record/jyx_123456789_74624/Description)): lowest-MAX quintile beats the highest by more than 1.50 percent a week, raw and risk-adjusted. A search snippet gives the sample as 20 coins excluding Bitcoin, January 2016 to December 2019; not confirmed. The other repository refused the connection.
- **Jia, Y., Liu, Y. and Yan, S. (2021). "Higher moments, extreme returns, and cross-section of cryptocurrency returns." *Finance Research Letters* 39, 101536. DOI 10.1016/j.frl.2020.101536.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/finlet/v39y2021ics1544612320303135.html)): 84 coins, moments computed from intraday data; volatility and kurtosis positively and skewness negatively related to future returns. No dates in the abstract.
- **Zhang, W., Li, Y., Xiong, X. and Wang, P. (2021). "Downside risk and the cross-section of cryptocurrency returns." *Journal of Banking & Finance* 133, 106246. DOI 10.1016/j.jbankfin.2021.106246.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/jbfina/v133y2021ics0378426621002053.html)): a positive cross-sectional relation between downside risk and future returns. The abstract does not name the measure or the sample.
- **Burggraf, T. and Rudolf, M. (2021). "Cryptocurrencies and the low volatility anomaly." *Finance Research Letters* 40, 101683. DOI 10.1016/j.frl.2020.101683.** A university magazine summary only: about 1,000 coins, 2013 to 2019, decile sorts on past volatility, and the low-volatility strategy earned negative returns. Not opened. If confirmed, a published failure of Section 8 in the broad market.
- **Wen, Z., Bouri, E., Xu, Y. and Zhao, Y. (2022). "Intraday return predictability in the cryptocurrency markets: Momentum, reversal, or both." *North American Journal of Economics and Finance* 62, 101733. DOI 10.1016/j.najef.2022.101733.** Abstract only ([RePEc listing](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html)): Bitcoin high-frequency prices 2013-03-03 to 2020-05-31, both intraday momentum and intraday reversal, also in Ethereum, Litecoin and Ripple; a timing strategy beats buy-and-hold. Time-series, not cross-sectional; the abstract does not give the intervals.
- **Bianchi, D. and Dickerson, A. "Trading Volume in Cryptocurrency Markets." Working paper, about 2018.** Search snippet only: 26 coins, portfolios re-formed every 12 hours on past return and volume, gross annualised Sharpe ratios up to 2.96. Not found or opened. The only lead on a sub-daily cross-sectional sort.
- **Han, C., Kang, B. and Ryu, J. Working paper on time-series and cross-sectional momentum under realistic assumptions.** Not opened. **Hindsight flag: sample reported as December 2013 to August 2023, which overlaps the dev segment** (see time-series.md). Its claim (weak cross-sectional momentum once costs are modelled) may be noted; its results must not be used as a reason to expect something.
- **Fieberg et al. (2025), supplement, Table B.8.** The replication of the Liu, Tsyvinski and Wu sorts on April 2015 to May 2022. Not opened; the main text says all the spreads remain significant.
- **Liu, Tsyvinski and Wu (2022), published version.** Paywalled; the numbers here are from the 2019 working paper.
- **From memory, not searched or not found:** Kozlowski, Puleo and Zhou (2020 or 2021) on weekly reversals (cited by Fičura as reporting a weekly reversal in small coins); Zhang and Li on liquidity risk; Leirvik (2022) on the volatility of liquidity; Garfinkel, Hsiao and Hu on disagreement, volume and returns (cited by Fieberg et al. as 2025, so check its sample dates before use); Cong, Karolyi, Tang and Zhao on value and network factors (needs data we do not have).

## Where I found nothing

- No cross-sectional study on hourly bars that I could open.
- No source restricted to one exchange's most liquid 40 or so pairs with changing membership; the closest are the largest 100 by capitalisation (Section 2), the 100 most liquid by Amihud ratio (Sections 3 and 4) and 35 large coins (Section 8).
- No source that separates bid-ask bounce from true reversal in crypto.
- No test of a long window distance-from-high (52-week-high) signal on crypto.
- No long-only test of momentum against an equal-weight benchmark of the same coins after costs, except the top trend quintile in Section 2 (reported net, but not against that benchmark) and the liquid winners of Section 1b (against a capitalisation-weighted market).
- No evidence that abnormal volume alone predicts next-period returns across coins; the one source that tests it finds little (Section 4).
