# Architecture

<!--
The big picture and the reasons behind it, for Claude.
Don't list files, classes or signatures: the source shows those.
Write what a newcomer couldn't work out by reading the code: how the parts fit together,
why a design was chosen over the obvious alternative, and the constraints that shaped it.
-->

## Overview

<!-- What the system does and its main parts, in a few sentences. -->

## Components and flow

<!-- How the main parts relate, and how data or control moves between them. -->

### Learning site

`learning/build.py` reads the catalog, Markdown content and banners, checks that they agree (unknown links, missing banners and misplaced files all fail the build), and renders Jinja2 templates into `learning/dist/`. It also writes `static/index.js`, the data behind link hover previews and search. The output is published as one multi-file private artifact. Its URL is in `learning/artifact-url.txt`.

Sync: the `learning-sync.sh` PostToolUse hook runs after `git commit`/`git merge` on `main`. If `learning/` differs from the commit in `learning/.published-commit` (local, gitignored), it tells Claude to rebuild and republish to the same URL. `learning/SPEC.md` is the contract between structure and design.

Content work runs through `learning-*` subagents in `.claude/agents/`: a planner (what to write next), a writer, an illustrator (banners), and three read-only checkers: a reviewer (one page, readability and consistency), a fact checker (one page, against the web) and an auditor (all pages, drift). The `write-page` skill chains writer and illustrator, then reviewer and fact checker until clean, then build, a banner look in the browser pane, and commit.

## Design notes

**Titles and summaries only in the catalog.** A planned concept needs a working link and hover preview before its body exists, so title and summary can't live in the page file. Concept files carry only the body.

**Build-time link resolution with `[[slug]]`.** Slugs survive moving files between folders, and the build can fail on a typo. Plain Markdown paths would break silently.

**Multi-page output, not a single-page app.** The site will have high tens of pages, and real URLs per page keep it simple. Previews and search share one generated index file.

**Checkers report, they do not edit.** The reviewer, fact checker and auditor are read-only and never see the writer's reasoning, so a review stays independent of authorship and every change goes through the one agent that owns the file. Readability and facts are separate agents so that neither job gets diluted, and the fact checker searches the web even when fairly sure, because beginners trust the site.

**Republishing is a reminder to Claude, not automation.** Only Claude can publish an artifact, so a git hook can't do it. A Claude Code hook can, but only for commits made through Claude, and only on `main`, so worktree branches don't overwrite the live site.

<!--
One short entry per design choice that needs explaining. Add one only when the reason isn't obvious from the code.

**Choice.** Why it was made, and what was rejected.
-->
