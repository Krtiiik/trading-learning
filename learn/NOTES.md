# Teaching notes

- Workspace lives in `learn/` inside the `trading` repo so lessons can use the learner's own stored data as examples.
- Prefer worked examples computed from the learner's store (`data/`) over invented numbers; they make the concepts concrete and double as a check on the data.
- Use the project glossary terms (`.claude/CONTEXT.md`): bar, raw price, adjusted close, adjustment factor, panel.
- Learner wrote "dropdowns" for drawdowns in the first request; treat as a typo, not a misconception.
- Lessons 1 and 2 delivered 2026-11-17 (bars and adjusted close; the stats table). No evidence of understanding yet, so no learning records. Next session: start with a few retrieval questions from both lessons before new material.
- Open finding from lesson 1 research: Yahoo's `close` is split-adjusted, contradicting the glossary's "raw price, never revised"; incremental fetch does not re-download after a split.
