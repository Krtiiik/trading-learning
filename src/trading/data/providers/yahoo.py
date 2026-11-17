from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from trading.data.bars import BAR_COLUMNS, INDEX_NAME, Granularity, empty_bars
from trading.data.providers.base import ProviderError

_INTERVALS: dict[str, str] = {"1d": "1d"}

_COLUMNS = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "splits",
}


class YahooProvider:
    """Yahoo Finance through the unofficial yfinance library. Personal and research use only."""

    name = "yahoo"

    def fetch(
        self,
        symbol: str,
        granularity: Granularity,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        interval = _INTERVALS.get(granularity)
        if interval is None:
            raise ValueError(f"Yahoo provider does not support granularity {granularity!r}")

        # Without this yfinance logs errors and returns an empty frame instead of raising.
        yf.config.debug.hide_exceptions = False
        range_args: dict[str, object]
        if start is None and end is None:
            range_args = {"period": "max"}
        else:
            # yfinance treats `end` as exclusive.
            range_args = {"start": start, "end": end + timedelta(days=1) if end else None}
        try:
            raw = yf.Ticker(symbol).history(
                interval=interval, auto_adjust=False, actions=True, **range_args
            )
        except Exception as error:
            raise ProviderError(f"Yahoo could not fetch {symbol}: {error}") from error
        return normalize(raw)


def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """Turn a yfinance daily history frame into the normalized bar shape."""
    if raw.empty:
        return empty_bars()
    missing = [column for column in _COLUMNS if column not in raw.columns]
    if missing:
        raise ProviderError(f"Yahoo response lacks columns {missing}")

    frame = raw[list(_COLUMNS)].rename(columns=_COLUMNS)
    index = pd.DatetimeIndex(frame.index)
    if index.tz is not None:
        index = index.tz_localize(None)
    frame.index = index.normalize().astype("datetime64[ns]").rename(INDEX_NAME)
    frame = frame[~frame.index.duplicated(keep="last")].sort_index()
    frame = frame.astype({column: "float64" for column in BAR_COLUMNS} | {"volume": "int64"})
    return frame[list(BAR_COLUMNS)]
