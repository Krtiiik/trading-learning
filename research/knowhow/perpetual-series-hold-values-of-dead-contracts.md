---
title: "Funding and basis hold values that describe no live contract (frozen after delisting, placeholders before listing, the old Luna under the new LUNAUSDT): mask them"
kind: pitfall
area: data
source: "Data steward check on 2026-11-19, train data only (to 2022-12-31): binance/premium/1h id 5dd2d25c086b, binance/funding id 619020e39d56, binance/spot/1h id a7d21dafe920, binance/universe id 88f9a7cf72c7"
trust: high
date: 2026-11-19
---

Three things in the perpetual-futures series are not observations of a market, and each reaches universe members on train.

- **Frozen basis after a contract stops trading.** The archive keeps writing hourly premium bars with the last value, in most cases until 2022-07-12 06:00. Stretches of 24 or more identical hourly closes: 226 on train, 44,236 hours. Inside member-months: ANC at -29.4% (991 hours, June and July 2022), the old Luna at -5.4% (441 hours, May 2022), BTCST at zero from 2021-03-12 (720), LEND at zero (511, October 2020), BTT at zero (408, January 2022), ICP at zero (271, July 2022). In 2020 thin contracts also sit at zero for one to three days while alive (QTUM, ALGO, NEAR, ZIL), which is the premium index's dead band and not an error. A frozen -29% in a cross-section of basis is the largest value by a factor of a hundred.
- **Placeholder funding.** While the basis is frozen at zero or missing, funding is a constant 0.0001: BTCST has 960 payments of exactly 0.0001 from 2022-02-15 to the end of train (61 member-days). 69 contracts also start with payments of exactly 0.0001 stamped before their first premium bar (346 events; CHZ 61, UNFI 55, ALGO 47, ADA 36), several from the 1st of the listing month.
- **The new LUNAUSDT carries the old Luna's contract.** The Store's `LUNAUSDT` (the coin listed 2022-05-31) and `LUNAUSDT-2022` hold the same funding and basis files, those of the contract that died in May 2022: 470 daily funding values dated 2021-01 to 2022-05, before the new coin has a bar, and a basis frozen at -5.4% during its first month as a member (271 hours in July 2022). The new coin's own contract has another symbol in the archive and is not in the Store. This is a defect of the mapping in the provider (reported to the coordinator), not a property of the market.

A mask that removes all of it without looking ahead, for hourly panels on the market's index:

```python
grid = pd.date_range(market.index[0], market.index[-1], freq="1h")
basis = pd.DataFrame(data.series("premium", "1h"), index=market.index).reindex(grid)
frozen = basis.eq(basis.shift(1)).rolling(24, min_periods=24).sum().eq(24)   # unchanged for 24 hours
live = (~frozen & basis.notna()).reindex(market.index).to_numpy() & ~np.isnan(market.close)
```

Use funding and basis only where `live` is true (for daily panels, take `live` at each day's last hourly bar). On train this drops 4,303 of 894,032 member-hours with basis and leaves 185 at 5% or more in size, all real dislocations; it also drops the thin-contract zero stretches of 2020, which carry no information anyway. Requiring a spot bar removes the old Luna's funding from the `LUNAUSDT` column.

Not established: the same count after 2022 (delistings continue, so expect the pattern in dev; apply the mask there too rather than tuning it).
