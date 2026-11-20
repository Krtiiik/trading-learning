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

### Phase 1 at the gate

2026-11-19. Written by the coordinating session. Phase 1 stops here and waits for the owner; Phase 2 has not started.

**What the example proved about the infrastructure.** One hypothesis went from published evidence to a reviewed verdict with four agents that each read only their definition, the skills and the records: the Literature scout supplied the motivation, the Data steward answered for the data, the Researcher registered, ran and wrote the verdict without asking anyone, the Skeptic re-derived the result with a loop that shares no code with the engine (+0.6612 against the recorded +0.6611). The ladder moved H1001 from registered to candidate to not replicated without anyone setting a status, and the seal stayed closed.

**What the example changed in the infrastructure.** Each of these came from an agent's report and was fixed by the coordinating session with a test:

- A date among a hypothesis's parameters would have broken the run record after the test had run.
- Run records now hold the benchmark at double cost and the dropped weight of the evaluated window. `harness_version` is 2 from here on; the two H1001 records are version 1, where `dropped_weight` was summed from the first bar of the data.
- A review of a hypothesis that is not supported is recorded as `audited`.
- A strategy that buys a coin outside the point-in-time universe is refused.
- A hypothesis can declare the first day of its evaluation, and research can read the ETF bars under the seal.
- Hourly bars that do not open on the hour are dropped by the provider.

**Left open on purpose, for the owner.** These would change how evidence is judged, so they were not changed after H1001 had run:

1. The dev rule's `min_ratio` of 0.5. With H1001's standard errors a true Sharpe difference of 0.25 becomes supported about one time in nine, and a null one time in forty (`knowhow/small-sharpe-differences-rarely-climb-the-ladder.md`).
2. The bootstrap's automatic block length. It jumps between near-identical series (9 or 22 bars) and moves the p-value by about a third (`knowhow/bootstrap-p-value-moves-with-block-length.md`). A block length fixed by rule or declared at registration would be steadier.
3. Renamed coins restart as new pairs, and the universe's exclusions are a hand-made list.
4. Open interest is not in the Store yet.

**Not covered by any check.** The harness's look-ahead check recomputes an experiment's panel on truncated bars; it does not rebuild the universe table. That the universe uses no later data rests on the Data steward's recomputation of all 63 train reconstitutions and on the unit tests, not on the per-run check.


Overnight session 2026-11-17 → 2026-11-18. One entry per experiment, appended as I go.

Conventions for every experiment unless stated otherwise:

- Universe: the 25 ETFs in `universe.toml`. Data: Yahoo daily bars fetched into this worktree's
  `data/` with `uv run trading fetch` on 2026-11-17 (the worktree had no data, it is gitignored).
- Sealed holdout: 2024-11-17 onward. All research code loads through `research/common.py`, which
  truncates at 2024-11-16. Only `research/holdout.py` may read past it, once, at the end.
- Evaluation window: 2005-01-03 .. 2024-11-15 (19.9 years). By 2005 the bond, gold and REIT
  ETFs exist; later listings (SLV, DBC 2006, HYG 2007, XLRE 2015, XLC 2018) join when they have bars.
- Account: $10,000, fractional shares, no commission, 5 bps per side (the pessimistic end of the
  brief), cash earns 0%. Signal on the close of day t, fill at the raw open of day t+1.
- Sharpe uses a zero risk-free rate. Turnover is one-way per year.
- Trial count is tracked at the bottom of this file, to be honest about multiple testing.

---

## E00 — Backtester and data check

**Hypothesis.** The engine's accounting matches known quantities on real data.

**Setup.** `research/e00_data_check.py`. Buy and hold SPY 2005 → seal in the engine, three ways.

**Result.**

- No interior gaps in any of the 25 symbols; no missing opens. Four overnight gaps above 15%
  (XLF 2008-09-19, XLE 2020-03-09, XLB and XLF 2020-03-16): all real market events.
- SPY total return: engine with daily reinvestment 6.075 vs adjusted close 6.071 (the 0.07%
  gap is reinvesting at the next open instead of the ex-date close). Price-only is 3.869 and
  dividends-kept-as-cash 4.543, so dividends are accounted for correctly.

- 60/40 SPY/IEF rebalanced at every close with no costs: engine $46,339 vs compounding
  0.6·r_SPY + 0.4·r_IEF on adjusted closes by hand $46,323 (0.03% apart; added later in
  the night as an independent cross-check of rebalancing).

**Verdict.** Engine is trustworthy. 30 unit tests cover the accounting, the cost model, the
t+1 lag, dividends and late listings; each rule has a truncation test proving no look-ahead.

---

## E01 — Baselines

**Hypothesis.** None; these set the bar. Parameters are the textbook ones, not tuned.

**Setup.** `research/e01_baselines.py`.

**Result (5 bps, fill at next open).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY buy & hold | 59,860 | 3,015 | 10.3% | 19.1% | 0.61 | -55.2% | 0.0x | 9 |
| Equal weight (1/N) | 42,918 | 2,162 | 8.8% | 14.8% | 0.64 | -41.9% | 0.8x | 387 |
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| TSMOM 12m, 1/N | 23,032 | 1,160 | 6.2% | 8.8% | 0.73 | -15.6% | 3.3x | 1,295 |
| SPY>SMA200 else IEF | 29,848 | 1,503 | 7.2% | 12.4% | 0.62 | -27.3% | 5.8x | 2,154 |
| SPY>SMA200 else cash | 28,928 | 1,457 | 7.1% | 11.6% | 0.65 | -24.4% | 2.9x | 1,029 |
| RSI2 pullback SPY | 5,843 | 294 | 2.3% | 6.4% | 0.40 | -15.0% | 8.1x | 1,977 |
| XS 5d reversal, 5 worst | 19,672 | 991 | 5.6% | 20.1% | 0.37 | -49.1% | 89.8x | 36,338 |

