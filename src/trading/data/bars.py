"""The normalized shape of bars that every provider returns and the store keeps."""

from typing import Literal

import pandas as pd

Granularity = Literal["1d"]
"""Bar length. Only daily bars are supported so far; intraday values come later."""

GRANULARITIES: tuple[Granularity, ...] = ("1d",)

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

INDEX_NAME = "date"


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
