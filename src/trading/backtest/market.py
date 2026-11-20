"""The price data a backtest trades against: raw prices for fills, dividends for income."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

import pandas as pd

from trading.data.storage import BarStore, load_panel


@dataclass(frozen=True)
class Market:
    """Raw open and close panels plus per-share dividends, on one shared date index.

    A NaN price means the symbol has no bar that day (not yet listed, or a gap):
    it cannot be traded then, and is valued at its last known close.
    """

    open: pd.DataFrame
    close: pd.DataFrame
    dividends: pd.DataFrame

    def __post_init__(self) -> None:
        for name in ("open", "dividends"):
            frame = getattr(self, name)
            if not frame.index.equals(self.close.index) or not frame.columns.equals(
                self.close.columns
            ):
                raise ValueError(f"{name} panel must share the close panel's index and columns")
        if not self.close.index.is_monotonic_increasing or self.close.index.has_duplicates:
            raise ValueError("market dates must be strictly increasing")

    @property
    def dates(self) -> pd.DatetimeIndex:
        return self.close.index  # type: ignore[return-value]

    @property
    def symbols(self) -> list[str]:
        return list(self.close.columns)

    @classmethod
    def from_store(
        cls,
        symbols: Iterable[str],
        start: date | str | None = None,
        end: date | str | None = None,
        store: BarStore | None = None,
    ) -> "Market":
        symbols = list(symbols)
        return cls(
            open=load_panel(symbols, "open", start=start, end=end, store=store),
            close=load_panel(symbols, "close", start=start, end=end, store=store),
            dividends=load_panel(symbols, "dividends", start=start, end=end, store=store).fillna(
                0.0
            ),
        )