Sharpe by sub-period (5 bps):

| strategy | 2005-09 | 2010-14 | 2015-19 | 2020-24 |
|---|---:|---:|---:|---:|
| SPY buy & hold | 0.13 | 0.98 | 0.88 | 0.76 |
| Equal weight (1/N) | 0.39 | 0.92 | 0.87 | 0.66 |
| 60/40 SPY/IEF | 0.28 | 1.38 | 1.09 | 0.70 |
| TSMOM 12m, 1/N | 0.68 | 0.95 | 0.66 | 0.59 |
| SPY>SMA200 else IEF | 0.47 | 0.65 | 0.68 | 0.71 |
| SPY>SMA200 else cash | 0.37 | 0.68 | 0.63 | 0.87 |
| RSI2 pullback SPY | 0.44 | 0.38 | 0.18 | 0.62 |
| XS 5d reversal, 5 worst | 0.58 | 0.36 | -0.01 | 0.41 |

**Observations.**

- "A few hundred dollars a year on $10k" is a low bar in absolute terms: every baseline clears
  it, and plain SPY made about $3,000/yr (compounded, so back-loaded). The honest question is
  therefore whether anything beats the passive baselines per unit of risk, not whether it
  makes money.
- Passive mixes are hard to beat: 60/40 has the best Sharpe (0.75) at 0.5x turnover.
- 12-month TSMOM matches it on Sharpe (0.73) with a third of the drawdown (-15.6% vs -31.6%),
  but earns less in dollars because about 40% of the account sits in cash earning nothing.
- The SMA200 switch on SPY does not beat buy and hold on Sharpe here; it halves drawdown.
  Daily checking whipsaws: 5.8x turnover and $2,154 of costs for the IEF version.
- Mean reversion is the cost story: the cross-sectional 5-day reversal earns Sharpe 0.82 at
  zero cost, 0.64 at 2 bps, 0.37 at 5 bps, and 0.24 if filled at the next close instead of
  the next open. 90x turnover; $36k of costs on a $10k account. Its edge also decays by
  sub-period (0.58 → 0.36 → -0.01 → 0.41). RSI-2 on SPY is alive but small (Sharpe 0.40) and
  in the market only a fraction of the time.

**Verdict.** Bar to beat after costs: Sharpe ≈ 0.75 (60/40) or ≈ 0.73 with maxDD ≈ -16% (TSMOM).

**Next.** Literature review (E02 notes), then candidates that the evidence supports.

---

## E02 — Literature review (web research by a sub-agent, sources in its report)

Not an experiment; recorded because it decides what gets tried. Summary of what the evidence
says for this exact setup (daily bars, long-only, t+1, 2–5 bps):

- **Slow trend following** (Faber 10-month SMA, MOP time-series momentum) is the best supported
  family. Realistic expectation Sharpe 0.5–0.7 and lagging SPY in bull markets. The more
  parameters (GEM, ADM, VAA/DAA) the worse the post-publication decay.
- **Short-term mean reversion** (IBS, RSI-2, 1–5 day reversal) has decayed since about 2015 and
  is measured entering at the signal close; a t+1 entry removes much of it. Fragile.
- **Volatility targeting** reliably cuts tail risk and gives a small Sharpe gain on equity and
  credit only (Harvey et al. 2018; Barroso-Detzel 2021: only the vol-managed market survives
  costs). Without leverage it can only de-risk.
- **Calendar effects**: turn-of-the-month is old and cheap but has thin recent evidence;
  overnight anomaly and pre-FOMC drift are dead after costs; TLT month-end is vendor evidence.
- **Sector momentum** on SPDRs: weak, short sample, equity-like drawdowns.
- **RL / deep learning**: no independent replication beating 1/N after costs; results swing
  with the random seed (one project: test Sharpe +0.86 to -0.32 across seeds); FinRL's own
  authors name backtest overfitting as a core problem. Zhang-Zohren-Roberts (2020) report
  Sharpe 1.4 at 10 bps on four ETFs, but in one bull window and with VIX as an "asset".
  Simplest defensible setup: a small direct-policy model, walk-forward, many seeds, treated
  as a likely negative result.
- **Pitfalls**: log every trial (deflated Sharpe); Yahoo opens are lower quality than closes.

Sub-agent's picks: (1) trend-filtered inverse-vol asset-class core with a no-trade band,
(2) a portfolio-level volatility cap, (3) a small turn-of-month tilt.

---

## E03 — Rule candidates from the literature

**Hypothesis.** (a) Inverse-vol sizing and a no-trade band improve plain TSMOM; (b) a
volatility cap improves equity-heavy passive mixes after costs (Harvey et al. 2018);
(c) turn-of-month on SPY survives 5 bps.

**Setup.** `research/e03_candidates.py`. Seven configurations written down before running:
12-month lookback, 60-day vol for sizing, 5% no-trade band (skip the day's rebalance if it
would move ≤5% of equity one way), caps of 12% on SPY (20-day), 10% on 1/N (60-day), 8% on
60/40 (20-day), turn-of-month holding the last session and first three of each month.

