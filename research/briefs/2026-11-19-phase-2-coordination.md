# Phase 2 coordination: rules for working in parallel

Date: 2026-11-19. Phase 2 of `2026-11-18-crypto-research-infrastructure.md` (the evidence catalogue) started at **13:16 UTC** and ends when every family has met its quota or at **01:16 UTC on 2026-11-20**, whichever comes first. This note adds what several agents working in one checkout at the same time need to know. Where it and an agent definition or skill differ, this note wins for Phase 2.

## Who owns what

| Family | Hypothesis ids | Family helper module (optional) |
|---|---|---|
| time-series | H1002 to H1999 (H1001 exists and counts) | `src/trading/experiments/timeseries_tools.py` |
| cross-sectional | H2001 to H2999 | `src/trading/experiments/crosssection_tools.py` |
| derivatives | H3001 to H3999 | `src/trading/experiments/derivatives_tools.py` |
| cross-market | H4001 to H4999 | `src/trading/experiments/crossmarket_tools.py` |

A Researcher writes only:

- its hypothesis files `research/hypotheses/H<its ids>-*.md` and experiment modules `src/trading/experiments/h<its ids>.py`;
- its family helper module, for code two of its experiments share, and tests for its own code (`tests/test_h<id>.py`, `tests/test_<family>_tools.py`);
- its own know-how notes, and lines under its own family heading in `research/knowhow/README.md` (`### Time-series`, `### Cross-sectional`, `### Derivatives`, `### Cross-market`, all under `## Families`).

Nobody but the coordinator edits the shared library (`src/trading/research/`, `src/trading/stats.py`, `src/trading/backtest/`, `src/trading/data/`), `research/LOG.md`, `research/CATALOGUE.md`, or another family's files. If you need a library change (a new statistical tool, a helper every family would use, a bug fix), do not make it: describe it precisely in your report, and carry on with hypotheses that do not need it.

## Rules that differ from working alone

1. **Do not run `uv run trading research catalogue`.** It rewrites every hypothesis file's status line and the catalogue, and would collide with other agents. Read status with `uv run trading research status <id>`. The coordinator regenerates the catalogue at checkpoints.
2. **Statuses will move, and candidates are decided at the checkpoint.** False-discovery control runs across every registered literature hypothesis, and one without a train run counts as p = 1. While other families are still registering and running, almost nothing shows as `candidate`. So: run train for every literature hypothesis you register, report, and stop. The coordinator announces the candidates once all train runs are in; dev runs for literature hypotheses happen only then.
3. **Run everything you register.** A registered hypothesis that is never run stays in the false-discovery total as p = 1 and makes every other hypothesis harder to pass. Do not register a hypothesis you may not get to.
4. **An exploration hypothesis runs on dev as soon as it is registered** (it cannot run on train). Its dev run is its one look.
5. **Commit by path, and expect company.** `git add <your paths>` then `git commit -m "..." -- <your paths>`. If git reports `index.lock`, wait a few seconds and retry. Never `git add -A`, never commit another agent's files, never push, amend or rebase. The harness refuses a run while any project module the run loads is uncommitted, so commit your modules before running; another agent's uncommitted experiment does not affect you.
6. **Write the verdict when the status is final for now.** For a rejected literature hypothesis or an exploration hypothesis after its dev run, write Results and Verdict at once. For a literature hypothesis that might still become a candidate, write Results after the train run and leave the Verdict for the checkpoint.

## Quota and spread, per family

- At least **8 hypotheses taken to a verdict** (time-series: H1001 plus seven).
- Different sub-angles, not eight variants of one idea, and **both granularities**: at least two of the eight on hourly bars.
- **Mixed origins**: at least two `exploration` and at least four `literature`.
- Mixed claims: predictive claims pooled across the universe have far more observations than a trading claim's Sharpe difference and are the kind the ladder can separate (`research/knowhow/small-sharpe-differences-rarely-climb-the-ladder.md`). Use them where the hypothesis is about whether a signal carries information; use a trading claim where the hypothesis is about a rule after costs. Always state the minimum detectable effect next to the predicted size.
- Descriptive facts about the market seen on train (distributions, correlations, seasonality) are worth a know-how note even when they suggest no trade.

## What has changed in the tools since the example hypothesis

- The bootstrap behind a trading claim's p-value now uses a block length fixed by the sample size (its cube root: 11 bars for 1,280 daily bars). Run records carry `harness_version` 3.
- Run records of trading claims hold the benchmark at double cost and the dropped weight of the evaluated window.
- A strategy that puts weight on a coin outside the point-in-time universe is refused: mask weights with `market.member_next`.
- A hypothesis can declare the first day of its evaluation: pass `start=params["start"]` to `evaluate_strategy` or `evaluate_predictor`. Quote dates in YAML parameters.
- Three kinds of predictive test are ready, all in `trading.research.evaluate`:
  - `evaluate_predictor(ctx, signal, granularity, horizon, method="rank_ic" | "fama_macbeth")`: does the signal order the coins against each other? (cross-sectional)
  - `evaluate_predictor(..., method="panel" | "panel_entity" | "panel_time")`: is a coin's return higher when its own signal is higher, pooled over coins and time? For a coin's own funding rate, a calendar dummy, a volatility state. The estimate is the slope (forward return per unit of signal), so put the signal in comparable units across coins. Errors come from time blocks and allow coins to move together.
  - `evaluate_market_predictor(ctx, series, granularity, horizon, target="equal_weight" | "BTCUSDT")`: does one market-wide series forecast the market's return? One series has few independent observations: check the minimum detectable effect.
  Signals are DataFrames (bar labels by coins) or, for the market test, a Series by bar label; row t may use bars labelled t or earlier only. Forward returns run from the next bar's open, as the engine trades.
