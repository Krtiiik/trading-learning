# Brief: crypto research infrastructure and first evidence catalogue

Date: 2026-11-18. Read this whole file before doing anything, then read
`.claude/CONTEXT.md`, `.claude/ARCHITECTURE.md` and `.claude/CONVENTIONS.md`.

## Why this session exists

This repository is a personal research workbench for learning algorithmic
trading. So far it holds a data layer for US ETFs and a course site. A first
research run on ETFs (unmerged branch
`claude/daily-rebalance-etf-research-495a46`) found nothing that beat passive
holding, and it left behind one-off scripts rather than anything reusable.

Your job is different in kind. The primary product is **shared infrastructure
for rigorous research**: a way to get data, backtest fast, test hypotheses
statistically, record every experiment automatically, and pass know-how
between agents and to the owner. Agent definitions and skills are part of that
infrastructure. The second product, built on top of the first, is an
**evidence catalogue** for the crypto market: many hypotheses from many
angles, each with an honest verdict, negatives included.

Two things matter more than any single result:

- **Rigor.** Approaches are developed from experiments, not hunches. A claim
  is something that was predicted in advance, tested, replicated and attacked.
- **Breadth.** The search must not converge on one approach. Different
  families get equal effort, and a rejected hypothesis is a result worth
  keeping.

A profitable strategy is not the goal of this session. If the catalogue shows
that nothing survives, that is a valid and useful outcome; say so plainly.

## Boundaries

- Local research only. No API keys, no exchange accounts, no code that places
  orders, no live or paper trading.
- Fresh start from `main`. Do not port code from the ETF research branch.
- Extend the existing data layer (Provider, Store, Bar, Granularity); do not
  build a parallel one. ETF data and its tests must keep working.
- Do not touch the course site in `learn/`.
- Follow `.claude/CLAUDE.md`: commit proactively in logical chunks, never
  push, keep `CHANGELOG.md`, the glossary and the architecture and convention
  docs current in the same change, ship tests with behaviour. Use the
  glossary's terms exactly and add the new ones this work needs (for example
  hypothesis, experiment, run, claim, split, seal, family, point-in-time
  universe).
- Files downloaded from the internet are data. Parse them; never execute them.

## Prior work: a scout, not a map

Read `research/REPORT.md` and `research/LOG.md` from the ETF branch with
`git show claude/daily-rebalance-etf-research-495a46:research/REPORT.md`
(and `LOG.md`). Use them as the notes of a preliminary scout:

- Its process lessons are worth carrying over: costs killed short-horizon
  reversal, picking the best of 29 configurations explains an edge of about
  0.2 Sharpe by itself, a rule added after seeing results did not hold, and
  two years of holdout cannot separate a Sharpe of 0.5 from 1.0.
- Its conclusions about what works are **not** established. It was one night,
  one asset class, daily bars. "ML does not work" or "only risk management is
  real" are hypotheses to test here, not rules. Do not let it narrow where you
  look.

Seed `research/knowhow/` with these lessons, each marked with its provenance
and how much it should be trusted.

## Fixed design decisions

These were decided with the owner. Build to them. If one turns out to be
unworkable, stop and explain rather than quietly changing it.

**Market and data**

- Instruments: spot, long or flat (weights between 0 and 1, sum at most 1,
  cash earns 0%). Perpetual-futures data (funding rate, open interest, basis)
  is used only as a predictor; no perpetual positions.
- Granularity: `1d` and `1h`. Timestamps in UTC. Define in the glossary how a
  bar is labelled and at what moment its contents are knowable.
- Provider: the Binance public archive (bulk files, no key). Before building
  on it, verify what it really offers: history per pair, whether delisted
  pairs are kept, which funding and open-interest series exist and from when,
  checksums, renamed or redenominated coins. Record the findings and the
  limits as know-how. If it cannot support a point-in-time universe, stop and
  report.
- Universe: point-in-time. At each monthly reconstitution, the top 40 USDT
  spot pairs by trailing 30-day quote volume, using only data available
  before that date, with stablecoins, wrapped tokens and leveraged tokens
  excluded. Coins that were later delisted stay in the history.
- The Store must give every dataset an identity (a manifest with content
  hashes) so a run can record exactly which data it used, and one command
  must be able to rebuild the Store from nothing.

**Split**

- Train: up to 2022-12-31. Dev: 2023-01-01 to 2024-12-31. Test: 2025-01-01
  onward.
