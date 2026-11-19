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
- `data.etf(field)` gives the US ETF daily bars up to the segment's end; `data.series("funding" | "premium" | "open_interest", granularity)` the perpetual-futures series aligned to spot bars. Open interest is being downloaded as Phase 2 starts and may not be there yet: check with `uv run trading verify`.

## Practical

- The bash tool mangles long heredocs that contain quotes. Write scripts with your file tool into a folder of your own under `C:\Users\lukas\AppData\Local\Temp\claude\2f19a128e68c6c2f\2e7d5544-1e63-4511-8bdb-68bfc25c0e66\scratchpad\` and run them with `uv run python <file>`. Keep throwaway scripts out of the repository.
- A daily experiment runs in seconds, an hourly one in tens of seconds to a few minutes (the hourly train market is 46,949 bars by 183 coins).
- Every commit message ends with a blank line and `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`.
