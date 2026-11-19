# Derivatives: literature notes

Collected by the Literature scout on 2026-11-19. Question of this run: what is the published evidence that perpetual-futures data (funding rate, basis, open interest, positioning ratios, liquidations) predicts the **spot** returns of cryptocurrencies, at daily and hourly horizons? The series are predictors only: we never hold a perpetual position.

**The short answer is that the evidence is thin.** The academic literature on perpetual futures is mostly about pricing the contract, about the return to a hedged carry trade (long spot, short perpetual: not available to us), and about which market leads price discovery at one minute or less. I found no peer-reviewed test of the funding rate, of open-interest growth, of long/short account ratios or of taker imbalance as a predictor of spot returns on a multi-coin sample that ends by 2022. Several of the most relevant papers were readable only as abstracts. A Researcher registering from this file should treat most entries as weak priors, and say so in the hypothesis file.

How to read an entry:

- Numbers are the paper's own, in its units, with the table or section they come from. Arithmetic of mine is marked "(my arithmetic)". I read the arXiv papers through a text extraction of their HTML versions, which garbles some tables; where a number is uncertain for that reason the entry says so, and it should be checked against the paper before it is quoted in a hypothesis file.
- "Opened" says which version I read. Publisher pages mostly answered with an access error, and working-paper PDFs came back as unreadable binary, so for those I read an abstract page only. By the scout's rule an abstract-only source is not an entry: it is listed under "Unverified leads", with exactly what the abstract states.
- "Sample end" is checked against the split: a sample ending by 2022-12-31 is clean evidence for the train segment. **This literature is young, and half of the sources I could open in full run past 2022. Each is marked "Hindsight flag". For a flagged source the claim may motivate a hypothesis; its numbers are full-sample figures that include dev-segment (or test-segment) data and must not be used as a reason to expect an effect or as an expected size.**
- The four sub-angles of the brief: (1) funding rate, (2) basis or futures premium, (3) open interest and positioning, (4) liquidations, leverage and price discovery.

Sections 1 to 6 are sources opened in full, ordered by how much they say about spot returns. After them come the unverified leads, grouped by sub-angle, then what transfers.

## 1. The perpetual's premium over spot follows past returns and is large; the profit is in a hedged trade (sub-angle 2)

**Claim.** Perpetual futures deviate from their no-arbitrage price by large amounts in both directions; the deviation is higher after the coin has risen, which the authors read as extrapolative demand for leveraged long exposure; a hedged trade that bets on convergence is profitable after fees.

