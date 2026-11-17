from datetime import date

import pandas as pd
import pytest

from trading.data.bars import BAR_COLUMNS
from trading.data.providers import ProviderError, YahooProvider
from trading.data.providers.yahoo import normalize


def yahoo_frame() -> pd.DataFrame:
    """Shaped like yfinance `Ticker.history(auto_adjust=False, actions=True)` output."""
    index = pd.DatetimeIndex(
        ["2024-03-14 00:00:00-04:00", "2024-03-15 00:00:00-04:00"], name="Date"
    ).tz_convert("America/New_York")
    return pd.DataFrame(
        {
            "Open": [510.0, 511.0],
            "High": [512.0, 513.0],
            "Low": [509.0, 508.0],
            "Close": [511.5, 509.8],
            "Adj Close": [505.1, 509.8],
            "Volume": [70_000_000, 90_000_000],
            "Dividends": [0.0, 1.6],
            "Stock Splits": [0.0, 0.0],
            "Capital Gains": [0.0, 0.0],
        },
        index=index,
    )


def test_normalize_renames_columns_and_strips_timezone():
    bars = normalize(yahoo_frame())

    assert tuple(bars.columns) == BAR_COLUMNS
    assert bars.index.name == "date"
    assert bars.index.tz is None
    assert list(bars.index.strftime("%Y-%m-%d")) == ["2024-03-14", "2024-03-15"]
    assert bars.loc["2024-03-15", "dividends"] == 1.6
    assert bars["volume"].dtype == "int64"


def test_normalize_of_empty_response_is_empty_bars():
    bars = normalize(pd.DataFrame())

    assert bars.empty
    assert tuple(bars.columns) == BAR_COLUMNS


def test_normalize_rejects_response_missing_columns():
    with pytest.raises(ProviderError, match="Adj Close"):
        normalize(yahoo_frame().drop(columns="Adj Close"))


@pytest.mark.network
def test_yahoo_fetches_real_spy_bars():
    bars = YahooProvider().fetch("SPY", "1d", start=date(2024, 3, 11), end=date(2024, 3, 15))

    assert list(bars.index.strftime("%Y-%m-%d")) == [
        "2024-03-11",
        "2024-03-12",
        "2024-03-13",
        "2024-03-14",
        "2024-03-15",
    ]
    assert (bars["close"] > 0).all()


@pytest.mark.network
def test_yahoo_unknown_symbol_raises_provider_error():
    with pytest.raises(ProviderError):
        YahooProvider().fetch("NOSUCHTICKERXYZ", "1d")
