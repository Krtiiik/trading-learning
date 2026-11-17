# Teaching notes

- Workspace lives in `learn/` inside the `trading` repo so lessons can use the learner's own stored data as examples.
- Prefer worked examples computed from the learner's store (`data/`) over invented numbers; they make the concepts concrete and double as a check on the data.
- Use the project glossary terms (`.claude/CONTEXT.md`): bar, raw price, adjusted close, adjustment factor, panel.
- Learner wrote "dropdowns" for drawdowns in the first request; treat as a typo, not a misconception.
- Lessons 1 and 2 delivered 2026-11-17 (bars and adjusted close; the stats table). No evidence of understanding yet, so no learning records. Next session: start with a few retrieval questions from both lessons before new material.
- Finding from lesson 1 research, fixed 2026-11-17: Yahoo's `close` is split-adjusted; glossary corrected and incremental fetch now re-downloads after a new split.

## The course site

The course is a Jekyll site in this folder, published as a private artifact: <https://claude.ai/artifact/XHsD8PE8fxWCrd7a6Ehxor>.

- **Writing.** Decide what to teach here, then delegate the writing to the `lesson-writer` agent (`.claude/agents/lesson-writer.md`) with the topic, the objective, the worked numbers and the part. It owns the Markdown format, the includes and the math conventions; don't hand-write lesson pages.
- **Parts 3 and 4** in `_data/parts.yml` were drafted from the mission's success criteria during the port, not chosen by a teaching session. Confirm or replace them before writing lessons for them.
- **Rebuild and republish after every change.** From `learn/`: `bundle exec jekyll build`, then `ruby publish.rb`. Then publish with the Artifact tool to the URL above: `file_path` `learn/_publish/index.html`, `root` `learn/_site`, `files` = the map in `learn/_publish/files.json`, and leave `capabilities` out so the stored declaration (`sample`, `db` with owner-only rules, `user`) carries over. Preview locally with `bundle exec jekyll serve`; Ask Claude stays hidden there by design.
- **Reading the learner's chats.** Each page's Ask Claude thread is saved in the artifact db, collection `chats`, one document per page with id `<page key>.<volume>` (e.g. `lessons-the-stats-table.1`; the key is the page path with `/` as `-`). A document holds `page`, `url`, `title`, `updated` and `items`: `{t: "user", text, quote?: {where, text}, at}`, `{t: "claude", text, at}` and `{t: "topic", at}` for a "New topic" break. Read them with the ArtifactData tool on the URL above: `list` the `chats` collection for an overview, `get` one document for a page's thread. Only the owner can read them; questions show where the learner got stuck, so check them before planning the next lesson.