- `data.etf(field)` gives the US ETF daily bars up to the segment's end; `data.series("funding" | "premium" | "open_interest", granularity)` the perpetual-futures series aligned to spot bars. Open interest is being downloaded as Phase 2 starts and may not be there yet: check with `uv run trading verify`.

## Practical

- The bash tool mangles long heredocs that contain quotes. Write scripts with your file tool into a folder of your own under `C:\Users\lukas\AppData\Local\Temp\claude\2f19a128e68c6c2f\2e7d5544-1e63-4511-8bdb-68bfc25c0e66\scratchpad\` and run them with `uv run python <file>`. Keep throwaway scripts out of the repository.
- A daily experiment runs in seconds, an hourly one in tens of seconds to a few minutes (the hourly train market is 46,949 bars by 183 coins).
- Every commit message ends with a blank line and `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`.

## A Researcher's run in Phase 2

The coordinator gives each Researcher a family, a block of ids, a helper module name and a quota. Everything else is here.

**Read first, in this order:** the role definition `.claude/agents/researcher.md` (follow its steps and rules); `research/briefs/2026-11-19-phase-2-coordination.md` (rules for several agents working in parallel: it wins where it differs from the definition or a skill); `research/README.md`; `.claude/CONTEXT.md` (use its terms exactly); the "Research code" section of `.claude/CONVENTIONS.md`; `research/knowhow/README.md` and every note it lists under Everyone, Process, Data, Engine, Statistics and your family (the Data steward is adding notes on hourly bars, funding, basis and ETF bars right now: re-read the Data section of the index just before you register anything that uses them); the skills `.claude/skills/register-hypothesis/SKILL.md`, `.claude/skills/run-experiment/SKILL.md`, `.claude/skills/record-knowhow/SKILL.md`; and, as a worked example of a registered hypothesis with its experiment and test, `research/hypotheses/H1001-trend-filter-on-daily-bars.md`, `src/trading/experiments/h1001.py`, `tests/test_h1001.py` (your files can be shorter than H1001's).

**How each hypothesis goes (the coordination note has the reasons):**
- *Literature origin:* state the minimum detectable effect, write the hypothesis file and the experiment module, `uv run trading research check <id>`, commit both by path (that commit is the registration), `check` again, `uv run trading verify`, `uv run trading research run <id> --segment train`, commit the run record by path, `uv run trading research status <id>`, then write "Results" in the file's body (numbers quoted from the run record with its run id). Do NOT run dev for a literature hypothesis in this run: candidates are decided at a checkpoint once every family's train runs are in. If the train p-value is above 0.10 the hypothesis cannot become a candidate whatever the others do, so also write its "Verdict" (rejected) now; if it is at or below 0.10, leave the Verdict for the checkpoint and say so in the file.
- *Exploration origin:* look at train data only (`trading.research.train_data()`), write down in the hypothesis file what you looked at and what you saw, register as above, then `uv run trading research run <id> --segment dev` (its one look; it cannot run on train), commit the record, and write Results and Verdict. Whether it ends as supported depends on false-discovery control across all exploration hypotheses' dev p-values, so quote the status the tool prints and note that it can move.
- Never run `uv run trading research catalogue`, never edit `research/LOG.md`, `research/CATALOGUE.md`, the shared library, or another agent's files. Run every hypothesis you register. Never look at dev by any route other than the single harness dev run.
- Predictive claims use `evaluate_predictor` (cross-sectional `rank_ic` / `fama_macbeth`, or pooled `panel` / `panel_entity` / `panel_time`) or `evaluate_market_predictor`; trading claims use `evaluate_strategy`. Declare an evaluation `start` in the parameters (quoted date) wherever the early, thin universe or a late-starting dataset would distort the test, and pass it on. `rank_ic` and `fama_macbeth` skip bars with fewer than `min_assets` scored coins (default 5). Decisions taken at a bar's close use `market.member_next`. The harness recomputes your `panel` three more times with later bars removed, so keep it vectorised.
- A parameter comes from the cited source or from a convention you state before running; you do not try values. A variant is a new hypothesis and counts.
- Hindsight guard: motivations cite published sources (the Literature scout's notes name them, with sample end dates) or train-period observations, never what you remember of 2023 onward.

**Keep it lean.** About 15 minutes per hypothesis. A hypothesis file needs every front-matter field, a "Registered design" of a paragraph or two, a small Results table and a few sentences of Verdict; not an essay. One short test file for your helper module on the synthetic `crypto_root` fixture (see `tests/conftest.py`; its universe has only four members) is welcome; do not test each experiment separately. Write know-how notes only for lessons another agent would otherwise rediscover (including descriptive market facts seen on train), listed under your family's heading in `research/knowhow/README.md`.

**Commits:** by path only (`git add <your paths>`, then `git commit -m "..." -- <your paths>`); Conventional Commit summaries without a scope (`docs:` for records and notes, `feat:` / `test:` for code); every message ends with a blank line and `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`; on an `index.lock` error wait a few seconds and retry; never `git add -A`, never push, amend or rebase. If the harness refuses something, fix the cause; never work around it. If you need a change in the shared library, do not make it: describe it in your report.

**Final report to the coordinator (short; lead with what is true now):** one table row per hypothesis: id, short title, origin, claim, granularity, segment run, estimate, one-sided p, minimum detectable effect, status as printed by `trading research status`; then what the infrastructure refused or made awkward, any library change you need, what you could not verify, and your commit hashes.