**Result (5 bps, fill at next open).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TSMOM 12m, 1/N + band | 23,519 | 1,185 | 6.3% | 8.8% | 0.73 | -15.8% | 1.5x | 599 |
| InvVol trend | 19,114 | 963 | 5.5% | 7.1% | 0.79 | -14.3% | 3.8x | 1,389 |
| InvVol trend + band | 18,610 | 937 | 5.4% | 7.2% | 0.78 | -15.0% | 2.1x | 786 |
| SPY vol cap 12% + band | 43,106 | 2,171 | 8.8% | 11.5% | 0.79 | -28.7% | 0.9x | 388 |
| 1/N vol cap 10% + band | 26,932 | 1,357 | 6.8% | 9.7% | 0.73 | -21.1% | 0.3x | 120 |
| 60/40 vol cap 8% + band | 28,290 | 1,425 | 7.0% | 7.3% | 0.97 | -17.3% | 0.8x | 302 |
| Turn of month SPY (-1,+3) | 1,289 | 65 | 0.6% | 8.0% | 0.12 | -24.6% | 12.0x | 2,313 |

**Observations.**

- (a) Inverse-vol sizing lifts TSMOM from Sharpe 0.73 to 0.79, mostly by lowering vol. The
  band halves turnover and cost but does not change Sharpe: costs were never the problem for
  slow trend. About a quarter of the account sits in cash at 0%. Its latest sub-period is
  its weakest (0.44–0.54 in 2020-24).
- (b) The cap helps every mix it was put on: SPY 0.61 → 0.79, 1/N 0.64 → 0.73, 60/40
  0.75 → 0.97. It works by cutting exposure in 2008, 2020 and 2022; it gives up return in
  calm bull years. It lowers dollars earned and lowers drawdown more.
- (c) Turn-of-month fails: Sharpe 0.12 at 5 bps, 0.21 at 2 bps. Twelve round trips a year
  cost 1.2% against an edge of about 1.8%. Two of four sub-periods are negative.
- Next-close fills change nothing for the slow rules (Sharpe within 0.02).

**Verdict.** Volatility-capped 60/40 is the first candidate that clearly beats the passive
bar on Sharpe and drawdown. Turn-of-month is dropped. Trend stays as a diversifier candidate.

---

## E04 — Is the capped 60/40 a plateau or a lucky setting?

**Hypothesis.** If the effect is real, neighbouring targets, windows, bands and other mixes
show it too. This is a sensitivity check, not a search: the E03 setting (8%, 20-day, 5% band)
stays the candidate whatever the neighbours score.

**Setup.** `research/e04_volcap_sensitivity.py`. 6 target×window cells, 4 bands, close fill,
10 bps, and the same cap on four other passive mixes.

**Result (5 bps).**

| 60/40 cap | Sharpe | CAGR | maxDD | turnover |
|---|---:|---:|---:|---:|
| 6%, 20d | 0.95 | 5.8% | -14.4% | 1.1x |
| 6%, 60d | 0.89 | 5.6% | -12.8% | 0.4x |
| **8%, 20d** | **0.97** | 7.0% | -17.3% | 0.8x |
| 8%, 60d | 0.88 | 6.6% | -16.5% | 0.3x |
| 10%, 20d | 0.91 | 7.3% | -19.6% | 0.5x |
| 10%, 60d | 0.86 | 7.1% | -20.1% | 0.2x |
| uncapped | 0.75 | 7.9% | -31.6% | 0.5x |

Band 0 / 2 / 5 / 10%: Sharpe 0.96 / 0.96 / 0.97 / 0.93. Close fill 0.95. At 10 bps 0.96.

Same cap on other mixes (uncapped → capped Sharpe; maxDD):

| mix | Sharpe | maxDD |
|---|---|---|
| 60/40 SPY/TLT | 0.78 → 0.95 | -30.2% → -18.0% |
| 40/60 SPY/IEF | 0.87 → 0.99 | -19.7% → -15.9% |
| SPY/IEF/GLD thirds | 0.92 → 0.98 | -20.8% → -15.1% |
| six-asset 1/N (SPY EFA IEF LQD GLD VNQ) | 0.66 → 0.79 | -33.4% → -17.1% |

Yearly, 60/40 vs capped: 2008 -16.8% vs -10.0%; 2020 +16.4% vs +9.0%; 2022 -16.5% vs -11.7%;
2019 +21.7% vs +18.2%; 2023 +16.9% vs +13.3%.

**Observations.**

- A plateau: every cell beats the uncapped mix (0.86–0.97 vs 0.75) and every mix improves.
  The E03 setting happens to be the best cell, so expect something nearer 0.9 than 0.97.
- The whole gain is in the crisis sub-periods (2005-09: 0.28 → 0.52; 2020-24: 0.70 → 0.86);
  in 2010-19 capped and uncapped are the same. It is crash insurance, not alpha, and it
  cost about 0.9 points of CAGR over the window. It missed part of the 2020 rebound.
- The base mix matters as much as the cap: 60/40 itself rode a 2005-2020 bond bull market
  with stocks and bonds negatively correlated. 2022 shows what happens when that breaks
  (-16.5% uncapped, -11.7% capped).
- Costs are irrelevant at this turnover (0.8x): doubling to 10 bps moves Sharpe by 0.01.

**Verdict.** Robust to its own parameters; regime-dependent through its base mix. Strong
finalist candidate. The dollars: about $1,400/yr on $10k (7.0% CAGR), less than uncapped
60/40 ($1,770/yr) or SPY ($3,015/yr), at about half the drawdown.

