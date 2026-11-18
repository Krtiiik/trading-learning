"""Sanity checks on stored bars. Free data has gaps and glitches; these surface them."""

from dataclasses import dataclass

import pandas as pd
import pandas_market_calendars as mcal

from trading.data.bars import Granularity, bar_length

PRICE_COLUMNS = ("open", "high", "low", "close", "adj_close")
JUMP_THRESHOLD = 0.25
"""A close-to-close move larger than this (25%) without a split on that bar is suspicious."""
CRYPTO_JUMP_THRESHOLD = 3.0
"""For a coin, only a close that quadruples or falls by three quarters in one bar is flagged:
it is how an unrecorded redenomination or a reused symbol shows up."""


@dataclass(frozen=True)
class Issue:
    check: str
    message: str
    dates: tuple[pd.Timestamp, ...] = ()

    def __str__(self) -> str:
        if not self.dates:
            return f"{self.check}: {self.message}"
        shown = ", ".join(date.strftime("%Y-%m-%d") for date in self.dates[:5])
        more = f" (+{len(self.dates) - 5} more)" if len(self.dates) > 5 else ""
        return f"{self.check}: {self.message} [{shown}{more}]"


def validate_daily(bars: pd.DataFrame, calendar: str = "NYSE") -> list[Issue]:
    """Issues found in daily bars; an empty list means every check passed."""
    if bars.empty:
        return [Issue("empty", "no bars")]
    issues = [
        _duplicate_dates(bars),
        _non_positive_prices(bars),
        _inconsistent_ohlc(bars),
        *_calendar_gaps(bars, calendar),
        _unexplained_jumps(bars),
        _unadjusted_splits(bars),
    ]
    return [issue for issue in issues if issue is not None]


def validate_crypto(bars: pd.DataFrame, granularity: Granularity = "1d") -> list[Issue]:
    """Issues found in bars of a market that never closes: every bar label should be present."""
    if bars.empty:
        return [Issue("empty", "no bars")]
    expected = pd.date_range(bars.index.min(), bars.index.max(), freq=bar_length(granularity))
    ratio = bars["close"] / bars["close"].shift()
    extreme = ((ratio > 1 + CRYPTO_JUMP_THRESHOLD) | (ratio < 1 / (1 + CRYPTO_JUMP_THRESHOLD))) & (
        bars["splits"] == 0
    )
    issues = [
        _duplicate_dates(bars),
        _non_positive_prices(bars),
        _inconsistent_ohlc(bars),
        _issue("missing", f"{granularity} bars missing inside the history", expected.difference(bars.index)),
        _issue("jumps", "closes that quadrupled or fell by three quarters in one bar", extreme),
    ]
    return [issue for issue in issues if issue is not None]


def _issue(check: str, message: str, mask: pd.Series | pd.Index) -> Issue | None:
    dates = tuple(mask[mask].index) if isinstance(mask, pd.Series) else tuple(mask)
    return Issue(check, f"{len(dates)} {message}", dates) if dates else None


def _duplicate_dates(bars: pd.DataFrame) -> Issue | None:
    duplicated = pd.Series(bars.index.duplicated(), index=bars.index)
    return _issue("duplicates", "duplicate dates", duplicated)


def _non_positive_prices(bars: pd.DataFrame) -> Issue | None:
    prices = bars[list(PRICE_COLUMNS)]
    bad = (prices.isna() | (prices <= 0)).any(axis=1)
    return _issue("prices", "bars with missing or non-positive prices", bad)


def _inconsistent_ohlc(bars: pd.DataFrame) -> Issue | None:
    high, low = bars["high"], bars["low"]
    bad = (
        (high < low)
        | (bars["open"] > high)
        | (bars["open"] < low)
        | (bars["close"] > high)
        | (bars["close"] < low)
    )
    return _issue("ohlc", "bars with open/close outside the high-low range", bad)


def _calendar_gaps(bars: pd.DataFrame, calendar: str) -> list[Issue | None]:
    sessions = mcal.get_calendar(calendar).valid_days(bars.index.min(), bars.index.max())
    sessions = pd.DatetimeIndex(sessions.tz_localize(None).astype("datetime64[ns]"))
    stored = pd.DatetimeIndex(bars.index.unique())
    return [
        _issue("missing", f"{calendar} sessions without a bar", sessions.difference(stored)),
        _issue("extra", f"bars on days {calendar} was closed", stored.difference(sessions)),
    ]


def _unexplained_jumps(bars: pd.DataFrame) -> Issue | None:
    move = bars["close"].pct_change().abs()
    jumps = (move > JUMP_THRESHOLD) & (bars["splits"] == 0)
    return _issue("jumps", f"close moves over {JUMP_THRESHOLD:.0%} without a split", jumps)


def _unadjusted_splits(bars: pd.DataFrame) -> Issue | None:
    # Close is split-adjusted, so a genuine split never moves it; a jump on the split
    # day means the bars before it were stored before the split was applied.
    move = bars["close"].pct_change().abs()
    stale = (move > JUMP_THRESHOLD) & (bars["splits"] != 0)
    return _issue("split", "splits with unadjusted history before them (re-fetch --full)", stale)
