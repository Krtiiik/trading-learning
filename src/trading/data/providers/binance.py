"""Binance public archive (data.binance.vision): bulk monthly and daily files, no API key.

Everything specific to the archive stays in this module: the bucket listing, checksum
verification, CSV layouts that changed over the years (headers appear in later files, spot
timestamps switch from milliseconds to microseconds in 2025), symbols reused for a different
coin, and the perpetual contracts quoted per 1000 coins. Downloaded files are data: they are
unzipped and parsed, never executed.
"""

import hashlib
import io
import threading
import uuid
import xml.etree.ElementTree as ElementTree
import zipfile
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Literal, Protocol
from urllib.parse import urlencode

import pandas as pd

from trading.data.bars import BAR_COLUMNS, EXTRA_COLUMNS, INDEX_NAME, Granularity, empty_bars
from trading.data.providers.base import ProviderError

LISTING_URL = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
DOWNLOAD_URL = "https://data.binance.vision/"
_S3 = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

Market = Literal["spot", "um"]
"""`spot`, or `um` for USDT-margined perpetual futures."""

KLINE_COLUMNS = (
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "trades",
    "taker_buy_volume",
    "taker_buy_quote_volume",
    "ignore",
)

MAX_UNZIPPED_BYTES = 512 * 1024 * 1024
"""Refuse archive members larger than this; the largest real file is a few megabytes."""

SYMBOL_REUSE: dict[str, tuple[str, str]] = {
    # symbol: (first day of the coin that owns the symbol today, name for the earlier coin)
    "LUNAUSDT": ("2022-05-28", "LUNAUSDT-2022"),
    "USDSUSDT": ("2026-01-01", "USDSUSDT-2020"),
}
"""Spot symbols Binance reused for a different coin. Bars before the date belong to the
earlier coin and are served under the second name; the plain symbol serves the later coin."""

REDENOMINATIONS: dict[str, tuple[str, float]] = {
    # symbol: (first day at the new denomination, new coins per old coin)
    "BTCSTUSDT": ("2021-03-19", 10),
    "COCOSUSDT": ("2021-01-23", 0.001),
    "DREPUSDT": ("2021-04-02", 0.01),
    "SUNUSDT": ("2021-06-18", 1000),
    "VIDTUSDT": ("2022-11-09", 10),
    "BNXUSDT": ("2023-02-22", 100),
    "QUICKUSDT": ("2023-07-21", 1000),
    "STRAXUSDT": ("2024-03-28", 10),
}
"""Token swaps that kept the symbol but changed the unit. They are treated like stock splits:
earlier prices are divided by the ratio (volumes multiplied) and the ratio is recorded in
`splits` on the first bar at the new denomination."""

_PERP_MULTIPLIERS = ("", "1000", "1000000", "1M")


class Transport(Protocol):
    """Fetches the bytes behind a URL. Replaced by an in-memory fake in tests."""

    def get(self, url: str) -> bytes: ...


class HttpTransport:
    """HTTPS through one pooled `requests` session, with a few retries."""

    def __init__(self, pool_size: int = 32, attempts: int = 4, timeout: float = 60.0) -> None:
        import requests
        from requests.adapters import HTTPAdapter

        self._session = requests.Session()
        self._session.mount(
            "https://", HTTPAdapter(pool_connections=4, pool_maxsize=pool_size, max_retries=0)
        )
        self._attempts = attempts
        self._timeout = timeout

    def get(self, url: str) -> bytes:
        error: Exception | None = None
        for _ in range(self._attempts):
            try:
                response = self._session.get(url, timeout=self._timeout)
                if response.status_code == 404:
                    raise ProviderError(f"not in the Binance archive: {url}")
                response.raise_for_status()
                return response.content
            except ProviderError:
                raise
            except Exception as caught:  # network errors are retried, then reported
                error = caught
        raise ProviderError(f"Binance archive request failed: {url}: {error}") from error


@dataclass(frozen=True)
class ArchiveFile:
    """One zip in the archive, as the bucket listing describes it."""

    key: str
    size: int
    etag: str

    @property
    def period(self) -> str:
        """`YYYY-MM` for a monthly file, `YYYY-MM-DD` for a daily one."""
        stem = self.key.rsplit("/", 1)[1].removesuffix(".zip")
        parts = stem.split("-")
        return "-".join(parts[-3:] if len(parts[-3]) == 4 and parts[-3].isdigit() else parts[-2:])