---

## E05 — Blend, idle cash, and a significance check

**Hypothesis.** (a) Blending trend with the capped mix diversifies; (b) parking trend's idle
cash in IEF (while IEF's own 12-month return is positive) removes the 0% cash drag;
(c) the Sharpe gains over 60/40 are larger than resampling noise.

**Setup.** `research/e05_blend_and_significance.py`. Three new configurations, pre-specified.
Paired circular block bootstrap of daily returns (20-day blocks, 2000 draws).

**Result (5 bps).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| InvVol trend + band | 18,610 | 937 | 5.4% | 7.2% | 0.78 | -15.0% | 2.1x | 786 |
| Capped 60/40 | 28,290 | 1,425 | 7.0% | 7.3% | 0.97 | -17.3% | 0.8x | 302 |
| Blend 50/50 trend + capped | 23,325 | 1,175 | 6.3% | 6.9% | 0.91 | -12.6% | 1.1x | 417 |
| Trend, idle cash in IEF | 22,026 | 1,109 | 6.0% | 7.6% | 0.81 | -15.8% | 3.5x | 1,412 |
| Trend-parked, cap 8% | 19,037 | 959 | 5.5% | 6.8% | 0.83 | -14.7% | 3.9x | 1,469 |

Bootstrap of Sharpe differences (observed, 90% interval, share of draws ≤ 0):

| pair | diff | 90% interval | P(≤0) |
|---|---:|---|---:|
| Capped 60/40 − 60/40 | +0.22 | [+0.05, +0.37] | 0.01 |
| Capped 60/40 − SPY | +0.36 | [+0.18, +0.54] | 0.00 |
| InvVol trend − 60/40 | +0.03 | [−0.24, +0.28] | 0.44 |
| Blend − 60/40 | +0.16 | [−0.03, +0.35] | 0.09 |
| Blend − Capped 60/40 | −0.06 | [−0.16, +0.05] | 0.80 |
| Trend, idle in IEF − 60/40 | +0.06 | [−0.22, +0.33] | 0.36 |

**Observations.**

- (a) The blend does not diversify much: trend and the capped mix correlate 0.84 (both are
  long risk assets when calm). Sharpe 0.91, but the smallest drawdown so far (-12.6%).
- (b) Parking idle cash in IEF adds 0.6 points of CAGR and 0.03 Sharpe: marginal.
- (c) Trend is statistically indistinguishable from 60/40. The capped mix's edge over its
  own uncapped base is the only difference whose 90% interval excludes zero. That p-value
  is not corrected for it being the best of ~10 rule candidates, so read it as "probably
  real, size uncertain" (the interval runs from +0.05 to +0.37).
- All trend variants are weakest in 2020-24 (Sharpe ≈ 0.45).

**Verdict.** Capped 60/40 remains the leading candidate. Trend and the blend are not better.

---

## E06 — Supervised return prediction (ridge, gradient boosting)

**Hypothesis.** A model that sees nine per-ETF features (four momentum horizons, 5-day
reversal, distance from the 200-day average, vol ratio, vol level, IBS) predicts 5-day
returns well enough to pick ETFs after costs.

**Setup.** `research/e06_supervised.py`, specification fixed before the first run and in the
file's docstring. 135,588 samples; 20 yearly folds with an expanding window and a 5-session
embargo; Ridge(alpha=100) and HistGradientBoosting (depth 3, 200 trees), no tuning. Portfolio:
top 5 predictions at 20% each if positive, averaged over the last 5 days' picks, 5% band.
New dependencies: scikit-learn, torch (dev group).

**Result.**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ridge top-5, 5 bps | 17,034 | 858 | 5.1% | 12.8% | 0.46 | -30.8% | 33.6x | 12,239 |
| GBM top-5, 5 bps | 16,009 | 806 | 4.9% | 14.5% | 0.40 | -38.2% | 29.9x | 10,756 |
| Ridge top-5, 0 bps | 42,053 | 2,118 | 8.7% | 12.8% | 0.71 | -30.4% | 34.0x | 0 |
| GBM top-5, 0 bps | 36,764 | 1,852 | 8.1% | 14.5% | 0.61 | -37.3% | 30.0x | 0 |

Out-of-sample daily rank IC: ridge +0.014 (t ≈ 1.3), GBM +0.021 (t ≈ 2.2); positive in all
four 5-year blocks for both. Ridge's largest coefficients are short-term reversal (rev_5
−0.035, IBS −0.019): the model mostly rediscovered mean reversion.

**Observations.**

- There is a small, real, persistent signal (IC ≈ 0.02), and it is the short-term reversal
  effect E01 already showed. It is not big enough: even at zero cost the portfolio only
  matches 1/N (Sharpe 0.61–0.71 vs 0.64), and at 5 bps the 30x turnover takes $11–12k.
- Both models are weakest in 2020-24 (Sharpe 0.15–0.26).

**Verdict.** Fails. Not pursued further: making it trade less would mean tuning the
portfolio rule on the same data, and the zero-cost ceiling is not worth reaching for.

---

## E09 — The capped 60/40 on 1994-2004, a period nothing here had touched

(Run while E07 trained; numbered by start time.)

**Hypothesis.** Written down before running: on a decade outside the walk-forward window,
the cap again raises Sharpe and cuts drawdown versus the uncapped mix.

