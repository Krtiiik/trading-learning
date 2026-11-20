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

## Design notes

**Titles and summaries only in the catalog.** A planned concept needs a working link and hover preview before its body exists, so title and summary can't live in the page file. Concept files carry only the body.

**Build-time link resolution with `[[slug]]`.** Slugs survive moving files between folders, and the build can fail on a typo. Plain Markdown paths would break silently.

**Multi-page output, not a single-page app.** The site will have high tens of pages, and real URLs per page keep it simple. Previews and search share one generated index file.

**Republishing is a reminder to Claude, not automation.** Only Claude can publish an artifact, so a git hook can't do it. A Claude Code hook can, but only for commits made through Claude, and only on `main`, so worktree branches don't overwrite the live site.

<!--
One short entry per design choice that needs explaining. Add one only when the reason isn't obvious from the code.

**Choice.** Why it was made, and what was rejected.
-->