- **Reference.** He, S., Manela, A., Ross, O. and von Wachter, V. (2022, revised 2024). "Fundamentals of Perpetual Futures." arXiv:2212.06888. <https://arxiv.org/abs/2212.06888>. Working paper.
- **Opened.** The HTML of version 5 (<https://arxiv.org/html/2212.06888v5>), about the first four fifths of the text: Sections 1 to 5 and Tables 2 to 9. The last part (appendix) was not read.
- **Sample.** BTC, ETH, BNB, DOGE and ADA perpetuals and spot on Binance, hourly prices and 8-hourly funding; start 2020-01-08 (BTC, ETH), 2020-01-31 (ADA), 2020-02-10 (BNB), 2020-07-10 (DOGE); end 2024-03-11 for all (Section 4.1, Table 2). Stablecoin interest rates from Aave.
- **Method.** A no-arbitrage benchmark for the perpetual given the funding rule and the interest rate; the deviation from it, expressed as an annualised rate (rho); a trading rule that opens a hedged position when the deviation is outside the round-trip cost bounds and closes it when the deviation returns to zero.
- **Size of the deviations (Table 4).** Mean deviation close to zero and insignificant for every coin (between -0.10 and 0.04). Mean absolute deviation 0.57 (BTC), 0.63 (ETH), 0.88 (BNB), 0.86 (DOGE), 0.83 (ADA), that is, 57 to 88 percent a year.
- **Past returns (Section 5, Table 9).** Pooled daily regression with coin fixed effects, 7,235 observations: the deviation on the coin's annualised spot return over the past 120 days has a coefficient of 0.13 (t = 4.52), or 0.20 (t = 10.43) with volatility as a control; the absolute deviation 0.05 (t = 4.07). I read these from a garbled table: check before quoting. Deviations co-move strongly across the five coins (Figure 3). A time trend of -0.11 a year in the absolute deviation: the gap has been shrinking.
- **What it does not test.** There is no regression of future spot returns on the deviation or on the funding rate. The regressions run the other way (returns explain the deviation). The paper notes only that the deviation's correlation with the same period's spot return is modest.
- **The strategy is hedged (Section 4.3, Tables 5 to 7).** Long spot and short perpetual when the perpetual is rich, the reverse when it is cheap; a variant never shorts spot but still shorts the perpetual. Sharpe ratios at the highest fee tier (6.75 bps spot, 1.44 bps futures, maker fees): 1.80 (BTC) to 4.84 (BNB) unrestricted; 1.62 to 3.29 for the long-spot-only variant. Most of the profit is price convergence, less of it funding payments (Table 8).
- **Costs.** Maker fees in three tiers; bid-ask spread and price impact assumed below 0.35 bps and left out. Far below our 12 to 25 bps per side.
- **Sample end.** 2024-03-11. **Hindsight flag: 14 of the 50 months lie in the dev segment.** All figures above are full-sample.
- **Transfer.** Not testable as published: every version of the strategy needs a short perpetual leg. What transfers is a description of the predictor: our basis series (the hourly premium index) is, by this paper, a measure of leveraged long demand that rises after rallies, has no drift, moves together across coins and has been getting smaller. Two consequences for a registration. First, any hypothesis that uses the premium must control for, or at least report against, past returns, or it re-tests momentum. Second, the paper gives no direction for spot: "a high premium predicts low spot returns" is the crash claim of the BIS paper under leads (2a), not a result of this one.

## 2. Funding rate and price changes lead each other at 8 hours (sub-angle 1)

**Claim.** Changes in the BitMEX funding rate and changes in the Bitcoin price Granger-cause each other at the 8-hour frequency.

- **Reference.** Nimmagadda, S. S. and Ammanamanchi, P. S. (2019). "BitMEX Funding Correlation with Bitcoin Exchange Rate." arXiv:1912.03270. <https://arxiv.org/abs/1912.03270>. Not peer reviewed; 9 pages.
- **Opened.** The full paper (<https://arxiv.org/html/1912.03270v1>).
- **Sample.** BitMEX funding rate of the inverse Bitcoin perpetual and the Bitstamp Bitcoin price, 8-hour observations, 2016-06-04 to 2019-10-03, 3,649 observations.
- **Method and result.** Granger causality on first differences of both series, lag length by AIC (not reported). "Price does not cause funding" is rejected (F = 4.29, p = 5e-08) and so is "funding does not cause price" (F = 7.11, p = 1e-15). The paper reports no coefficient, no sign and no size for the direction funding to price. In the conclusion the authors read it as momentum (very high funding goes with high prices), which is an interpretation, not a test. A trading rule based on funding is named as future work.
- **Costs.** Not considered.
- **Sample end.** 2019-10-03. Clean, and entirely before our derivatives data starts (2020-01), so the whole train segment is post-sample for it.
- **Transfer.** Testable here as a predictive claim: the change in a coin's funding rate at the last funding event against its spot return over the next 8 hours (hourly bars) or the next day. The paper supports "there is information", not a direction, so a registration has to choose the sign from an argument and say that the source does not fix it. It is one coin on another exchange with another contract type (inverse), the test is on price changes rather than returns, and the funding rate of that era was partly a lagged function of the premium, so funding "predicting" price may be the premium doing it.

## 3. The Binance USDT perpetual is the main source of volatility for spot markets (sub-angle 4)

**Claim.** In five-minute realised volatility, the Binance tether-margined Bitcoin perpetual transmits volatility to every other Bitcoin spot and perpetual market and receives little; spot traders react more slowly.

- **Reference.** Alexander, C., Heck, D. F. and Kaeck, A. (2021). "The Role of Binance in Bitcoin Volatility Transmission." arXiv:2107.00298. <https://arxiv.org/abs/2107.00298>. Later published in *Applied Mathematical Finance* (from memory; I did not open the published version).
- **Opened.** The arXiv paper through <https://ar5iv.labs.arxiv.org/html/2107.00298>, Sections 1 to 5.2 and Tables 1 to 13; the end of Section 5 and the conclusion were not read.
- **Sample.** Bitcoin, 2021-01-01 to 2021-03-31. Spot: BTC/USD on Coinbase, Bitstamp and Kraken, BTC/USDT on Binance and Huobi. Perpetuals: Binance USDT (linear), Binance USD and Bybit USD (inverse). Second-by-second prices, realised volatility over five-minute intervals.
- **Method.** Multiplicative error models of pre-averaged, diurnally adjusted realised volatility, one market's lagged volatility entering another's equation.
- **Size.** The Binance USDT perpetual sends flows of about 0.18 to Bybit and 0.15 to the Binance USD perpetual (Table 7): a one-standard-deviation shock raises expected volatility there by about 4.3 and 3.4 percent. It is the main emitter to the spot markets as well (Section 4.2, Table 8, Figure 1), also under two other volatility measures (Tables 10 and 11). Spillovers are lowest in Asian hours and highest in US hours (Table 9).
- **What it does not test.** Returns. It cites Alexander and Heck (2020) for derivatives leading price discovery. It is about volatility five minutes ahead.
- **Costs.** Not applicable (no strategy).
- **Sample end.** 2021-03-31. Clean. One quarter, one coin.
- **Transfer.** Testable only in part. The claim is about volatility, at five minutes, from perpetual price moves, and the Store holds no perpetual price bars, only the premium index. An hourly version would ask whether last hour's variation in the premium (the high-low range of the hourly premium bar) predicts the next hour's spot volatility beyond spot's own lagged volatility. That is a predictive claim about risk, usable for a rule that goes flat when volatility is forecast to rise, and five-minute effects may be gone at one hour.

## 4. Open interest and same-day volatility are negatively related on Binance and Bybit (sub-angle 3)

**Claim.** On centralised exchanges, Bitcoin's daily volatility is higher on days of high trading volume and lower on days of high open interest in perpetuals.

- **Reference.** Chen, E., Ma, M. and Nie, Z. (2024). "Exploring the Impact: How Decentralized Exchange Designs Shape Traders' Behavior on Perpetual Future Contracts." arXiv:2402.03953. <https://arxiv.org/abs/2402.03953>. Working paper.
- **Opened.** The full paper (<https://arxiv.org/html/2402.03953v4>).
- **Sample.** Bitcoin perpetuals, daily. Binance and Bybit from 2020-08-05, 1,147 observations each, which puts the end near 2023-09-25 (my arithmetic; the three decentralised exchanges in the paper end 2023-09-26). Data from Coinalyze; Bitcoin prices from CryptoCompare.
- **Method.** Garman-Klass daily volatility regressed on its own lags and on the expected and unexpected parts (from an ARIMA model) of open interest, volume and liquidated volume **of the same day** (Equation 2).
- **Result (Table 1).** Expected and unexpected open interest both carry negative, significant coefficients on Binance and on Bybit; volume carries positive ones. On two decentralised exchanges, liquidations of long positions go with higher volatility and liquidations of shorts mostly do not (Tables 1 and 2, Section 3.3).
- **What it does not test.** Prediction. Every regressor except lagged volatility is contemporaneous, and the dependent variable is volatility, not the direction of returns.
- **Costs.** Not applicable.
- **Sample end.** About 2023-09-25. **Hindsight flag: about nine months of the sample lie in the dev segment.**
- **Transfer.** Testable only in part, and only by changing the claim: a lagged version (yesterday's open-interest level or surprise against today's realised volatility) is not in the paper. Open interest in the Store starts 2021-12 for most coins, so train is about one year. The sign also runs against the practitioner story that high open interest is a "powder keg" for volatility; a registration should state which of the two it predicts.

## 5. Exchange-reported open interest is unreliable at short intervals (data caveat for sub-angle 3)

Not a return pattern: a published reason to distrust the input.

- **Reference.** Giagkiozis, I. and Said, E. (2024). "Reconciling Open Interest with Traded Volume in Perpetual Swaps." *Ledger* 9, 1-15. arXiv:2310.14973. <https://arxiv.org/abs/2310.14973>.
- **Opened.** The full paper (<https://arxiv.org/html/2310.14973v2>).
- **Sample.** Twelve Bitcoin perpetual markets on seven exchanges (Bybit, Deribit, Binance, BitMEX, OKX, Kraken, HTX); tick data for January 2023 and for July to September 2023.
- **Method.** For a perpetual the absolute change in open interest over an interval cannot exceed the volume traded in it. The paper counts the intervals in which the reported figures break that bound.
- **Result.** Several large exchanges report open interest that cannot be reconciled with their reported volume. For the Binance BTCUSDT perpetual the bound holds over each whole period; within January 2023 it is broken in 0.4 percent of hours and 14.0 percent of minutes; within July to September 2023 in 27.2 percent of days, 41.1 percent of hours and 33.4 percent of minutes. The authors cannot say whether open interest, volume or both are wrong.
- **Sample end.** 2023-09. **Hindsight flag** in form only: it is a statement about data quality, not about returns, and it says nothing about 2021-12 to 2022-12, the part of the train segment that has open interest.
- **Transfer.** Applies directly: our open interest is Binance's own 5-minute snapshot series. Hypotheses on hourly open-interest **changes** rest on the least reliable form of the data; daily levels or multi-day growth are safer. Worth a check by the Data steward on train: how often the hourly change in open interest exceeds the hour's perpetual volume (which needs perpetual volume, not in the Store).

## 6. Practitioner check: funding changes move with prices and do not predict them (sub-angle 1)

A practitioner note, opened in full. Used as a lead and as a prior, not as evidence.

- **Reference.** Jung, J. H. (2024-08-02). "Can Funding Rate Predict Price Change?" Presto Research. <https://prestolabs.io/research/can-funding-rate-predict-price-change>.
- **Sample.** BTC on Binance, roughly early 2021 to early 2024 (dates not stated; read from the figure's description); 7-day windows.
- **Result.** The 7-day change in annualised funding against the 7-day price change of the same window: R-squared 12.5 percent, positive slope. The funding change of one window against the price change of the next: R-squared zero, which the author calls no predictive power. A cross-sectional signal built from funding across the 50 most liquid Binance perpetuals is said to look favourable before costs with very high turnover; its numbers are in images I could not read.
- **Costs.** None.
- **Sample end.** About early 2024. **Hindsight flag: overlaps the dev segment.**
- **Transfer.** A published null for the time-series version of "funding predicts returns" on BTC at a weekly horizon, and a hint that the cross-section of coins is the more promising form. Both are testable here as predictive claims; neither has an academic source behind it.

A second source opened in full, also flagged, adds only context to sub-angle 2: Borri, N., Liu, Y., Tsyvinski, A. and Wu, X. (2025), "Cryptocurrency as an Investable Asset Class: Coming of Age", arXiv:2510.14435 (<https://arxiv.org/html/2510.14435v4>, first three quarters read), Section 3.6: the hedged carry trade on Binance Bitcoin perpetuals (long spot, short perpetual, earning funding) is described as highly profitable in the past and compressing since. **Hindsight flag: its sample runs to 2025 and overlaps the test segment; I record the claim only.** Not testable here (short perpetual leg).

## Unverified leads

Sources I could not open in full. For each: what the abstract (or the page named) states, nothing more. "From memory" marks what I recall and could not confirm. None of this should be cited as evidence until someone reads the paper.

### Sub-angle 2: basis and carry

**2a. A high futures premium predicts price crashes.** Schmeling, M., Schrimpf, A. and Todorov, K. (2023, revised 2025). "Crypto carry." BIS Working Papers 1087 (<https://www.bis.org/publ/work1087.htm>); also CEPR Discussion Paper 20719; forthcoming in *Management Science*, DOI 10.1287/mnsc.2024.05069.
- Read: the BIS summary page (abstract, focus, contribution, findings) and the abstract of the 2025 CEPR version. The PDF came back unreadable and the journal page refused access.
- States: Bitcoin and Ether; carry is the futures price over the spot price, the return to long spot and short futures; it averages above 10 percent a year and reaches up to 60 percent (2023 abstract; "at times above 40 percent" in the 2025 abstract); interest rates explain little of it; it is driven by smaller trend-chasing investors seeking leverage and by scarce arbitrage capital; **high carry predicts future price crashes**, and a rise in carry coincides with dearer crash insurance (2023 findings; the 2025 abstract no longer states the crash result).
- From memory, not confirmed: the sample starts around 2019 and uses both dated futures (CME and offshore) and perpetuals; high carry also predicts liquidations of long futures positions.
- **Sample end unknown. Hindsight flag: the paper was revised in October 2025, so treat the sample as overlapping dev until checked.**
- Transfer if confirmed: this is the one source whose claim is about the spot price itself and suits long or flat. Testable as a predictive claim (a coin's trailing average premium or funding against the probability or size of a large fall over the next days) or as a trading claim (flat while the premium is extreme, against buy-and-hold). It is the first paper to read: it decides the direction for sub-angles 1, 2 and 4.

**2b. The basis is the strongest cross-sectional predictor of crypto futures returns, at daily horizons only.** Chi, Y., Hao, W., Hu, J. and Ran, Z. (2023). "An empirical investigation on risk factors in cryptocurrency futures." *Journal of Futures Markets* 43(8), 1161-1180. DOI [10.1002/fut.22425](https://doi.org/10.1002/fut.22425). Earlier working paper: "Factor Structure of Cryptocurrencies".
- Read: the abstract ([RePEc listing](https://ideas.repec.org/a/wly/jfutmk/v43y2023i8p1161-1180.html)). The publisher and a conference copy of the working paper refused access.
- States: major cryptocurrencies, 2017 to 2021; basis, momentum and basis-momentum factors earn significant excess returns, as in commodity futures; basis is the strongest predictor of cross-sectional differences in **futures** returns; the momentum premium is not statistically strong; the basis-momentum premium vanishes after controlling for basis; daily factor returns are far more significant than weekly ones and monthly ones are not significant.
- Not in the abstract: which coins and exchanges, the direction of the basis sort, sizes, costs. A search summary of the working paper says most of the long-short profit is in the long leg; I could not confirm it. From memory of the commodity literature the long leg is the low-basis (backwardated) contracts.
- **Sample end 2021. Clean.**
- Transfer if confirmed: testable only in part. The returns are futures returns, which include the funding or roll that a spot holder never receives; if the basis predicts futures returns only through that carry, nothing is left for spot. What a registration can test is the spot part: rank the point-in-time universe by the premium index, hold the low-premium (or high-premium, to be decided from the paper) group, daily rebalancing, against the equal-weight universe. Daily rebalancing of a cross-sectional sort is expensive at 12 to 25 bps per side, and the paper says the effect is gone at a monthly horizon.

**2c. The dated-futures basis has some power to predict spot price changes, with a bias.** Lee, S., El Meslmani, N. and Switzer, L. N. (2020). "Pricing efficiency and arbitrage in the bitcoin spot and futures markets." *Research in International Business and Finance* 53, 101200. DOI [10.1016/j.ribaf.2020.101200](https://doi.org/10.1016/j.ribaf.2020.101200).
- Read: the abstract ([university listing](https://abdn.elsevierpure.com/en/publications/pricing-efficiency-and-arbitrage-in-the-bitcoin-spot-and-futures-)).
- States: Bitcoin spot and all CBOE and CME futures contracts, January 2018 to March 2019; the basis has some predictive power for future changes in the spot price and in the risk premium, but is a biased predictor; spot-futures gaps persist and widen after thefts and new coin issues.
- **Sample end 2019-03. Clean.** One coin, regulated dated futures, fifteen months, direction and size not in the abstract.
- Transfer: testable only in part (we have the perpetual premium, not a dated basis; the claim is the textbook regression of the spot change on the basis).

**2d. Not opened.** Christin, N., Routledge, B., Soska, K. and Zetlin-Jones, A. "The Crypto Carry Trade" (working paper, Carnegie Mellon; <https://www.andrew.cmu.edu/user/azj/files/CarryTrade.v1.0.pdf> came back unreadable). From memory: the return to the hedged trade (long spot, short futures) on offshore exchanges and its exposure to liquidation; not testable here. Cao, Y., Luo, P., Cheng, Y. and Dong, Y., "Anatomy of Cryptocurrency Perpetual Futures Returns": I found only a third-party summary (134 candidate signals for perpetual returns, basis the strongest) and no primary source. Fan, Z., Jiao, F., Lu, L. and Tong, X., "The Risk and Return of Cryptocurrency Carry Trade": per search summaries it sorts coins on lending interest rates, not on futures basis; data we do not have. Koijen, R., Moskowitz, T., Pedersen, L. and Vrugt, E. (2018), "Carry", *Journal of Financial Economics* 127(2): the parent result, from memory, that carry predicts returns in every asset class studied; not opened in this run, no crypto.

### Sub-angle 3: positioning

**3a. Positions of speculators and retail traders predict Bitcoin futures returns.** Shi, S. (2022). "Bitcoin futures risk premia." *Journal of Futures Markets* 42(12), 2190-2217. DOI [10.1002/fut.22373](https://doi.org/10.1002/fut.22373).
- Read: the abstract ([RePEc listing](https://ideas.repec.org/a/wly/jfutmk/v42y2022i12p2190-2217.html)).
- States: trading activity and extreme sentiment of speculators and of retail traders help predict subsequent changes in Bitcoin futures prices at several horizons; speculators are negative-feedback traders and retail traders positive-feedback traders; lower transaction costs go with higher risk premia; some macro variables predict futures returns; the effect of hedgers' position changes depends on extreme macro conditions.
- Not in the abstract: sample dates, contract, the sign of the positioning effect. From memory, not confirmed: CME futures and the weekly Commitments of Traders report.
- **Sample end not stated; published December 2022, so it ends by 2022. Clean on that reasoning.**
- Transfer if confirmed: testable only in part. We have no trader-category positions. The nearest series are Binance's long/short account ratios (all accounts, and top traders), which count accounts rather than size; "retail" maps loosely to the all-accounts ratio. Train is about one year. The abstract gives the feedback behaviour, not the direction of the prediction, so the paper must be read before a sign is registered.

### Sub-angle 4: liquidations, leverage and price discovery

**4a. Perpetuals on offshore exchanges lead spot in price discovery, at one-minute resolution.** Two papers, abstracts only.
- Alexander, C., Choi, J., Park, H. and Sohn, S. (2020). "BitMEX bitcoin derivatives: Price discovery, informational efficiency, and hedging effectiveness." *Journal of Futures Markets* 40(1), 23-43. DOI [10.1002/fut.22050](https://doi.org/10.1002/fut.22050) ([abstract](https://econpapers.repec.org/RePEc:wly:jfutmk:v:40:y:2020:i:1:p:23-43)). States: minute data; BitMEX derivatives lead the major spot exchanges; spreads, price gaps between exchanges and relative volume determine which market leads; the derivatives are informationally more efficient than spot. A search summary gives the perpetual about half of two price-discovery measures across four markets; not confirmed.
- Alexander, C. and Heck, D. F. (2020). "Price discovery in Bitcoin: The impact of unregulated markets." *Journal of Financial Stability* 50, 100776. DOI [10.1016/j.jfs.2020.100776](https://doi.org/10.1016/j.jfs.2020.100776) ([abstract](https://econpapers.repec.org/RePEc:eee:finsta:v:50:y:2020:i:c:s1572308920300759)). States: minute-level information flows within and between spot and derivatives; perpetuals and futures on Huobi, OKEx and BitMEX lead by a wide margin; CME futures and US spot exchanges mostly react, and may be slow to.
- **Sample ends: not in the abstracts; both were published in 2020, so they end by then. Clean.** Bitcoin only.
- Transfer: not testable at our granularity as published. A lead measured in minutes says nothing reliable about the next hourly bar. The hourly form of the claim (the last hour's change in the premium index, that is, the perpetual's move not yet matched by the index, predicts the next hour's spot return with a positive sign) is a new hypothesis that this literature motivates and does not support; expect it to be small against 24 to 50 bps for a round trip.

**4b. The opposite for regulated futures: spot leads.** Baur, D. G. and Dimpfl, T. (2019). "Price discovery in bitcoin spot or futures?" *Journal of Futures Markets* 39(7), 803-817. DOI [10.1002/fut.22004](https://doi.org/10.1002/fut.22004) ([abstract](https://econpapers.repec.org/RePEc:wly:jfutmk:v:39:y:2019:i:7:p:803-817)). States: with the information-share measures of Hasbrouck and of Gonzalo and Granger, spot price changes come before those of the CBOE and CME futures launched in December 2017, which the authors put down to spot's larger volume and round-the-clock access. Sample ends by 2019; clean. It sets the prior that "the futures market leads" is a statement about where the volume is, not a law.

**4c. Long positions are liquidated about twice as often as shorts.** Cheng, Z., Deng, J., Wang, T. and Yu, M. (2021). "Liquidation, Leverage and Optimal Margin in Bitcoin Futures Markets." arXiv:2102.04591 ([abstract](https://arxiv.org/abs/2102.04591)). States: BitMEX Bitcoin perpetual; about 3.51 percent of long and 1.89 percent of short positions are liquidated per day; liquidated traders use 60x leverage on average; margins would need to be far higher to make a daily margin call a 1 percent event. Sample dates not in the abstract; submitted 2021-02, so clean. Descriptive, not predictive, and the Store has no liquidation data: not testable. It supports looking for the effect of leverage on the downside.

**4d. Not opened.** Soska, K., Dong, J.-D., Khodaverdian, A., Zetlin-Jones, A., Routledge, B. and Christin, N. (2021). "Towards Understanding Cryptocurrency Derivatives: A Case Study of BitMEX." *Proceedings of The Web Conference 2021*, DOI 10.1145/3442381.3450059 (the PDF came back unreadable): per its university press coverage, small positions are liquidated disproportionately and liquidations can feed volatility in spot. Albers, J., Cucuringu, M., Howison, S. and Shestopaloff, A. (2021), "Fragmentation, Price Formation, and Cross-Impact in Bitcoin Markets", arXiv:2108.09750, abstract only: order-flow features predict returns 500 milliseconds ahead across the most liquid Bitcoin markets and give a leader-lagger network; far below our granularity. Two 2026 arXiv papers seen only in search results, **both flagged because their samples include 2024 and later**: 2607.27070 (early-warning signals around seven liquidation cascades in the Binance BTCUSDT perpetual) and 2607.09426 (order imbalance at quarter-hour boundaries predicting returns in crypto futures).

### Practitioner leads (sub-angles 1 and 3), not opened beyond news summaries

- K33 Research and VanEck statistics, as reported in news: Bitcoin's returns after periods of negative average funding were well above average (a contrarian reading of funding). Seven episodes since 2018 by K33's own count, and the periods include 2023 on. **Hindsight flag.** This is the only source I found for the "crowded positioning" reading of funding, and it is not a study.
- Brave New Coin, "Testing theory: is perpetual swap funding rate predictive": funding against the next 8 hours' return on BitMEX, result described as mixed. Not opened.
- The Block (2024), on Binance's long/short account ratio: anecdotes that readings near or below 1 preceded falls. **Hindsight flag.** No test.
- K33 (2023), on CME: lower next-day Bitcoin returns after days of rising open interest with a falling basis. **Hindsight flag.** No Binance equivalent tested.

## What transfers to our setup

Setup: spot only, long or flat, the point-in-time universe (40 USDT pairs on Binance, monthly reconstitution), daily and hourly bars in UTC, signal at a bar's close and trade at the next open, 12 to 25 bps per side. Predictor history: funding and basis from 2020-01 (three years of train), open interest and ratios from 2021-12 (one year; BTC from 2020-09).

- **The hedged carry trade does not transfer at all.** The profitable strategies in He et al., Borri et al., Christin et al. and the carry side of Schmeling et al. are long spot and short perpetual. They say funding and premium are on average paid by longs; they say nothing about the spot leg alone.
- **The direction for spot is supported by one abstract.** "High premium, then crash" (lead 2a) is the only published claim about spot prices, and I could not read the paper. The momentum reading (premium and funding rise with prices, Sections 1, 2 and 6) and the contrarian reading (crowded longs get liquidated, 2a and the practitioner leads) are both in the literature, and for a contemporaneous relation they do not conflict: the premium is high because the price rose. They differ on what happens next, and no source I opened tests that.
- **Control for past returns.** By Section 1 the premium is in part a function of the past 120-day return. A premium or funding signal that is not measured against the coin's own momentum is a momentum test with a noisier input.
- **Funding is a smoothed, capped function of the premium.** On Binance the funding rate is built from the premium index averaged over the funding interval plus a clamped interest component (from memory of the exchange's documentation, not checked in this run). The two series are not independent evidence; the premium is the hourly one and funding the 8-hourly one.
- **Cross-section over time series.** The only academic result on predicting returns across coins is the basis factor (lead 2b), for futures returns. The practitioner note (Section 6) points the same way. With 40 coins a pooled or ranked predictive claim has far more observations than a single-coin regression, which matters with a three-year train segment.
- **Open interest: one year of train, doubtful hourly changes.** Section 5 argues for daily levels and multi-day growth rather than hourly changes. The only relation I could open (Section 4) is contemporaneous and about volatility.
- **Hourly lead-lag is unsupported.** Price discovery results are at one minute or below. An hourly test is legitimate as a hypothesis and should predict a small effect.
- **Costs.** Almost none of these sources considers costs at our level; the one that does (Section 1) uses maker fees below 7 bps on a hedged trade. A daily cross-sectional sort or an hourly signal must clear 24 to 50 bps for a round trip.

Forms a Researcher could register, with the support each has:

| Hypothesis form | Granularity | Support |
| --- | --- | --- |
| Extreme premium or funding predicts a lower or more negative-skewed spot return over the next days; flat while extreme | daily | Lead 2a (abstract only, sample end unknown: flagged); mechanism in Section 1 |
| Cross-sectional rank of coins by premium predicts next-day spot returns | daily | Lead 2b (abstract only, clean, futures returns); Section 6 (practitioner, flagged) |
| Change in funding at the last event predicts the next 8 hours' spot return | hourly | Section 2 (opened, clean, no sign, one coin); Section 6 says no at a weekly horizon |
| Premium predicts returns beyond what the coin's own past return predicts | daily | Section 1 gives the confound, not the result |
| Last hour's change in the premium predicts the next hour's spot return | hourly | Leads 4a, 4b (one-minute evidence only): motivation, not support |
| Variation of the premium predicts next-hour or next-day spot volatility | hourly or daily | Section 3 (opened, clean, five-minute, BTC, one quarter) |
| Open-interest level or growth predicts next-day volatility | daily | Section 4 (opened, flagged, contemporaneous, negative sign); Section 5 caveat |
| All-accounts long/short ratio predicts next-day returns | daily | Lead 3a (abstract only, other data); practitioner anecdotes |

## Where I found nothing

- No academic paper that tests the **funding rate** (level, extremes, changes or cumulative funding) as a predictor of spot returns on more than one coin, with a stated sample ending by 2022. The contrarian "crowded longs" reading of funding has only practitioner statistics behind it.
- No academic test of **open-interest growth**, or open interest relative to volume, as a predictor of returns in crypto perpetuals.
- No academic test of **long/short account ratios, top-trader ratios or the taker buy/sell ratio of perpetuals** as predictors of spot returns or volatility.
- No academic test of **liquidations** as a predictor of subsequent returns (reversal after a cascade) on a sample ending by 2022; and the Store has no liquidation series.
- No **hourly** lead-lag study between perpetual and spot; everything is at one minute or faster.
- No source that tests any of these on a liquidity-ranked universe with changing membership.