**Setup.** `research/e09_pre2005_check.py`. IEF starts in 2002, so the bond leg is VFITX
(Vanguard Intermediate-Term Treasury fund; daily NAV from Yahoo via
`uv run trading fetch --symbols VFITX --data-dir data/extra`, fetched 2026-11-17). Mutual
funds trade at closing NAV, so fills are at the next close. Same parameters as E03.

**Result (5 bps, next-close fill).**

| 1994-2004 | net P&L $ | CAGR | vol | Sharpe | maxDD |
|---|---:|---:|---:|---:|---:|
| SPY buy & hold | 21,182 | 10.9% | 18.4% | 0.65 | -47.5% |
| 60/40 SPY/VFITX | 17,435 | 9.6% | 11.2% | 0.88 | -24.4% |
| Capped 60/40 SPY/VFITX | 10,567 | 6.8% | 8.0% | 0.86 | -22.1% |

Capped − uncapped Sharpe: −0.02, 90% interval [−0.14, +0.10].

Proxy check on 2005 → seal with VFITX in place of IEF: 60/40 0.74, capped 0.91
(difference +0.17, interval [+0.02, +0.32]). That matches the IEF version (0.75 → 0.97
with next-open fills), so the proxy is sound and the 1994-2004 result is not a proxy artefact.

Yearly: the cap gave up 1997 (+14.3% vs +23.6%), 1998 (+13.8% vs +21.9%) and 1999 (+7.5%
vs +10.5%), when volatility was high in a rising market, and saved almost nothing in the
slow 2000-02 bear market (2001: −7.9% vs −3.9%; 2002: −7.9% vs −8.0%).

**Verdict.** The hypothesis failed. Outside the window the cap bought no Sharpe, a
2-point smaller drawdown, and cost 2.8 points of CAGR. Its 2005-2024 edge comes from two
fast crashes (2008, 2020) where volatility rose before most of the loss. In a slow bear
market or a volatile bull market it is a drag. Over the two periods together the cap is a
risk dial, not a source of return: Sharpe roughly equal to or better than uncapped,
never clearly worse, at lower volatility and lower dollars.

This is the most important check of the night: the leading candidate's advantage over
plain 60/40 is regime-dependent and should not be expected to persist at its 2005-2024 size.

---

## E07 — Direct policy optimisation (the simplest "RL")

**Hypothesis.** A small policy that maps each ETF's nine features to a score, with softmax
weights over the listed ETFs plus cash, trained by gradient ascent on net-of-cost Sharpe,
finds an allocation rule that beats the hand-written ones out of sample.

**Setup.** `research/e07_direct_policy.py`, specification fixed before the first run (in the
docstring): linear and MLP (9→8→1) policies, Adam lr 0.01, 300 epochs, 20 yearly folds
with an expanding window from 2000, 5 seeds each, evaluated in the real engine with a 5%
band. CPU only (each training takes about a second; the GPU was not needed all night).

**Result (5 bps).**

| policy | Sharpe by seed | ensemble Sharpe | ensemble CAGR | maxDD | turnover | ensemble Sharpe at 0 bps |
|---|---|---:|---:|---:|---:|---:|
| linear | 0.28, 0.32, 0.24, 0.22, 0.29 | 0.30 | 2.7% | -29.0% | 26.8x | 0.59 |
| MLP | −0.15, −0.12, 0.02, 0.23, 0.12 | 0.15 | 1.1% | -30.7% | 59.2x | 0.71 |

Ensemble Sharpe by sub-period: linear 0.39 / 0.14 / 1.14 / 0.37; MLP 0.44 / −0.18 / 0.39 / −0.20.

**Why it fails** (`research/e07_diagnostic.py` and a per-year look at linear seed 0):

- Overfitting, visible directly. Trained on 2000-2019, the MLP scores net Sharpe 1.9–2.2
  in sample and −0.36 to +0.08 on 2020-24. The linear policy scores 0.90 in sample and
  0.33 out.
- Two regimes of failure for the linear policy. With training windows up to 2014 it
  learns a concentrated, twitchy rule: 58–136x turnover a year, largest weight 30–48%.
  From the 2015 fold on it collapses to a diffuse rule: 60–75% cash, largest weight 5%,
  about 1x turnover, earning −4% to +8% a year. Maximising Sharpe with a cash slot rewards
  doing very little.
- Seed variance for the MLP spans −0.15 to +0.23: the seed matters more than the model.
- The learned average holdings are bonds and defensive sectors (IEF, LQD, TLT, HYG, GLD,
  XLP, XLV): the policy learned "low volatility had high Sharpe in the training window".

**Verdict.** Fails, for the reasons the literature predicted. Not tuned further.

---

## E10 — What holding the leading candidate would have felt like

No new configurations. `research/e10_finalist_diagnostics.py`, walk-forward window, 5 bps.

| | SPY | 60/40 | Capped 60/40 |
|---|---:|---:|---:|
| worst rolling 12 months | -47.4% | -27.4% | -13.8% |
| median rolling 12 months | +14.1% | +10.0% | +8.5% |
| best rolling 12 months | +77.5% | +39.4% | +23.9% |
| 12-month windows that lost money | 18% | 14% | 14% |
| losing calendar years (of 20) | 3 | 3 | 3 |
| longest time under water (trading days) | 1,223 | 699 | 611 |
| deepest drawdown in dollars | -13,398 | -8,571 | -4,699 |
| lowest equity from a $10k start | 6,050 | 8,551 | 9,691 |