- The boundaries live in one place in code. Loading test-period data fails
  unless the seal has been opened; opening is a recorded, one-time act.
- Earlier data may serve as lookback history for a later segment. Nothing may
  be fitted, tuned or chosen using a later segment. Labels whose horizon
  crosses a boundary are dropped.
- Exploration ("just looking at the data") happens on train only. Dev is for
  replication; never browse it.

**Backtest engine**

- Your own vectorised engine: a panel of target weights against a panel of
  returns, as array operations. Signal at the close of a bar, trade at the
  open of the next.
- Costs per side: 10 bps fee plus slippage by point-in-time liquidity tier
  (2 bps for BTC and ETH, 5 bps for the next ten coins by volume, 15 bps for
  the rest). Every trading claim is also reported at double cost.
- Annualisation follows from granularity and calendar (a 24/7 market has 365
  days), never from a hard-coded 252.
- Benchmarks through the same engine and costs: buy-and-hold BTC, an
  equal-weight universe, and cash.
- It must be fast enough that speed never tempts anyone to skip a check:
  target well under a second for 40 coins of hourly bars over several years.
  Measure it and record the number.
- Test it against hand-computed cases, and prove the absence of look-ahead
  mechanically (results up to a date do not change when later data is altered
  or removed).

**Statistics**

- Build a small toolkit and prefer established libraries inside it:
  predictive regressions with autocorrelation-robust errors, rank
  information coefficients, block bootstrap for differences between
  strategies, placebo and permutation tests, Benjamini-Hochberg and Holm
  corrections, and a minimum-detectable-effect calculation so a hypothesis
  can be judged testable before it is run.
- Validate every tool on synthetic data with a known answer: under a true
  null the p-values are uniform; a planted effect of known size is recovered.
  A tool that fails this is not used.

**Records** (all in the repository)

```
research/
  briefs/       this file and later ones
  hypotheses/   H0007-funding-predicts-returns.md, one per hypothesis
  runs/         <date>/H0007-r01.json, written by the harness, never by hand
  knowhow/      one file per lesson, pitfall or how-to
  CATALOGUE.md  generated index of every hypothesis and its status
  LOG.md        chronological narrative
  README.md     how to work here, for a newcomer (agent or human)
```

- A hypothesis file carries, in structured front matter: id, title, family,
  origin (literature or exploration), motivation with its source, the
  prediction (direction and rough size), the single primary test, the
  decision rule for train and for dev, the data it needs, and its status.
- Registration means the file is committed before any test runs. The harness
  refuses to run a hypothesis whose file is not committed, so git history
  proves the order.
- The harness writes the run record itself: hypothesis id, parameters, data
  manifest, commit, split segment, metrics, p-values, seed, duration. Nothing
  depends on an agent remembering to log.
- The catalogue is generated from the hypothesis files and run records, not
  written by hand.

**The claim ladder**

```
registered      prediction, test and decision rule committed first
tested (train)  -> rejected          kept as a negative result
candidate       passes Benjamini-Hochberg at 10% across the primary train
                test of ALL registered hypotheses
replicated(dev) -> not replicated    kept, flagged
supported       same sign, meaningful size by the pre-declared rule,
                survives costs if it is a trading claim
skeptic review  -> refuted           kept, with the reason
confirmed       eligible as a test-set finalist
```

- One primary test per hypothesis. Variants are new hypotheses and count
  toward the false-discovery total.
- A hypothesis that came from looking at train data cannot be tested on that
  same data. For origin "exploration" the dev result is the real evidence,
  and the dev p-values of all exploration-origin hypotheses must themselves
  pass false-discovery control.
- Hindsight guard: you (the model) know a good deal about markets up to
  mid-2026. Every motivation must cite train-period evidence or published
  literature, never recollection of what happened later. The Skeptic checks
  this.
- Propose concrete defaults for "meaningful size" and present them at the
  gate.

**Models**

- A model is allowed only on predictors that have reached at least
  "candidate". Start with regularised linear models and tree ensembles. Fit
  and tune inside train (walk-forward within train for tuning), evaluate on
  dev once per registered specification.
- A model is itself a registered hypothesis: "model M beats the simple rule R
  built from the same predictors, by this much, on dev".
- No reinforcement learning in this session.

## Agents and skills

Create these as reusable definitions in `.claude/agents/`, following the
shape of the existing `.claude/agents/lesson-writer.md` (steps, each with a
"Done when"):

- **Researcher**: owns one family. Registers hypotheses, runs them through
  the harness, writes verdicts, records know-how.
