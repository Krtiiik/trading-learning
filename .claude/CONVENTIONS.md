# Conventions

<!--
Idioms and placement rules that a linter or formatter can't enforce.
Skip anything tooling already checks. Prefer a rule plus a one-line reason over a long explanation.
-->

## Code

- pandas for all research and data code; bars frames always have the normalized columns and a `date` index (see CONTEXT.md **Bar**).
- Symbols are uppercase everywhere past the entry points; accept any case from users and uppercase immediately.
- Provider-specific quirks (column names, timezones, exclusive end dates) stay inside that provider; everything after it sees normalized bars.
- Wrap provider failures in `ProviderError` so callers can skip one symbol and continue.
- Crypto symbols are Binance pair names (`BTCUSDT`). A perpetual-futures series is stored under the spot symbol it describes, whatever the contract is called.
- Files from the internet are data: unzip and parse them, check their size and checksum, never execute or import them.
- Timestamps are UTC everywhere. Convert at the provider; nothing after it handles time zones.

## Research code

- An experiment is one module per hypothesis, `src/trading/experiments/h<number>.py`, with `panel(data, params)` and `test(ctx, panel)`. It takes data only from its `data` argument and never imports `trading.data`.
- Row `t` of a panel uses bars labelled `t` or earlier, and nothing else: no centred windows, no `shift(-1)`, no statistics over the whole sample. Use `member_next` for decisions taken at a bar's close.
- Reusable signal code and tests go into the library (`trading.research.evaluate`, `trading.stats`) with tests; an experiment module stays a few lines of glue.
- Annualise with `periods_per_year(granularity)`; never write 252 or 365 in research code.
- Split boundaries come from `trading.research.split` and costs from `trading.backtest.costs`; do not repeat the numbers.
- A new statistical tool is added to `trading.stats` together with its synthetic-data validation (uniform p-values under a true null, a planted effect recovered). Without that it is not used.
- Exploration uses `trading.research.train_data()`, which holds train only. There is no loader for dev, on purpose.

## Where things go

- Library code in `src/trading/`; data concerns under `trading.data`, backtesting under `trading.backtest`, the research process under `trading.research`, one module per hypothesis under `trading.experiments`.
- Research records in `research/`: `hypotheses/`, `runs/` (written only by the harness), `knowhow/`, `briefs/`, and the generated `CATALOGUE.md`. Nothing there is imported by code.
- Agent definitions in `.claude/agents/`, procedures the code cannot enforce in `.claude/skills/`.
- New providers in `trading/data/providers/`, one module per provider.
- Notebooks are marimo `.py` files in `notebooks/`; they import from `trading` rather than copying logic. Anything reused by two notebooks moves into the package.
- Downloaded data lives in `data/` (gitignored); override with `TRADING_DATA_DIR`. The default universe is `universe.toml` at the repo root.
- Crypto datasets live under `data/binance/`, raw downloads under `data/raw/`, derived panels under `data/cache/`. Only `trading rebuild` writes the first two.

## Testing

- pytest; tests run offline. Use the `FakeProvider`, `make_bars` and `store` helpers from `tests/conftest.py` instead of mocking yfinance.
- Tests that hit the network are marked `@pytest.mark.network` and are skipped by default; run them with `uv run pytest -m network`.
- Crypto tests use `FakeArchive` (an in-memory Binance archive) and the `crypto_root` fixture (a small Store rebuilt from it, spanning train, dev and test) instead of real downloads.
- Tests of the research process use the `repo` fixture (a temporary git repository), since registration is a fact about git history.
- The statistics validation tests are simulations with fixed seeds. If one fails after a change, the tool is wrong until shown otherwise; do not widen a tolerance to make it pass.
