---
name: review-claim
description: Carry out a Skeptic review of a research finding - re-derive it, attack it with a fixed list of checks on train data, and write the verdict into the hypothesis file. Use when a hypothesis reaches "supported", or when a result (positive or negative) needs an independent audit.
---

# Review a claim

A review is an attempt to break a finding. It starts from the registration and the run records, uses train data only, and ends in a verdict in the hypothesis file. The checks below are the minimum; add any attack the specific claim invites.

**Before you start:** read the front matter of the hypothesis file, its run records and its experiment module. Leave the Researcher's verdict text for the end.

## The tool

`trading.research.harness.replay` re-runs a hypothesis's experiment on train without writing a record, optionally with changed parameters:

```python
from trading.research.harness import replay

base = replay("H1001")                    # the registered test, on train
other = replay("H1001", lookback_days=56)  # one parameter moved
print(base.estimate, base.p_value, base.metrics["strategy"]["sharpe"])
```

It works on train only. There is no way to replay dev, by design: the dev numbers are in the run record.

## The checks

| # | Check | How | It fails when |
|---|---|---|---|
| 1 | Re-derivation | `replay(id)` against the train run record; then the headline number by a second route (a loop over bars, `scipy` by hand on a few dates) | the numbers do not match, or the second route disagrees |
| 2 | Look-ahead and leakage | read `panel` line by line; ask of every input "knowable at this bar's close?"; check membership uses `member_next`; look for whole-sample statistics | any input is not knowable in time |
| 3 | Neighbouring parameters | `replay` with each parameter at two or three neighbours on each side | the registered value is a spike among weak neighbours |
| 4 | Sub-periods | the estimate per calendar year of train (slice the returns in `metrics`, or recompute per year) | one year carries most of the effect |
| 5 | Sub-universes | without BTC and ETH; top half and bottom half by liquidity tier | a handful of coins carries it |
| 6 | Costs | the double-cost numbers in the records; a one-bar execution delay | the sign flips at double cost or with the delay |
| 7 | Placebo | `stats.circular_shift_test`, `stats.asset_permutation_test`, or the same rule on a signal that should not work | the placebo "works" about as well |
| 8 | Hindsight | every source published or from train; cited samples end by 2022; nothing in the motivation that only later years could suggest | the motivation leans on what happened after 2022 |
| 9 | Process | `uv run trading research check <id>`; run records carry the registered spec hash; dev was run once; the dataset ids in the records match `uv run trading verify` | the registration or the records are not what they should be |

For a negative result (rejected or not replicated) the same checks apply in mirror: is the null result an artefact of a bug, of costs that are too harsh, of a test with no power? Report the minimum detectable effect next to the estimate.

## The verdict

1. Add a `## Skeptic review` section to the body of the hypothesis file: one short paragraph per check with what you ran and the numbers, then the verdict and the strongest reason for it. Say which checks were weak or could not be done.
2. Record it:
   ```
   uv run trading research skeptic <id> --verdict confirmed --reason "..."
   uv run trading research catalogue
   ```
   For a `supported` hypothesis the verdict is `confirmed` or `refuted`: `confirmed` only when every check passed; anything that would make you hesitate to bet on it is `refuted`, with the reason. For any other status (an audit of a rejected or not replicated hypothesis) the verdict is `audited`: it records that the review happened and changes no status, and its reason says whether the recorded status is sound. The command refuses the wrong kind of verdict for the status.
3. Commit the hypothesis file and the catalogue, by path.

Your variations are attacks. None of them is registered or reported as a better version, and none of their numbers leaves the review section.
