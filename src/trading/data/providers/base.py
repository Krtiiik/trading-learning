from datetime import date
from typing import Protocol

import pandas as pd

from trading.data.bars import Granularity


class ProviderError(Exception):
    """A provider could not deliver bars for a symbol (unknown symbol, network, rate limit)."""


class Provider(Protocol):
    """A source of market bars.

    Implementations return frames in the normalized bar shape (see `trading.data.bars`):
    columns `BAR_COLUMNS`, index named `date`, sorted ascending, no duplicates.
    For daily bars the index holds tz-naive trading dates.
    """

    name: str

    def fetch(
        self,
        symbol: str,
        granularity: Granularity,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Bars for `symbol` from `start` to `end`, both inclusive; `None` means unbounded."""
        ...