- Rolling 3-year Sharpe: the capped mix is ahead of plain 60/40 on 77% of days, but the
  median gap is only +0.08; ahead of SPY on 90% of days (median +0.30).
- The cap is binding most of the time: fully invested on 31% of days, 86% invested on
  average, under 50% invested on 8% of days.
- Calendar-year P&L of the capped mix on the compounding account ranges from −$4,002
  (2022, on about $34k) to +$4,254 (2019). In the first five years, on about $10–11k, it
  made +337, +1,052, +677, −1,212, +1,093.

**Verdict.** A smoother ride, not a richer one: same number of losing years as 60/40, about
half the worst loss, about 85% of the median gain.

---

## E11 — How much of each rule's profit is more than stock and bond exposure?

**Question.** Every rule made money because markets went up. How many dollars a year did
each earn beyond a static SPY/IEF mix with the same average exposure?

**Setup.** `research/e11_alpha.py`. No new configurations. Daily net returns (5 bps)
regressed on buy-and-hold SPY and IEF returns; the intercept is alpha. Newey-West t (20 lags).

| rule | β SPY | β IEF | alpha %/yr | alpha $/yr on $10k | t | R² |
|---|---:|---:|---:|---:|---:|---:|
| Equal weight (1/N) | 0.77 | 0.23 | -0.2% | -20 | -0.24 | 0.93 |
| 60/40 SPY/IEF | 0.60 | 0.40 | -0.1% | -9 | -2.75 | 1.00 |
| TSMOM 12m, 1/N | 0.33 | 0.09 | 2.3% | 225 | 1.63 | 0.49 |
| SPY>SMA200 else IEF | 0.34 | 0.30 | 2.8% | 279 | 1.17 | 0.25 |
| RSI2 pullback SPY | 0.11 | -0.04 | 1.4% | 139 | 1.22 | 0.11 |
| XS 5d reversal, 5 worst | 0.88 | 0.30 | -3.7% | -371 | -1.44 | 0.65 |
| Turn of month SPY | 0.18 | -0.02 | -1.1% | -110 | -0.74 | 0.19 |
| InvVol trend + band | 0.27 | 0.18 | 1.8% | 180 | 1.55 | 0.47 |
| Capped 60/40 | 0.36 | 0.27 | 2.0% | 202 | 2.71 | 0.79 |
| Blend trend + capped | 0.31 | 0.23 | 1.9% | 189 | 2.26 | 0.68 |

**Observations.**

- This is the sharpest answer to the brief. The timing rules (trend, cap) each earned
  roughly $140–280 a year on $10k beyond their market exposure: "a few hundred dollars",
  as asked. Only the capped mix and the blend have t above 2, and those t-values are in
  sample, uncorrected for ~25 configurations tried, and E09 showed the cap's alpha was
  about zero in 1994-2004.
- The rest of each rule's profit (the larger part) is plain exposure to stocks and bonds,
  which a static mix gives for free. 60/40 daily rebalanced has alpha −$9: that is its
  trading cost.
- The fast rules have negative alpha after costs (reversal −$371, turn-of-month −$110).

**Verdict.** There may be a small timing edge of the order of $200 a year on $10k in slow
risk-management rules. It cannot be distinguished from luck with confidence on 20 years.

---

## E12 — Relative momentum (sector rotation, dual momentum)

(Run while E08 trained.)

**Hypothesis.** The two textbook relative-momentum rules beat the passive bar. The
literature review expected them not to (post-publication decay, equity-like drawdowns).

**Setup.** `research/e12_relative_momentum.py`. Two configurations, each run once: the top 3
SPDR sectors by 12-month return (a slot only while its own return is positive, else cash);
SPY or EFA by 12-month return if positive, else IEF. Checked daily, 5% band.

**Result (5 bps).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sector top-3, 12m | 36,425 | 1,835 | 8.0% | 16.2% | 0.56 | -28.0% | 13.1x | 5,685 |
| Dual momentum SPY/EFA else IEF | 17,841 | 899 | 5.3% | 15.0% | 0.42 | -40.4% | 8.1x | 2,637 |

Sharpe by sub-period: sectors 0.34 / 0.86 / 0.38 / 0.61; dual momentum 0.25 / 0.56 / 0.45 / 0.42.

**Observations.** Both are worse than holding SPY (0.61) on Sharpe. Checking a ranking
daily makes it flip between near-tied candidates (8–13x turnover), and concentrating in
one or three equity funds keeps equity-size drawdowns. Dual momentum switched late in
2008 and was whipsawed afterwards.

**Verdict.** Fails, as the review predicted. Dropped.

---

## E08 — PPO allocation agent (stable-baselines3)

**Hypothesis.** A standard RL agent allocating daily between SPY, IEF, GLD and cash beats
the fixed mixes of the same assets out of sample after costs.

**Setup.** `research/e08_ppo.py`, specification fixed before the first run (docstring):
observation = 9 features × 3 assets + current weights; action → softmax weights; reward =
100·log(1 + net return) with 5 bps on weight changes; 252-day episodes from random starts;
PPO defaults, MLP 2×32, 150,000 steps per fold; four expanding walk-forward folds testing
2012-14, 2015-17, 2018-20, 2021-24; 5 seeds. New dependencies: gymnasium, stable-baselines3.
CPU only: 5 seeds in parallel took 5.4 minutes in total.

