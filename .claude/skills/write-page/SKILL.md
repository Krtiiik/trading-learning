---
name: write-page
description: Write one learning site page end to end - writer and illustrator, review and fact check until clean, build, banner check, commit. Use when the user asks to write a concept or lesson for the learning site.
argument-hint: <concept slug | lesson idea>
---

Run the learning site agents to write one page. The argument names a concept slug from `catalog.yaml`, or describes a lesson.

You (the main session) only dispatch agents, run the build and commit. The agents write and judge.

## 1. Brief

- Concept: find the slug in the catalog. If it is not there, ask the user whether to add it (and to which group) before you go on.
- Lesson: settle a title, a one-line summary, a slug and `builds_on` with the user, unless the argument already gives them (for example, a planner suggestion).

The brief is the slug, kind, title, summary, group or `builds_on`, and anything the user said about the page.

## 2. Write and draw

Dispatch in parallel:

- `writer` with the brief.
- `illustrator` with the brief (lessons and concepts both get a banner).

## 3. Check until clean

Dispatch in parallel, each with the slug and the file path:

- `reviewer`
- `fact-checker`

Run `uv run python scripts/build.py --words <slug>` first and put the number in the reviewer's task: the reviewer cannot run commands, and counting by hand gives a different number each time.

The page is **clean** when both end with `clean`. If not, send the blocker and major findings (minor ones too, if they are cheap) to `writer`, and banner findings to `illustrator`. Then check again.

Once the page is clean, you may send the cheap minor findings to `writer` in one last pass. Skip the re-check after that pass: minor fixes only change wording. Read the page yourself, and run the checkers again only if the writer changed a fact, a number or the page's structure.

Repeat until clean. Stop and ask the user when the writer rejects a finding and the next round raises the same finding again: the agents disagree and the user decides.

## 4. Build and look

1. Run `uv run python scripts/build.py` and `uv run pytest`. Send build errors to the agent that owns the file.
2. Open the page with `preview_start` (`site`) and look at the banner and page in light and dark mode, at desktop and mobile width. Send what looks wrong (clipped text, overlap, unclear picture, unreadable at card size on the home page) to `illustrator`, then look again.

## 5. Commit

Add a line to `CHANGELOG.md` under `[Unreleased]` / `Added` (a new page) or `Changed` (a rewrite). Commit content, banner and changelog together, for example `feat: write the spread concept page`.

Report to the user: the page, the number of check rounds, findings the writer rejected and why, and minor findings left open.
