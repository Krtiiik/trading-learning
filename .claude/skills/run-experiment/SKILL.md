---
name: run-experiment
description: Run a registered hypothesis through the harness on the right segment, commit the run record, and read the result off the claim ladder. Use for every train, dev or test run of a hypothesis.
---

# Run an experiment

The harness is the only way a hypothesis is tested. It writes the run record itself; you never create or edit a file in `research/runs/`.

1. **Make sure the data is as recorded.** `uv run trading verify`. If a dataset does not match its manifest, stop and ask the Data steward (or run `uv run trading rebuild`); a run on a changed Store is refused anyway.
2. **Commit your code first.** The harness refuses when any project module the run uses is uncommitted, so that the record's commit reproduces the run.
3. **Run the segment the ladder allows.**
   ```
   uv run trading research run <id> --segment train
   ```
   - A `literature` hypothesis runs on **train** first. It may run on **dev** only once the ladder shows it as `candidate`.
   - An `exploration` hypothesis cannot run on train (it came from there); it runs on **dev** directly.
   - **Dev runs once** per registered specification. Before you run it, be sure the train run was right, because you will not get another look.
   - **Test** runs happen only in the final phase, after the seal has been opened for the finalists. Do not attempt one.
4. **If the harness refuses, read the reason and fix the cause.** Do not work around it. The refusals and what they mean:
   - *not registered / changed since it was registered*: see the `register-hypothesis` skill. A changed test is a new hypothesis.
   - *uncommitted code*: commit the files it names.
   - *looks ahead*: your `panel` gave different values for past bars when later bars were removed. Find the line that uses the future (a centred window, `shift(-1)`, a whole-sample statistic, "last bar of the period" decided from the next bar) and fix it. Nothing was recorded.
   - *not a candidate / already ran on dev / sealed*: the ladder does not allow this run. That is the answer.
5. **Commit the run record**, by path, as its own commit:
   ```
   git add research/runs/<date>/<id>-r<nn>.json
   git commit -m "docs: record <id> <segment> run" -- research/runs/<date>/<id>-r<nn>.json
   ```
6. **Read the status from the ladder, not from the p-value.**
   ```
   uv run trading research status <id>
   uv run trading research catalogue        # updates status lines and CATALOGUE.md; commit those too
   ```
   Whether a hypothesis is a candidate depends on every other registered hypothesis, and can change when more are registered. Report the status the tools print.
7. **Write the verdict** in the hypothesis file's body: the estimate, the p-value and q-value, the double-cost result for a trading claim, and what it means. Quote numbers from the run record.

**Re-running.** A train run can be repeated (each run is recorded; the latest counts). A dev run can be repeated only when the earlier one was invalid, for instance a bug in library code or a rebuilt dataset, with the reason on record:

```
uv run trading research run <id> --segment dev --rerun-reason "..."
```

"The result was disappointing" is not a reason. If the experiment module itself was wrong, the honest route is a new hypothesis.