class BinanceArchive:
    """Provider of spot bars, and of perpetual-futures series used as predictors only."""

    name = "binance"

    def __init__(
        self,
        raw_dir: Path | None = None,
        transport: Transport | None = None,
        workers: int = 16,
    ) -> None:
        self.raw_dir = Path(raw_dir) if raw_dir is not None else None
        self._transport = transport
        self._workers = workers
        self._lock = threading.Lock()

    # Listing

    def list_symbols(self, market: Market, kind: str, frequency: str = "monthly") -> list[str]:
        """Every symbol that has files of this kind, delisted ones included."""
        prefix = f"{_market_path(market)}/{frequency}/{kind}/"
        prefixes, _ = self._list(prefix)
        return sorted(item[len(prefix) :].strip("/") for item in prefixes)

    def list_files(self, prefix: str) -> list[ArchiveFile]:
        """The zips directly under `prefix`, oldest first."""
        _, files = self._list(prefix)
        return sorted((file for file in files if file.key.endswith(".zip")), key=lambda f: f.key)

    def _list(self, prefix: str) -> tuple[list[str], list[ArchiveFile]]:
        prefixes: list[str] = []
        files: list[ArchiveFile] = []
        marker = ""
        while True:
            query = {"delimiter": "/", "prefix": prefix} | ({"marker": marker} if marker else {})
            try:
                root = ElementTree.fromstring(self._get(f"{LISTING_URL}?{urlencode(query)}"))
            except ElementTree.ParseError as error:
                raise ProviderError(f"unreadable Binance archive listing for {prefix}") from error
            prefixes += [node.text or "" for node in root.findall("s3:CommonPrefixes/s3:Prefix", _S3)]
            for node in root.findall("s3:Contents", _S3):
                files.append(
                    ArchiveFile(
                        key=node.findtext("s3:Key", "", _S3),
                        size=int(node.findtext("s3:Size", "0", _S3)),
                        etag=node.findtext("s3:ETag", "", _S3).strip('"'),
                    )
                )
            if root.findtext("s3:IsTruncated", "false", _S3) != "true":
                return prefixes, files
            marker = root.findtext("s3:NextMarker", "", _S3) or (
                files[-1].key if files else prefixes[-1]
            )

    # Download

    def download(self, file: ArchiveFile) -> bytes:
        """The verified bytes of one archive file, from the raw cache when it is intact."""
        cached = self.raw_dir / file.key if self.raw_dir is not None else None
        if cached is not None and cached.is_file():
            content = cached.read_bytes()
            if self._matches(file, content):
                return content
        content = self._get(DOWNLOAD_URL + file.key)
        if not self._matches(file, content):
            raise ProviderError(f"checksum mismatch for {file.key}")
        if cached is not None:
            cached.parent.mkdir(parents=True, exist_ok=True)
            # Two symbols can share an archive file (a reused symbol), so each writer gets its
            # own partial file; whoever swaps second finds the verified file already in place.
            partial = cached.with_name(f"{cached.name}.{uuid.uuid4().hex}.partial")
            partial.write_bytes(content)
            try:
                partial.replace(cached)
            except PermissionError:
                partial.unlink(missing_ok=True)
                if not cached.is_file():
                    raise
        return content

    def _matches(self, file: ArchiveFile, content: bytes) -> bool:
        if "-" not in file.etag:
            # For a single-part upload the listing's ETag is the MD5 of the object.
            return hashlib.md5(content, usedforsecurity=False).hexdigest() == file.etag
        # Multipart uploads have no usable ETag; the archive's own SHA-256 file decides.
        expected = self._get(DOWNLOAD_URL + file.key + ".CHECKSUM").split()[0].decode()
        return hashlib.sha256(content).hexdigest() == expected

    def _get(self, url: str) -> bytes:
        if self._transport is None:
            with self._lock:
                if self._transport is None:
                    self._transport = HttpTransport(pool_size=self._workers * 2)
        return self._transport.get(url)

    def _frames[T](self, files: Iterable[ArchiveFile], parse: Callable[[bytes], T]) -> list[T]:
        files = list(files)
        with ThreadPoolExecutor(self._workers) as pool:
            return list(pool.map(lambda file: parse(_unzip(self.download(file), file.key)), files))

    # Spot bars (the Provider protocol)

    def fetch(
        self,
        symbol: str,
        granularity: Granularity,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Spot bars for `symbol` from the monthly files, `start` and `end` inclusive.

        The archive publishes a month after it ends, so the newest bars are those of the last
        complete month. Daily labels are tz-naive UTC dates, hourly labels tz-aware UTC instants.
        """
        return self.fetch_with_sources(symbol, granularity, start, end)[0]

    def fetch_with_sources(
        self,
        symbol: str,
        granularity: Granularity,
        start: date | None = None,
        end: date | None = None,
    ) -> tuple[pd.DataFrame, list[ArchiveFile]]:
        symbol = symbol.upper()
        archive_symbol, since, until = _resolve_reuse(symbol)
        files = self.list_files(f"data/spot/monthly/klines/{archive_symbol}/{granularity}/")
        files = [file for file in files if _overlaps(file.period, start, end)]
        if not files:
            return empty_bars(), []
        klines = pd.concat(self._frames(files, _parse_klines))
        bars = _redenominate(_to_bars(klines, granularity), archive_symbol)
        lower = _later(_timestamp(start, bars.index), _timestamp(since, bars.index))
        upper = _earlier(_day_end(end, bars.index), _day_end(until, bars.index))
        return bars.loc[lower:upper], files

    # Perpetual-futures series (predictors only; no perpetual positions are ever held)

    def perp_symbols(self) -> list[str]:
        return self.list_symbols("um", "fundingRate")

    def fetch_funding(self, perp_symbol: str) -> tuple[pd.DataFrame, list[ArchiveFile]]:
        """Funding events: index `time` (UTC), columns `rate` and `interval_hours`."""
        prefix = f"data/futures/um/monthly/fundingRate/{perp_symbol.upper()}/"
        files = self.list_files(prefix)
        if not files:
            return _empty_series("time", ("rate", "interval_hours")), []
        raw = pd.concat(self._frames(files, _parse_funding))
        index = pd.to_datetime(raw["calc_time"], unit="ms", utc=True).dt.round("1min")
        frame = pd.DataFrame(
            {
                "rate": raw["last_funding_rate"].to_numpy("float64"),
                "interval_hours": raw["funding_interval_hours"].to_numpy("float64"),
            },
            index=pd.DatetimeIndex(index, name="time"),
        )
        return _tidy(frame), files

    def fetch_premium(
        self, perp_symbol: str, granularity: Granularity = "1h"
    ) -> tuple[pd.DataFrame, list[ArchiveFile]]:
        """Premium index bars: the perpetual's basis over the index price, as a fraction.

        Index `date` labelled like spot bars of the same granularity; columns open/high/low/close.
        """
        prefix = f"data/futures/um/monthly/premiumIndexKlines/{perp_symbol.upper()}/{granularity}/"
        files = self.list_files(prefix)
        columns = ("open", "high", "low", "close")
        if not files:
            return _empty_series(INDEX_NAME, columns), []
        klines = pd.concat(self._frames(files, _parse_klines))
        frame = klines[list(columns)].astype("float64")
        frame.index = _bar_index(klines["open_time"], granularity)
        return _tidy(frame), files

    def fetch_open_interest(self, perp_symbol: str) -> tuple[pd.DataFrame, list[ArchiveFile]]:
        """Hourly open interest and positioning ratios from the daily `metrics` files.

        The archive holds 5-minute snapshots; each hour keeps its last snapshot and is labelled
        by the hour's open, so it is knowable at the same moment as that hour's spot bar.
        """
        files = self.list_files(f"data/futures/um/daily/metrics/{perp_symbol.upper()}/")
        files = [file for file in files if file.period >= "2000"]  # a few stray 1993-dated files
        if not files:
            return _empty_series(INDEX_NAME, tuple(_METRICS.values())), []
        raw = pd.concat(self._frames(files, _parse_metrics))
        raw = raw.dropna(subset=["create_time"]).sort_values("create_time")
        raw = raw.set_index(pd.DatetimeIndex(raw.pop("create_time"), name=INDEX_NAME))
        hourly = raw.groupby(raw.index.floor("1h")).last()
        return _tidy(hourly), files


def perp_symbol_for(spot_symbol: str, perp_symbols: Iterable[str]) -> str | None:
    """The perpetual contract tracking a spot pair, if any (`SHIBUSDT` -> `1000SHIBUSDT`)."""
    available = set(perp_symbols)
    plain = _resolve_reuse(spot_symbol.upper())[0]
    return next((m + plain for m in _PERP_MULTIPLIERS if m + plain in available), None)


def spot_symbols(archive_symbols: Iterable[str], quote: str = "USDT") -> list[str]:
    """Store symbols for the archive's pairs in `quote`, with reused symbols split in two."""
    symbols = [symbol for symbol in archive_symbols if symbol.endswith(quote)]
    earlier = [SYMBOL_REUSE[symbol][1] for symbol in symbols if symbol in SYMBOL_REUSE]
    return sorted(symbols + earlier)


def _market_path(market: Market) -> str:
    return "data/spot" if market == "spot" else "data/futures/um"


def _resolve_reuse(symbol: str) -> tuple[str, date | None, date | None]:
    """Archive symbol plus the first and last day that belong to the requested coin."""
    for archive_symbol, (first_day, earlier_name) in SYMBOL_REUSE.items():
        boundary = date.fromisoformat(first_day)
        if symbol == archive_symbol:
            return archive_symbol, boundary, None
        if symbol == earlier_name:
            return archive_symbol, None, boundary - timedelta(days=1)
    return symbol, None, None


def _overlaps(period: str, start: date | None, end: date | None) -> bool:
    month = period[:7]
    return (start is None or month >= f"{start:%Y-%m}") and (end is None or month <= f"{end:%Y-%m}")


def _unzip(content: bytes, key: str) -> bytes:
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            members = archive.infolist()
            if len(members) != 1 or members[0].file_size > MAX_UNZIPPED_BYTES:
                raise ProviderError(f"unexpected contents in {key}")
            return archive.read(members[0])
    except zipfile.BadZipFile as error:
        raise ProviderError(f"{key} is not a zip file") from error


def _has_header(raw: bytes) -> bool:
    return raw[:1].isalpha()


def _parse_klines(raw: bytes) -> pd.DataFrame:
    return pd.read_csv(
        io.BytesIO(raw), header=None, names=list(KLINE_COLUMNS), skiprows=int(_has_header(raw))
    )


def _parse_funding(raw: bytes) -> pd.DataFrame:
    names = ["calc_time", "funding_interval_hours", "last_funding_rate"]
    return pd.read_csv(io.BytesIO(raw), header=None, names=names, skiprows=int(_has_header(raw)))


_METRICS = {
    "sum_open_interest": "open_interest",
    "sum_open_interest_value": "open_interest_value",
    "count_toptrader_long_short_ratio": "top_trader_account_ratio",
    "sum_toptrader_long_short_ratio": "top_trader_position_ratio",
    "count_long_short_ratio": "account_ratio",
    "sum_taker_long_short_vol_ratio": "taker_volume_ratio",
}


def _parse_metrics(raw: bytes) -> pd.DataFrame:
    frame = pd.read_csv(io.BytesIO(raw))
    times = pd.to_datetime(frame["create_time"], utc=True, errors="coerce")
    values = frame[list(_METRICS)].apply(pd.to_numeric, errors="coerce").rename(columns=_METRICS)
    return values.assign(create_time=times.astype("datetime64[ns, UTC]"))


def _bar_index(open_time: pd.Series, granularity: Granularity) -> pd.DatetimeIndex:
    values = open_time.to_numpy("int64")
    # Spot files switch from milliseconds to microseconds at 2025-01-01; tell them apart by size.
    micro = values >= 10**14
    nanos = values * 1_000_000
    nanos[micro] = values[micro] * 1_000
    index = pd.DatetimeIndex(nanos.astype("datetime64[ns]"), name=INDEX_NAME)
    if granularity == "1d":
        return index.normalize()
    return index.tz_localize("UTC")


def _to_bars(klines: pd.DataFrame, granularity: Granularity) -> pd.DataFrame:
    frame = klines[["open", "high", "low", "close", "volume", *EXTRA_COLUMNS]].astype("float64")
    frame.index = _bar_index(klines["open_time"], granularity)
    # Crypto has no dividends or splits: the adjusted close is the close.
    frame = frame.assign(adj_close=frame["close"], dividends=0.0, splits=0.0)
    return _tidy(frame[[*BAR_COLUMNS, *EXTRA_COLUMNS]])


def _redenominate(bars: pd.DataFrame, symbol: str) -> pd.DataFrame:
    if symbol not in REDENOMINATIONS or bars.empty:
        return bars
    first_day, ratio = REDENOMINATIONS[symbol]
    boundary = pd.Timestamp(first_day, tz=bars.index.tz)
    before = bars.index < boundary
    bars = bars.copy()
    bars.loc[before, ["open", "high", "low", "close", "adj_close"]] /= ratio
    bars.loc[before, ["volume", "taker_buy_volume"]] *= ratio
    after = bars.index[~before]
    if len(after):
        bars.loc[after[0], "splits"] = ratio
    return bars


def _tidy(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[~frame.index.duplicated(keep="last")].sort_index()


def _empty_series(index_name: str, columns: tuple[str, ...]) -> pd.DataFrame:
    index = pd.DatetimeIndex([], name=index_name, dtype="datetime64[ns, UTC]")
    return pd.DataFrame({column: pd.Series(dtype="float64") for column in columns}, index=index)


def _timestamp(day: date | None, index: pd.DatetimeIndex) -> pd.Timestamp | None:
    if day is None:
        return None
    return pd.Timestamp(day, tz=index.tz)


def _day_end(day: date | None, index: pd.DatetimeIndex) -> pd.Timestamp | None:
    if day is None:
        return None
    return pd.Timestamp(day, tz=index.tz) + pd.Timedelta(days=1) - pd.Timedelta(1, "ns")


def _later(a: pd.Timestamp | None, b: pd.Timestamp | None) -> pd.Timestamp | None:
    return max((value for value in (a, b) if value is not None), default=None)


def _earlier(a: pd.Timestamp | None, b: pd.Timestamp | None) -> pd.Timestamp | None:
    return min((value for value in (a, b) if value is not None), default=None)
