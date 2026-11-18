"""The normalized shape of bars that every provider returns and the store keeps."""

from typing import Literal

import pandas as pd

Granularity = Literal["1d", "1h"]
"""Bar length: daily, or hourly (crypto only so far)."""

GRANULARITIES: tuple[Granularity, ...] = ("1d", "1h")

BAR_COLUMNS: tuple[str, ...] = (
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "dividends",
    "splits",
)
"""Raw (unadjusted) OHLCV, the provider's adjusted close, and corporate actions on that bar."""

EXTRA_COLUMNS: tuple[str, ...] = (
    "quote_volume",
    "trades",
    "taker_buy_volume",
    "taker_buy_quote_volume",
)
"""Optional columns a provider may add after `BAR_COLUMNS`; the store keeps them when present."""

INDEX_NAME = "date"

_LENGTHS: dict[str, pd.Timedelta] = {"1d": pd.Timedelta(days=1), "1h": pd.Timedelta(hours=1)}


def empty_bars() -> pd.DataFrame:
    """A bars frame with no rows but the normalized columns and index."""
    frame = pd.DataFrame(
        {column: pd.Series(dtype="float64") for column in BAR_COLUMNS},
        index=pd.DatetimeIndex([], name=INDEX_NAME, dtype="datetime64[ns]"),
    )
    return frame.astype({"volume": "int64"})


def check_granularity(granularity: str) -> Granularity:
    if granularity not in GRANULARITIES:
        raise ValueError(
            f"unsupported granularity {granularity!r}; supported: {', '.join(GRANULARITIES)}"
        )
    return granularity  # type: ignore[return-value]


def bar_length(granularity: Granularity) -> pd.Timedelta:
    return _LENGTHS[check_granularity(granularity)]


def bar_columns(frame: pd.DataFrame) -> list[str]:
    """`BAR_COLUMNS` followed by the extra columns `frame` carries, in canonical order."""
    return [*BAR_COLUMNS, *(column for column in EXTRA_COLUMNS if column in frame.columns)]


def knowable_at(index: pd.DatetimeIndex, granularity: Granularity) -> pd.DatetimeIndex:
    """The UTC moment at which each 24/7 bar's contents are final: its label plus its length.

    A bar is labelled by its open. Daily labels are tz-naive UTC dates, hourly labels tz-aware
    UTC instants; the result is always tz-aware UTC. Not meant for exchange-session bars
    (US ETFs), whose daily bar is final at the session close.
    """
    opened = index if index.tz is not None else index.tz_localize("UTC")
    return opened + bar_length(granularity)