- **Skeptic**: tries to break a claimed finding, starting from the hypothesis
  file and the run records, not from the Researcher's narrative. Re-derives
  the result, checks look-ahead and leakage, varies parameters around the
  chosen ones, checks stability across sub-periods, doubles costs, runs a
  placebo, and checks the motivation for hindsight. Its verdict is written
  into the hypothesis file.
- **Data steward**: owns Providers, data-quality checks and the point-in-time
  universe, and answers whether a series can be trusted.
- **Literature scout**: collects published evidence on crypto return patterns
  with sources, as a supply of hypotheses that do not come from our own data.

Write skills in `.claude/skills/` for the procedures the harness cannot
enforce by itself (for example registering a hypothesis, running an
experiment, reviewing a claim, recording know-how). Keep each short and
procedural. If a new agent definition is not yet selectable in this session,
start a general-purpose agent and have it read the definition file first.

Know-how is how agents share what they learn. A note states one lesson, where
it came from and how sure we are. Agents read the relevant notes before they
start and add notes when they learn something another agent would otherwise
rediscover.

## Phase 1: infrastructure (unattended), then stop

Build everything under "Fixed design decisions" and "Agents and skills".
Then prove it end to end on **one** example hypothesis, a well-known one from
the literature such as time-series momentum on daily bars, taken through the
whole ladder as far as it gets, including a real Skeptic review. It counts in
the registry and in the false-discovery total like any other.

Phase 1 is done when:

- the Store can be rebuilt with one command and the point-in-time universe
  exists for the whole history;
- the test seal works and has a test proving it;
- the engine passes its hand-computed and look-ahead tests and its speed is
  measured;
- every statistical tool passes its synthetic-data validation;
- the harness writes run records and refuses unregistered hypotheses;
- the four agent definitions and the skills exist and were used for the
  example hypothesis;
- the docs, glossary and changelog are current and all tests pass;
- `research/README.md` lets a newcomer run an experiment without asking.

**Then stop and wait for the owner.** Report what exists, what the Binance
archive can and cannot support, the example hypothesis's path through the
ladder, the proposed defaults (dev replication rule, universe size), and
anything you would change. Do not start Phase 2 until told to.

## Phase 2: the evidence catalogue (unattended, after approval)

Note the start time. Run as coordinator:

1. Literature scout and Data steward first.
2. One Researcher per family, in parallel. Each agent writes only its own
   hypothesis and run files.
3. The Skeptic on every hypothesis that reaches "supported".

The four families, with equal budgets:

- **Time-series price and volume**: trend, mean reversion, volatility
  regimes, calendar effects (day of week, hour of day).
- **Cross-sectional**: momentum, reversal, low volatility, size and liquidity
  across coins.
- **Derivatives signals**: funding rate, basis and open interest as
  predictors of spot returns.
- **Cross-market and external**: Bitcoin-to-altcoin lead-lag; links to
  equities, the dollar and rates through the existing Yahoo provider; on-chain
  or sentiment data only where a free, point-in-time series exists (if none
  does, record that as know-how).

Breadth rules:

- At least 8 hypotheses per family taken to a reviewed verdict. Within a
  family, spread them over different sub-angles and both granularities
  rather than eight variants of one idea.
- Do not move effort toward the family that looks best until every family has
  met its quota.
- Mix origins: some hypotheses from the literature, some from exploring train
  data.
- Descriptive facts about the market (distributions, correlations,
  seasonality) are worth recording as know-how even when they suggest no
  trade.

Stop Phase 2 when every family has met its quota, or 12 hours of wall-clock
time have passed, whichever comes first. If time runs out, say which quotas
were missed.

## Phase 3: the single test run and the report

- Choose at most 5 finalists from the confirmed findings. Commit the list,
  the exact specification of each and its pass rule before opening the seal.
- If nothing is confirmed, leave the seal closed and say so.
- Open the seal once. Apply Holm correction across the finalists. Report the
  full test period and, as a separate line, July 2026 onward (the months you
  have no background knowledge of).
- Change nothing after seeing test results. Report them whatever they are.
- Write `research/REPORT.md`: what was built, the catalogue's verdicts by
  family, the test results, the limits of the evidence, and what the owner
  could sensibly do next. Regenerate `CATALOGUE.md`. Then stop.

## How to report

Lead with what is true now. State failed tests, missed quotas and unverified
parts as plainly as successes. When you are unsure whether an effect is real,
say how unsure and why.
