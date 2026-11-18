# Research log

A chronological narrative of what was done and why. Results live in the hypothesis files and run records; lessons in `knowhow/`. Newest entries at the bottom.

## 2026-11-18: Phase 1, the research infrastructure

Brief: `briefs/2026-11-18-crypto-research-infrastructure.md`. Goal of the phase: shared infrastructure for rigorous research, proven end to end on one example hypothesis. No strategy is expected from it.

### The Binance archive was checked before anything was built on it

The bucket listing of data.binance.vision was read in full for spot klines and USDT-margined futures. It keeps delisted pairs (253 of 776 USDT pairs have ended), checksums every file, and has funding and basis from 2020-01 and open interest from 2021-12. That is enough for a point-in-time universe, so the work went ahead. Details and limits: `knowhow/binance-archive-coverage.md`.

Looking at gaps and jumps in the daily bars of all pairs turned up things no documentation mentions: a symbol reused for a different coin (LUNA), eight token swaps that changed the unit under the same symbol, about 110 tokenised stocks listed since June 2026, and 43 hourly bars per coin that open 28 minutes past the hour after an outage in 2018. All are handled in the provider or the universe rules: `knowhow/binance-archive-quirks.md`, `knowhow/universe-exclusions-are-curated.md`.

### What was built

- Data: hourly granularity, a Binance archive Provider, datasets with manifests, `trading rebuild`, the point-in-time universe (110 monthly reconstitutions from 2017-10; 363 pairs were ever members; 40 members from 2019-07).
- Engine: vectorised, next-open fills, tiered costs, hold rows; checked against hand-computed cases and a loop, with a mechanical no-look-ahead proof.
- Statistics: nine tools, each validated on synthetic data.
- Process: the split and seal, hypothesis registry, harness, claim ladder, catalogue, and `trading research` commands.
- Four agent definitions and four skills.

### Decisions taken while building, for the owner to confirm

These fill gaps the brief left open. They are listed in the gate report.

1. **Dev replication rule.** A literature candidate is "supported" when its dev estimate has the predicted sign and reaches both half its train estimate and a minimum size declared at registration. No dev p-value is required, because two years cannot deliver one for most trading claims (`knowhow/two-years-cannot-separate-sharpe-ratios.md`).
2. **Two false-discovery controls.** Literature hypotheses are controlled across their train p-values; exploration hypotheses skip train and are controlled across their dev p-values. Untested hypotheses count as p = 1 in their control.
3. **Statuses move.** Candidate status depends on all registered hypotheses and is recomputed each time. A hypothesis that was a candidate when its dev run happened can lose that status later; it then shows as rejected, and its dev run stays on record.
4. **Hold rows in the engine.** A weights row of NaN means "do not trade", so a strategy can rebalance weekly or monthly on daily or hourly bars. The equal-weight benchmark rebalances monthly, at reconstitution.
5. **Id blocks by family** (H1xxx to H4xxx), so parallel Researchers cannot collide.
6. **`research/literature/`** was added to the records layout for the Literature scout's notes.
7. **Open interest is not fetched by default**: about 400,000 small files. Funding and basis are.

### Disclosure: what was seen of the test period

Building the data layer meant handling files from the whole history. Test-period data was touched only as structure, with these exceptions, none of which was used for any choice:

- While checking file formats, the first three rows of BTCUSDT's daily file for 2026-10, of its hourly premium file for 2026-10 and of its metrics file for 2026-10-01 were printed, and one check printed BTC's last two daily bars (2026-10-30 and 31).
- The names (not the prices) of pairs with data-quality flags in the test period were printed, and the count of extreme daily moves after 2024 (six).
- Listing dates of all pairs, including the tokenised stocks of 2026, were read from the archive listing.

No returns, rankings or universe memberships from 2025 on were looked at. Universe construction for the test period ran mechanically and its output was not inspected beyond the number of reconstitutions and members.

### Seen on train while checking the engine

Buy-and-hold BTC from 2017-08 to 2022-12 through the engine: Sharpe 0.72, maximum drawdown -83%. The equal-weight universe rebalanced monthly: Sharpe 0.52, CAGR 2%, maximum drawdown -92%, turnover 2.8 times a year, costs 1.2% a year. These are the benchmarks any trading claim has to beat on train, and they were seen before the example hypothesis was registered; its choice of test did not depend on them (the design was fixed from the literature first), but the reader should know.
