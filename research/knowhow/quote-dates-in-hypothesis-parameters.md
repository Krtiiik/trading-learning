---
title: "A date in a hypothesis's parameters must be quoted, or the run cannot be recorded"
kind: pitfall
area: process
source: "Found while registering H1001 on 2026-11-18: yaml.safe_load, trading.research.harness._plain and registry.spec_hash called by hand on the two spellings. No run was lost to it; a full harness run with an unquoted date was not tried."
trust: medium
date: 2026-11-18
---

In front matter, `start: 2019-07-01` is read by YAML as a date object and `start: "2019-07-01"` as text. `trading research check` accepts both. `evaluate_strategy` accepts both too, so the test would run; but the harness then writes the parameters into the run record as JSON, and `json.dumps(_plain({"start": datetime.date(2019, 7, 1)}))` raises `TypeError: Object of type date is not JSON serializable`. The run would end in a traceback after the test has been computed, with nothing recorded.

Write every date in `primary_test.params` in quotes. If one slipped through, adding the quotes afterwards is safe: the spec hash turns dates into text before hashing, so both spellings give the same hash (checked) and the hypothesis is still as registered.

Not established: that nothing else in the harness trips over a date object first; the pieces were called one by one.
