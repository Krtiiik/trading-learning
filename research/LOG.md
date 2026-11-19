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

### The example hypothesis H1001: Researcher

2026-11-18. One hypothesis, family time-series, origin literature: `hypotheses/H1001-trend-filter-on-daily-bars.md`.

- **Registered first** (commit 68febdf). Each universe member's 1/N slot holds the coin while its close is above its 20-day average, cash otherwise, decided at every daily close; the benchmark is the same slots always filled; the estimate is the difference in net Sharpe ratio from 2019-07-01. The rule and the daily schedule follow Detzel et al.; the literature leaves the lookback at "7 to 28 days" and the schedule open, so 20 days and daily evaluation were stated as choices before anything ran. Predicted +0.25 against a minimum detectable effect of 1.03 on train: registered as underpowered, on purpose. The module was tried on the synthetic Store only (`tests/test_h1001.py`). I had read the two train benchmark figures in the entry above before registering and said so in the file.
- **Train** (H1001-r01): +0.66, p 0.044, q 0.044, +0.48 at double cost. Candidate.
- **Between the runs** I loaded train data once, with a scratch script, because the record's `dropped_weight` of 0.075 was at the edge of a warning sign I had registered without a number. It is three single slots on the day after a pair's last bar. I judged the run sound; the file says plainly that a strict reader may disagree.
- **Dev** (H1001-r02, the one look): +0.12, p 0.42, -0.09 at double cost, against a required +0.33. **Not replicated.** On dev the filter cut volatility and drawdown and gave up return; buy-and-hold BTC did far better than either side.
- **Nothing goes to the Skeptic as a supported finding.** No variant was run and none will be added under this id.
- **What the infrastructure did**: it refused nothing, because nothing was attempted out of order; `check` reported the uncommitted file before the commit and the registration after every later edit; the status moved registered, candidate, not replicated without anyone setting it. What was awkward is in the know-how notes of this date: an unquoted date in the parameters would have broken record writing, `dropped_weight` is cumulative and cannot be taken apart on dev, and the run record has no benchmark figures at double cost (the benchmark's double-cost Sharpe ratio has to be backed out of the estimate).
- **For the owner**: `knowhow/small-sharpe-differences-rarely-climb-the-ladder.md` puts numbers on what the ladder can separate for trading claims on this much data. A true Sharpe difference of 0.25 is supported about one time in nine and a null one time in forty; H1001's path is what either looks like.

### The example hypothesis H1001: Skeptic

2026-11-19. An audit, because H1001 is `not replicated` and not `supported`: verdict `audited`, no status changed. The review is the "Skeptic review" section of `hypotheses/H1001-trend-filter-on-daily-bars.md`; every number of every attack stays there.

- **How it was done.** Registration, run records, experiment module and the library code first; the Researcher's Results, Verdict and log entry only after the result had been re-derived. Train data only. Dev was not loaded and cannot be; its numbers are quoted from H1001-r02.
- **The train result is not an artefact.** `replay` reproduces H1001-r01 to the last digit, and a loop that holds units and cash and shares no code with the engine gives +0.6612 against the record's +0.6611. No input of the panel, the benchmark or the membership is known later than the bar's close. The nine checks of the review skill found no lucky parameter, no single year, no handful of coins, no dependence on cost or on the instant of execution; the one weak check is that much of the gain sits on a few crash days, which is what the standard error of 0.38 already says.
- **The status is sound.** Registration precedes both runs, the experiment has one commit, no library code changed before the dev run, dev ran once, the dataset ids match `trading verify`, and 0.124 is below the required 0.331.
- **Neither run settles the question.** One hypothesis through a one-sided 10% gate, with a train estimate equal to what a null that passes the gate averages; a dev rule that a true effect of the predicted size fails more often than it passes. "Not replicated" means the rule was not met.
- **The three points the Researcher flagged.** The dropped weight of 0.075 does not void the train run: three last-bar slots that change no return, against a criterion no daily rule on this universe could be sure to meet (the registered benchmark drops 0.175 in the same window). The look at train data between the runs does not compromise the dev run, though the script was not kept and cannot be checked. The daily benchmark was a legitimate, registered choice that accounts for a fifth of the train estimate; against the monthly reference the hypothesis would still have been a candidate.
- **Infrastructure, for whoever maintains it.** `dropped_weight` changed meaning in commit b74ae59 without a new `harness_version`, so the two H1001 records carry the old meaning unmarked. The bootstrap's automatic block length jumps between near-identical series and moves the p-value. The harness's look-ahead check truncates bars but not the universe table. The review skill's check 4 points at return series that run records do not hold. Nothing in `src/` was touched.
- **Know-how added**: the bootstrap p-value as a range, placebo tools on the point-in-time universe, crash days judged against a placebo, the engine against an independent loop, and additions to the notes on dropped weight and on the correlation with the benchmark.
