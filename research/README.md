# Research: how to work here

This folder holds the records of crypto market research: what was predicted, what was tested, what came out. The code that enforces the process is in `src/trading/` (`research`, `backtest`, `stats`, `experiments`). Read this page once and you can run an experiment without asking anyone.

Terms in **bold** are defined in `.claude/CONTEXT.md`; use them as defined.

## The idea in five lines

1. A **hypothesis** is written down and committed before it is tested: prediction, one **primary test**, decision rule.
2. Time is **split** in three **segments**: train (to 2022-12-31), dev (2023-2024), test (2025 on). The test segment is **sealed**.
3. The **harness** is the only way to test a hypothesis. It writes the **run record**.
4. Where a hypothesis stands on the **claim ladder** is computed from the records, with false-discovery control across all hypotheses.
5. Negative results stay. The **catalogue** lists everything.

## What is where

```
research/
  README.md       this page
  briefs/         what each session was asked to do
  hypotheses/     one file per hypothesis (H1001-...md); TEMPLATE.md to copy
  runs/           <date>/<id>-r<nn>.json, written by the harness, never by hand
  knowhow/        one note per lesson, pitfall, how-to or market fact; README.md is the index
  literature/     published evidence per family, collected by the Literature scout
  CATALOGUE.md    generated index of every hypothesis and its status
  LOG.md          chronological narrative of what was done and why
  SEAL.json       appears only once the test seal has been opened
```

## Setup

```bash
uv sync
uv run trading rebuild          # crypto datasets from the Binance public archive: ~30 min, ~3.7 GB, once
uv run trading verify           # every dataset matches its manifest
uv run pytest                   # ~2 minutes
```

No account, API key or order-placing code exists here or may be added. This is local research.

## Run your first experiment

Suppose you want to test "coins that rose over the last four weeks keep rising".

**1. Read what is known.** `research/knowhow/README.md` and the notes it lists for your area, and `research/literature/` for published evidence.

**2. Look at data, on train only.**

```python
from trading.research import train_data

data = train_data()                 # everything up to 2022-12-31; later data cannot be loaded
market = data.market("1d")          # or "1h"
close = market.frame("close")       # DataFrame: bar labels x coins
members = market.frame(market.member)
funding = data.series("funding", "1d")
```

There is no loader for dev. If your idea came from looking at train data, its **origin** is `exploration` and only its dev run counts as evidence.

**3. Register it.** Follow `.claude/skills/register-hypothesis/SKILL.md`: copy `hypotheses/TEMPLATE.md`, fill it in, compute the **minimum detectable effect**, write the experiment module, commit both.

```bash
uv run trading research mde sharpe-difference --correlation 0.8
uv run trading research check H1002
```

An experiment is a module with two functions. This is a complete one:

```python
# src/trading/experiments/h1002.py
from trading.research.evaluate import evaluate_strategy, rebalance_labels


def panel(data, params):
    """Target weights. Row t may use bars labelled t or earlier, nothing else."""
    market = data.market("1d")
    close = market.frame("close")
    rising = close / close.shift(params["lookback_days"]) - 1 > 0
    members = market.frame(market.member_next)        # membership known at the bar's close
    weights = (rising & members).astype(float).div(members.sum(axis=1).clip(lower=1), axis=0)
    return weights.loc[rebalance_labels(market, "week")]   # only these rows trade; others hold


def test(ctx, panel):
    return evaluate_strategy(ctx, panel, "1d", benchmark="equal_weight")
```

For a predictive claim, `panel` returns the signal and `test` calls `evaluate_predictor(ctx, panel, "1d", horizon=7)`.

**4. Run it.** Follow `.claude/skills/run-experiment/SKILL.md`.

```bash
uv run trading research run H1002 --segment train
git add research/runs && git commit -m "docs: record H1002 train run" -- research/runs
uv run trading research status H1002
uv run trading research catalogue
```

