# Literature

Published evidence on crypto return patterns, collected by the Literature scout (`.claude/agents/literature-scout.md`) as a supply of hypotheses that do not come from our own data. One file per family; one line per pattern here.

A pattern listed here is a lead, not a finding: it becomes a hypothesis when a Researcher registers it. Each entry carries the sample end date of its source, because a paper whose sample runs past 2022 overlaps our dev or test segments.

## Time-series

Notes: [time-series.md](time-series.md).

- **Price above its 5- to 100-day moving average: long, otherwise cash.** Raises the Sharpe ratio over buy-and-hold on Bitcoin (1.92 to between 2.09 and 2.51) with break-even costs of 112 to 396 bps one way; the gain is in drawdown, not return, shrinks for long windows, and a later study finds only a one-week price-to-average ratio survives data-snooping control. Sources: Detzel et al. 2021 (sample to 2018-01), Hudson and Urquhart 2021 (to 2017-12, out-of-sample failure on Bitcoin in 2018), Wei et al. 2024 (to 2022-03). Testable here as published.
- **Short-horizon time-series momentum: the past week's return predicts the next one to four weeks.** Weekly coefficient 0.19 to 0.22 on Bitcoin, concentrated after very strong weeks; daily effect weak under bootstrap; weaker for Ethereum; no costs. Source: Liu and Tsyvinski 2021, working paper version (sample to 2018-05). Testable as a predictive claim; as a long-or-flat trading claim only in part.
- **Momentum lives at one to four weeks and is gone by eight (cross-sectional evidence, filed here for its horizon).** Winners-minus-losers earns 2.5 to 4.1 percent a week at 1- to 4-week lookbacks, nothing at 8 to 100 weeks; profit is in the long leg and in large coins. Source: Liu, Tsyvinski and Wu 2022, working paper version (sample to 2018-12). Not a time-series test.
- **Parent result: 12-month time-series momentum in futures.** Sign of the past 12-month return, held one month, long or short, volatility-scaled; alpha about 1.58 percent a month, gross. Source: Moskowitz, Ooi and Pedersen 2012 (sample to 2009-12, no crypto). Not testable here as published; its 12-month lookback has no support in crypto.
- **Unverified leads** (abstract only or not opened; see the notes): Grobys, Ahmed and Sapkota 2020 (20-day moving average on eleven coins, to 2018); Grobys and Sapkota 2019 (a null result on crypto momentum, to 2018); Tzouvanas et al. 2020; Han, Kang and Ryu (sample to 2023-08, overlaps dev: flagged); Deprez and Frömmel 2024 (sample dates unknown: flagged).

## Cross-sectional

Nothing yet.

## Derivatives

Nothing yet.

## Cross-market

Nothing yet.
