# Trading

My personal collection of learning how to trade.

## Setup

Requires [uv](https://docs.astral.sh/uv/) (it installs Python 3.14 if needed).

```bash
uv sync
```

## Market data

Download daily bars for the ETF universe in `universe.toml` into `data/`:

```bash
uv run trading fetch
```

Run it again any time to add only the new bars. Other options:

```bash
uv run trading fetch --symbols AAPL MSFT   # specific symbols instead of the universe
uv run trading fetch --full                # re-download whole histories
```

Data comes from Yahoo Finance via yfinance, for personal research use only. Each fetch prints warnings for suspicious data (missing sessions, bad prices, large moves without a split).

Load stored bars in Python:

```python
from trading.data import load_bars, load_panel

spy = load_bars("SPY", start="2010-01-01")          # one symbol, all bar columns
prices = load_panel(["SPY", "TLT", "GLD"])          # adjusted close, one column per symbol
```

## Crypto market data

Rebuild the crypto datasets from the Binance public archive (no account or key needed):

```bash
uv run trading rebuild
```

This downloads daily bars for every USDT spot pair, ranks the point-in-time universe (top 40 by volume, re-ranked monthly), then fetches hourly bars, funding rates and basis for coins that were ever members. The first run takes about half an hour and 3.7 GB (including the panel cache built on first use); later runs reuse the verified downloads in `data/raw/`. Check the result at any time:

```bash
uv run trading verify           # quick: names, sizes, modification times
uv run trading verify --deep    # re-hash every file
```

Crypto research does not read these files directly; see `research/README.md`.

## Notebooks

```bash
uv run marimo edit notebooks/explore_bars.py
```

## Tests

```bash
uv run pytest
```

```bash
uv run pytest -m network
```

The second runs the tests that talk to Yahoo.