**Result (2012-01-03 .. seal, 5 bps, next-open fill, 5% band).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PPO seed 0 | -3,926 | -305 | -3.8% | 13.2% | -0.23 | -56.5% | 32.7x | 2,914 |
| PPO seed 1 | -2,771 | -215 | -2.5% | 13.1% | -0.13 | -49.2% | 41.7x | 3,816 |
| PPO seed 2 | 2,403 | 187 | 1.7% | 11.4% | 0.20 | -30.1% | 44.8x | 5,768 |
| PPO seed 3 | -976 | -76 | -0.8% | 12.4% | -0.00 | -40.9% | 43.1x | 4,603 |
| PPO seed 4 | -1,840 | -143 | -1.6% | 12.1% | -0.07 | -45.7% | 50.5x | 5,203 |
| PPO ensemble | -50 | -4 | -0.0% | 11.2% | 0.05 | -36.5% | 29.8x | 3,279 |
| PPO ensemble, 0 bps | 4,622 | 360 | 3.0% | 11.2% | 0.32 | -22.1% | 29.6x | 0 |
| SPY/IEF/GLD thirds | 12,978 | 1,009 | 6.7% | 8.1% | 0.84 | -16.8% | 0.6x | 112 |
| 60/40 SPY/IEF | 21,602 | 1,680 | 9.4% | 9.7% | 0.97 | -21.1% | 0.5x | 123 |
| Capped 60/40 | 17,380 | 1,352 | 8.1% | 7.1% | 1.14 | -13.7% | 0.7x | 170 |
| SPY buy & hold | 47,786 | 3,717 | 14.6% | 16.5% | 0.91 | -33.7% | 0.0x | 8 |

**Observations.**

- Four of five seeds lost money over thirteen years in which all three assets rose. The
  seed-averaged agent broke even. Holding the same three assets in fixed thirds made
  $12,978 with a Sharpe of 0.84.
- Costs are not the reason: at zero cost the ensemble's Sharpe is 0.32.
- The agent learned the recent past. Its first fold, trained on 2005-2011 (gold's bull
  market), held 67% gold in 2012 and 53% in 2013, the year gold fell 28%. It then moved to
  65% SPY for 2015 and back down to 24% by 2018.
- It trades 30–50x a year despite the cost term in its reward and the 5% band.
- Seed spread −0.23 to +0.20: no single run means anything.

**Verdict.** Fails clearly, and in the way the literature warned: about 1,500 training days
per fold of three noisy return series is far too little for an agent to learn anything but
the last regime. RL is not the right tool for this problem at this data scale.

---

## E13 — A trend switch on the stock leg, plus the cap

**Hypothesis.** E09 showed the cap adds nothing in a slow bear market. Trend rules are
meant for exactly that regime, and the cap for fast crashes, so the two together should be
at least as good as the cap alone in the walk-forward window and better on 1994-2004.

**Setup.** `research/e13_trend_switch_cap.py`. One configuration, written down before
running: 60% SPY only while SPY's 12-month return is positive (else that 60% is cash), 40%
IEF always, then the same 8% / 20-day cap and 5% band. The rule is
`rules.trend_switched_mix` followed by `rules.volatility_cap`.

**Result (5 bps).**

| 2005 .. seal, next-open fill | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| Capped 60/40 | 28,290 | 1,425 | 7.0% | 7.3% | 0.97 | -17.3% | 0.8x | 302 |
| Trend-switched 60/40 | 26,437 | 1,332 | 6.7% | 7.9% | 0.86 | -17.7% | 1.1x | 450 |
| Trend-switched + capped | 23,830 | 1,200 | 6.3% | 6.6% | 0.96 | -13.6% | 1.5x | 570 |

Sharpe by sub-period:

| | 2005-09 | 2010-14 | 2015-19 | 2020-24 |
|---|---:|---:|---:|---:|
| 60/40 | 0.28 | 1.38 | 1.09 | 0.70 |
| Capped 60/40 | 0.52 | 1.44 | 1.12 | 0.86 |
| Trend-switched + capped | 0.75 | 1.35 | 0.91 | 0.82 |

| 1994-02 .. 2004, VFITX, next-close fill | net P&L $ | CAGR | vol | Sharpe | maxDD |
|---|---:|---:|---:|---:|---:|
| 60/40 SPY/VFITX | 16,748 | 9.4% | 11.2% | 0.86 | -24.4% |
| Capped 60/40 | 10,050 | 6.6% | 8.0% | 0.83 | -22.1% |
| Trend-switched 60/40 | 18,901 | 10.2% | 9.2% | 1.11 | -10.4% |
| Trend-switched + capped | 13,986 | 8.3% | 7.0% | 1.18 | -7.8% |

Further numbers for the combination in the walk-forward window:

- Sharpe difference vs capped 60/40: −0.01, 90% interval [−0.17, +0.16]: a tie.
- Sharpe difference vs plain 60/40: +0.21, 90% interval [−0.07, +0.48], P(≤0) = 0.11.
  Vs SPY: +0.35, [+0.07, +0.64], P(≤0) = 0.02.
- Alpha vs static SPY/IEF exposure: +2.5%/yr, about $250 a year on $10k, t = 2.3
  (betas 0.24 SPY, 0.32 IEF).
- Invested 82% on average; the SPY leg is on 81% of days.
- Calendar years: four small or large losses (2011 −0.5%, 2015 −0.8%, 2018 −0.6%,
  2022 −12.1%); 2008 was +2.6% and 2009 was 0.0% (it sat out both the crash and the rebound).
  Worst rolling 12 months −12.5%.
