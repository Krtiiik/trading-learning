---
# Copy to H<4 digits>-<short-slug>.md, fill in every field, delete these comments, and commit
# BEFORE running anything. Everything here is frozen at that commit except `status` and
# `skeptic`, which the tools write. See .claude/skills/register-hypothesis/SKILL.md.

id: H0000                # H1xxx time-series, H2xxx cross-sectional, H3xxx derivatives, H4xxx cross-market, H0xxx models
title: One line saying what is claimed
family: time-series      # time-series | cross-sectional | derivatives | cross-market
origin: literature       # literature (published source) | exploration (came from looking at train data)
claim: trading           # trading (a rule beats a benchmark after costs) | predictive (a signal ranks or forecasts returns)
status: registered       # written by `trading research catalogue`; leave as is

motivation: >
  Why this should hold, in a few sentences. Cite published work or train-period evidence
  (say what you looked at). Never what you remember happening after 2022.
sources:
  - "Author, A. and Author, B. (year). Title. Venue. Sample: assets, dates. Link."

prediction:
  direction: positive    # positive | negative: the sign you predict for the estimate
  size: "about 0.3"      # rough size, in the unit below
  unit: difference in annualised net Sharpe ratio (strategy minus benchmark)

primary_test:            # exactly one
  experiment: trading.experiments.h0000
  granularity: 1d        # 1d | 1h
  params: {}             # every number the experiment uses, with values from the source or a stated convention
  description: >
    In words: what is computed, against what, with which statistic and which p-value.

decision:
  train: >
    One-sided p-value of the primary test in the predicted direction; candidate if it passes
    Benjamini-Hochberg at 10% across the train tests of all registered literature hypotheses.
  dev:
    min_ratio: 0.5       # literature only: dev estimate at least this share of the train estimate
    min_size: 0.2        # and at least this, in the estimate's unit (trading: > 0 means it survives costs)

power:                   # from `uv run trading research mde ...`, before running
  mde_train: 0.0
  mde_dev: 0.0
  note: Is the predicted size detectable? If not, what will a null result mean?

data:
  - binance/spot/1d
  - binance/universe

# For a model only: the hypotheses whose predictors it uses (each must be at least a candidate).
# predictors: [H1001, H3002]
---

# H0000: title

## Registered design

Anything about the design that does not fit the fields above: the exact rule, the benchmark,
what would count as the test having been done wrongly. Written before the first run.

## Results

Added after the runs, by the Researcher. Numbers quoted from the run records, with their ids.

## Verdict

What the result means and how sure we are. Status as printed by `trading research status`.

## Skeptic review

Added by the Skeptic, if the hypothesis is reviewed.
