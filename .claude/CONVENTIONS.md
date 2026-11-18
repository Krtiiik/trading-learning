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

## Where things go

- Library code in `src/trading/`; data concerns under `trading.data`, future areas (strategies, backtesting) as sibling packages.
- New providers in `trading/data/providers/`, one module per provider.
- Notebooks are marimo `.py` files in `notebooks/`; they import from `trading` rather than copying logic. Anything reused by two notebooks moves into the package.
- Downloaded data lives in `data/` (gitignored); override with `TRADING_DATA_DIR`. The default universe is `universe.toml` at the repo root.
- Crypto datasets live under `data/binance/`, raw downloads under `data/raw/`, derived panels under `data/cache/`. Only `trading rebuild` writes the first two.

## Testing

- pytest; tests run offline. Use the `FakeProvider`, `make_bars` and `store` helpers from `tests/conftest.py` instead of mocking yfinance.
- Tests that hit the network are marked `@pytest.mark.network` and are skipped by default; run them with `uv run pytest -m network`.
- Crypto tests use `FakeArchive` (an in-memory Binance archive) and the `crypto_root` fixture (a small Store rebuilt from it, spanning train, dev and test) instead of real downloads.