If the ladder says `candidate`, run `--segment dev` (once). If it then says `supported`, a Skeptic reviews it (`.claude/skills/review-claim/SKILL.md`).

**5. Write the verdict** into the hypothesis file's body and record anything worth knowing as a know-how note (`.claude/skills/record-knowhow/SKILL.md`).

## The claim ladder

```
registered      prediction, test and decision rule committed first
tested (train)  -> rejected          kept as a negative result
candidate       train p-value passes Benjamini-Hochberg at 10% across the train tests
                of ALL registered literature hypotheses (untested ones count as p = 1)
replicated(dev) -> not replicated    kept, flagged
supported       dev estimate has the predicted sign and at least the pre-declared size
skeptic review  -> refuted           kept, with the reason
confirmed       eligible as a test-set finalist
```

- One primary test per hypothesis. A variant is a new hypothesis and counts in the false-discovery total.
- An `exploration` hypothesis skips train: it runs on dev, and the dev p-values of all exploration hypotheses pass through their own Benjamini-Hochberg control at 10%.
- "Meaningful size" on dev is declared per hypothesis before any run: `min_size` in the estimate's unit, and for literature hypotheses `min_ratio` of the train estimate (default 0.5).
- A trading claim's estimate is net of costs, so "positive on dev" already means it survived them; the same test at **double cost** is in every run record.
- Status can change when other hypotheses are registered, because the false-discovery control is across all of them. Always read it from `trading research status`.

## What the harness refuses, and why

| It refuses | Because |
|---|---|
| a hypothesis file that is not committed | registration must precede the test; git history proves the order |
| a hypothesis whose frozen fields changed since its first commit | a changed test is a new hypothesis |
| uncommitted code in any module the run uses | the record's commit must reproduce the run |
| an experiment that imports `trading.data` | experiments get data only up to the end of their segment |
| a panel whose past rows change when later bars are removed | that is look-ahead |
| a train run of an `exploration` hypothesis | it came from train; testing it there proves nothing |
| a dev run of a hypothesis that is not a candidate, or a second dev run | dev is for replication, once |
| any test run before the seal is opened, or for a non-finalist, or a second one | the test segment is used once, at the end |
| a trading claim without double-cost numbers | every trading claim is reported at double cost |
| a model whose predictors have not reached candidate | models are built only on predictors with evidence |
| a Store that does not match its manifests | the record must name the data that was really used |

Fix the cause. Never work around a refusal.

## Conventions you need

- **Timing.** A bar is labelled by its open, in UTC. A signal is computed at a bar's close and traded at the next bar's open.
- **Long or flat.** Weights between 0 and 1, a row sums to at most 1, cash earns 0%. Perpetual-futures data is a predictor only.
- **Costs.** 10 bps fee plus slippage per side by **liquidity tier**: 2 bps for BTC and ETH, 5 bps for the next ten coins, 15 bps for the rest.
- **Universe.** Trade only **point-in-time universe** members (`market.member`, or `market.member_next` for a decision at a bar's close).
- **Benchmarks.** Buy-and-hold BTC, the equal-weight universe (rebalanced monthly), and cash, all through the same engine and costs; `evaluate_strategy` reports all three.
- **Annualisation.** `periods_per_year(granularity)`: a market that never closes has 365 days.
- **Hindsight.** The models doing this research know markets up to mid-2026. A motivation cites literature or train-period evidence, never memory of later years.

## Opening the seal

Only in the final phase, once: at most five **confirmed** hypotheses are chosen as **finalists**, the list and each pass rule are committed, and then

```bash
uv run trading research open-seal H1001 H3004
```

writes `SEAL.json`. Each finalist gets one test run. If nothing is confirmed, the seal stays closed.

## Who does what

Agent definitions are in `.claude/agents/`: the **Researcher** owns a family, the **Skeptic** tries to break supported findings, the **Data steward** answers for the data, the **Literature scout** supplies hypotheses from published work. The procedures they share are the skills in `.claude/skills/`.
