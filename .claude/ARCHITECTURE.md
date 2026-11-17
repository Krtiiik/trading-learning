# Architecture

<!--
The big picture and the reasons behind it, for Claude.
Don't list files, classes or signatures: the source shows those.
Write what a newcomer couldn't work out by reading the code: how the parts fit together,
why a design was chosen over the obvious alternative, and the constraints that shaped it.
-->

## Overview

A personal research workbench for learning algorithmic trading. So far it covers market data: download daily bars for a universe of US ETFs from a free provider, keep them locally, sanity-check them, and load them into pandas for research in marimo notebooks. A course site in `learn/` teaches with it (see the last section).

## Components and flow

`trading fetch` → for each symbol in the universe, the update step asks a provider for bars (everything, or only since the last stored bar) → normalizes them into the common bar shape → writes them to the store → runs the sanity checks and prints issues as warnings.

Research code never talks to a provider: it reads the store through `load_bars` / `load_panel`, so notebooks work offline and see the same data every time.

## Design notes

**Provider behind a protocol.** yfinance is an unofficial scraper that can break or be rate-limited; keeping it behind a small interface lets Stooq, Alpaca or a paid source replace it without touching storage or research code. Providers normalize to one bar shape so nothing downstream knows where data came from.

**Raw prices plus adjusted close, not fully adjusted OHLC.** Raw prices (split-adjusted only, as Yahoo serves them) equal what traded since the last split and are never touched by dividends; the adjusted close gives total returns. Fully adjusted OHLC can be derived when needed. Storing only adjusted data would lose the traded prices.

**Incremental updates re-fetch the last stored bar.** A bar stored while its session was open gets replaced by final values. Comparing that bar's adjustment factor with the provider's tells whether a new dividend re-adjusted history. A split does not change the factor (it scales raw and adjusted prices alike), so a split not yet stored is checked separately. Either way the symbol is downloaded in full, since the stored prices are stale; appending would mix pre- and post-split prices.

**Parquet per symbol, data not in git.** Typed, compressed, fast with pandas, trivially inspectable per symbol, and appending one symbol never rewrites others. Data is reproducible from `trading fetch` and redistributing Yahoo data would break its terms, so `data/` is gitignored.

**Sanity checks warn, never block.** Free data regularly has gaps and real extreme moves (e.g. silver on 2026-01-30); refusing to store it would leave no data. Issues are surfaced so research can decide.

**Daily index is tz-naive trading dates.** A daily bar belongs to a session date, not an instant. Intraday bars, once added, should use tz-aware UTC timestamps.

## Course site (`learn/`)

The course that teaches with this workbench is a Jekyll site in `learn/`: Markdown lessons and reference sheets with Liquid includes for quizzes and asides, built locally and published as one private multi-file Claude artifact (republished after every change). There is no GitHub Pages and no server.

**Why the artifact, and why it shapes the code.** Publishing as an artifact gives the reader an in-page Ask Claude chat (the artifact's `sample` capability) and somewhere to keep those chats (its `db`), which later teaching sessions read with ArtifactData to see what the learner asked. Everything follows from where the pages must work: under `jekyll serve`, as plain files, and inside the artifact. Hence relative `.html` links only, KaTeX rendering to MathML (the artifact's content policy allows CDN scripts but not CDN stylesheets or fonts), and Ask Claude lighting up only when the runtime grants it, so the same build shows no trace of it locally.

**Chats are owner-only.** The published db rules restrict every path to the artifact's owner, so a shared link never exposes the learner's questions, while ArtifactData (acting as the owner) can still read them. The private `data/users/<id>/` area was avoided because nobody but that viewer can read it, which would hide the chats from the teaching session too.

**Content has one writer.** Teaching sessions decide what to teach and delegate the writing to the `lesson-writer` agent, which owns the Markdown format, includes and math conventions, so lessons stay uniform as the course grows. The visual design is specified separately in `learn/DESIGN.md`.

**Facts are read, not copied.** The course brief sent with each chat (mission and glossary) and the dashboard's ETF count are read at build time from `MISSION.md`, `.claude/CONTEXT.md` and `universe.toml`, so the site cannot drift from them.