- Insensitive to execution: Sharpe 0.97 at 2 bps, 0.94 at 10 bps, 0.93 with next-close fills.

**Observations.**

- In the window the combination ties the cap alone on Sharpe, has the smallest drawdown of
  any candidate except the 50/50 blend, and is the most even across sub-periods (worst 0.75
  where the cap alone has 0.52).
- On 1994-2004 it is clearly better than both the plain and the capped mix. **Caveat:** the
  idea was formed after seeing the cap's yearly returns on 1994-2004 in E09, so that period
  is not an untouched test of it. The window result is the clean one, and there it is a tie.
- It does not protect against a bond sell-off: in 2022 it lost 12.1%, because the 40% IEF
  leg is always on and bonds fell with stocks.
- It earns the fewest dollars of the 60/40 family ($1,200/yr vs $1,771 plain).

**Verdict.** The most consistent candidate across 31 years. Chosen as the finalist (see
"Finalist choice" below).

---

## Finalist choice (written and committed before the holdout was run)

**Finalist: Trend-switched + capped 60/40.** 60% SPY while SPY's 12-month return is
positive (else cash), 40% IEF, scaled down so expected volatility (20-day covariance) is at
most 8% a year, rebalances under 5% of equity skipped, signal at the close, trade at the
next open.

Why this one and not the capped 60/40, which has the highest walk-forward Sharpe (0.97 vs 0.96):

- In the walk-forward window the two are a statistical tie; the combination has the smaller
  drawdown (−13.6% vs −17.3%) and the steadier sub-periods.
- The capped mix failed its own pre-registered out-of-window check (E09). Picking it anyway
  would be following a ranking over evidence.
- Each component has independent support in the literature (slow trend; volatility
  management of equity exposure), and every parameter is a textbook value (12 months, 20
  days) or was shown to sit on a plateau (E04).

What could be wrong with this choice: the trend switch was added after seeing where the cap
failed, which is how overfitting happens. The holdout is the check on that. The capped
60/40 is reported on the holdout too, as a comparison row only.

One more disclosure: I am a language model whose training data extends past November 2024,
so I have vague general knowledge of how markets moved in 2025. I did not look at any
holdout bar, and the choice above rests only on the numbers in this log, but that
background knowledge cannot be fully ruled out as an influence.

---

## Holdout — run once, 2026-11-17 23:08

**Setup.** `research/holdout.py`, after the finalist was committed (c482992) and the script
rehearsed on sealed data (`--rehearsal`, 2022-11-17 .. 2024-11-15; a first rehearsal wrote
its output to `holdout_result.txt` by mistake because one edit had not applied; that file
held sealed-data numbers only, was deleted, and the rehearsal was repeated before the real
run). Window 2024-11-17 .. 2026-11-17, 501 sessions, fresh $10,000, 5 bps, next-open fill.

**Result.**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Finalist: trend-switched + capped 60/40 | 777 | 391 | 3.8% | 7.9% | 0.51 | -9.9% | 1.3x | 26 |
| Capped 60/40 (comparison only) | 1,087 | 547 | 5.3% | 8.1% | 0.68 | -8.5% | 1.1x | 24 |
| SPY buy & hold | 2,776 | 1,396 | 13.1% | 16.9% | 0.81 | -18.8% | 0.2x | 5 |
| Equal weight (1/N) | 2,610 | 1,313 | 12.4% | 11.8% | 1.05 | -12.2% | 1.1x | 25 |
| 60/40 SPY/IEF | 1,879 | 945 | 9.0% | 10.5% | 0.88 | -10.5% | 0.7x | 15 |
| TSMOM 12m, 1/N | 1,846 | 929 | 8.9% | 9.9% | 0.91 | -11.1% | 3.1x | 68 |
| SPY>SMA200 else IEF | 1,706 | 858 | 8.2% | 12.4% | 0.70 | -11.4% | 3.0x | 64 |

**Verdict.** Profitable (+$777, about $390 a year) and the worst row in the table. The
walk-forward Sharpe of 0.96 became 0.51. The risk management cost return and saved almost
no drawdown versus plain 60/40 on these days. The late-added trend switch did worse than
the cap alone. Reported as-is; no further analysis of the holdout days.

---

## Trial count

Configurations evaluated on the walk-forward window so far (every one, including failures):

- E01: 8 baselines (no tuning).
- E03: 7 rule candidates, pre-specified.
- E04: 20 sensitivity runs around one E03 candidate (5 extra target×window cells, 3 extra bands,
  1 fill, 1 cost, 10 mix runs). Declared as sensitivity, not selection.
- E05: 3 new configurations (blend, idle cash in IEF, that plus cap).
- E06: 2 models, one specification (plus 0 and 2 bps reruns of the same targets).
- E09: 1 pre-registered out-of-window check of the E03 candidate (plus its proxy check).
- E07: 2 policies x 5 seeds, one specification (plus a diagnostic that re-scores, no new configuration).
- E10, E11: analyses of existing configurations only.
- E12: 2 relative-momentum configurations, pre-specified.
- E08: 1 PPO specification x 5 seeds.

Total distinct strategy configurations evaluated on the walk-forward window: 27 (8 baselines,
7 + 3 + 2 rule candidates, 2 supervised, 2 direct-policy, 1 PPO, plus the two close relatives
in E05), not counting the 20 declared sensitivity runs of E04.
- E13: 2 new configurations (trend-switched 60/40, and that plus the cap), on two periods.
  Total distinct configurations: 29.
