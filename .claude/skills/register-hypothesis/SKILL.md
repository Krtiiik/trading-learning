---
name: register-hypothesis
description: Register a research hypothesis - write its file with the prediction, the single primary test and the decision rule, check that it is testable, and commit it before anything is run. Use whenever a new hypothesis, a variant of one, or a model is about to be tested.
---

# Register a hypothesis

Registration is the commit of the hypothesis file. The harness reads git history: it refuses a hypothesis that is not committed, and one whose registered fields changed afterwards. So everything below happens **before** the first run, and none of it is edited after.

1. **Pick the id.** `H` plus four digits, the next free number in your block: `H1xxx` time-series, `H2xxx` cross-sectional, `H3xxx` derivatives, `H4xxx` cross-market, `H0xxx` models and anything across families. A variant of an existing hypothesis gets a new id.
2. **Copy `research/hypotheses/TEMPLATE.md`** to `research/hypotheses/<id>-<short-slug>.md` and fill in every field. The template's comments say what each field means. The ones people get wrong:
   - `origin`: `literature` only if the idea comes from a published source you cite. If looking at train data played any part in choosing the idea or its parameters, it is `exploration`, and its evidence will be the dev run alone.
   - `motivation` and `sources`: published work, or the train-period observation that prompted it (say what you looked at). Never what you remember happening after 2022.
   - `prediction`: a direction and a rough size in the unit of the estimate. "Positive, about 0.3 Sharpe" is a prediction; "there may be an effect" is not.
   - `primary_test`: exactly one. Name the experiment module, the granularity, the parameters and, in words, the statistic and its p-value. Parameters come from the source or from a stated convention, not from trying values.
   - `decision.dev`: `min_size` is the smallest dev estimate you would call meaningful, in the estimate's unit; `min_ratio` (literature only) the share of the train estimate dev must reach. Defaults are in the template; deviate only with a reason written next to it.
   - `claim`: `trading` if the test is a strategy against a benchmark after costs (it must then report double cost), `predictive` otherwise.
   - A **model** also lists `predictors:` (the ids of the hypotheses whose signals it uses, each at least a candidate) and its test is "the model beats the simple rule built from the same predictors, on dev".
3. **Judge testability before running.** Compute the minimum detectable effect for train and dev and write both into `power`:
   ```
   uv run trading research mde sharpe-difference --correlation 0.8 --start 2019-07-01
   uv run trading research mde mean --deviation <sd of one observation> --per-year 365 --overlap <horizon>
   ```
   If the predicted size is far below what train can detect, say so in `power.note`. The hypothesis may still be registered (a negative result will then mean "too small to see", not "absent"), but do not register several underpowered variants hoping one lands.
4. **Write the experiment module** `src/trading/experiments/h<number>.py` with `panel(data, params)` and `test(ctx, panel)`. Take data only from `data`; use `evaluate_strategy` or `evaluate_predictor` for the test. Do **not** run it on real data yet. A unit test on synthetic data is fine and welcome.
5. **Validate, commit, check.**
   ```
   uv run trading research check <id>          # reports structural problems before the commit
   git add research/hypotheses/<id>-*.md src/trading/experiments/h<number>.py
   git commit -m "docs: register <id> <short title>" -- research/hypotheses/<id>-*.md src/trading/experiments/h<number>.py
   uv run trading research check <id>          # must now say "is registered"
   ```
   Commit only these files, by path.

After this commit the front matter is frozen except `status` and `skeptic`, which the tools write. Results and discussion go in the body, below the registered sections. If you later think the test was badly designed, leave this file as it is, say so in its body, and register a new hypothesis.
