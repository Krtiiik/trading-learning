---
name: record-knowhow
description: Record one lesson, pitfall, how-to or market fact as a know-how note in research/knowhow/, with where it came from and how far to trust it. Use whenever you learn something another agent or the owner would otherwise have to rediscover, and read the notes before starting work in research/.
---

# Record know-how

Know-how is how agents share what they learn. A note states **one** thing, says where it came from, and says how sure we are.

## Before you work

Read `research/knowhow/README.md` (the index) and open every note listed for your area or under "Everyone". Trust each as far as its `trust` field says and no further: a `low` note is a lead, not a rule.

## When to write one

Write a note when you learned something that will change what the next agent does: a pitfall you hit, a quirk of the data, a limit of a tool, a procedure that works, a descriptive fact about the market (a distribution, a seasonality, a correlation) even if it suggests no trade. Do not write one for a single hypothesis's result (that lives in its file) or for anything the code or the docs already say.

## How

1. **Check the index first.** If a note already covers it, update that note instead (add your evidence, raise or lower its trust, date the change). Delete a note that turned out to be wrong, and say so in your commit message.
2. **Create `research/knowhow/<short-slug>.md`**:

   ```markdown
   ---
   title: "One sentence stating the lesson"
   kind: pitfall            # lesson | pitfall | how-to | fact
   area: data               # everyone | data | engine | statistics | process | market | <family>
   source: Where this comes from: a run record, a measurement, a paper, another session's report
   trust: medium            # high: measured or tested here, reproducible | medium: seen here once, or well-sourced elsewhere | low: hearsay, a single run, another asset class, memory
   date: 2026-11-18
   ---

   The lesson in two to six sentences: what is true, how we know (the number, the command or the run id), and what to do about it.
   ```

   - The title is the lesson itself, not a topic: "Hourly bars are missing for every coin during exchange outages", not "Outages".
   - Give the evidence a reader can check: a run id, a command with its output, a table.
   - Say what it does **not** establish. A lesson from ETFs is not yet a lesson about crypto; a pattern seen on train is not a finding.
   - Market facts come from train data only, and say so.
3. **Add one line to `research/knowhow/README.md`** under the note's area: `- [Title](slug.md) (trust)`.
4. **Commit** the note and the index together, by path.

Keep notes short. A note that needs sections is two notes.
