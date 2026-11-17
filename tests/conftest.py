from datetime import date

import pandas as pd
import pytest

from trading.data.bars import BAR_COLUMNS, INDEX_NAME, empty_bars
from trading.data.storage import BarStore


def make_bars(
    start: str, periods: int, close: float = 100.0, adj_factor: float = 1.0
) -> pd.DataFrame:
    """Business-day bars with a gently rising close and a constant adjustment factor."""
    index = pd.bdate_range(start, periods=periods, name=INDEX_NAME).astype("datetime64[ns]")
    closes = [close + step for step in range(periods)]
    frame = pd.DataFrame(
        {
            "open": closes,
            "high": [value + 1 for value in closes],
            "low": [value - 1 for value in closes],
            "close": closes,
            "adj_close": [value * adj_factor for value in closes],
            "volume": [1_000_000] * periods,
            "dividends": [0.0] * periods,
            "splits": [0.0] * periods,
        },
        index=index,
    )
    return frame.astype({column: "float64" for column in BAR_COLUMNS} | {"volume": "int64"})


class FakeProvider:
    """Serves bars from an in-memory history and records each request."""

    name = "fake"

    def __init__(self, history: dict[str, pd.DataFrame] | None = None) -> None:
        self.history = history or {}
        self.requests: list[tuple[str, date | None, date | None]] = []

    def fetch(self, symbol, granularity, start=None, end=None) -> pd.DataFrame:
        self.requests.append((symbol, start, end))
        bars = self.history.get(symbol, empty_bars())
        lower = None if start is None else pd.Timestamp(start)
        upper = None if end is None else pd.Timestamp(end)
        return bars.loc[lower:upper]


@pytest.fixture
def store(tmp_path) -> BarStore:
    return BarStore(tmp_path / "data")
