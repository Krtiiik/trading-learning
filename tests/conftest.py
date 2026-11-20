import hashlib
import io
import subprocess
import zipfile
from datetime import date
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd
import pytest

from trading.data.bars import BAR_COLUMNS, INDEX_NAME, empty_bars
from trading.data.pit_universe import UniverseRules
from trading.data.providers.base import ProviderError
from trading.data.providers.binance import DOWNLOAD_URL, LISTING_URL, BinanceArchive
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


# Crypto: an in-memory Binance archive and a small Store rebuilt from it.

KLINE_HEADER = (
    "open_time,open,high,low,close,volume,close_time,quote_volume,"
    "count,taker_buy_volume,taker_buy_quote_volume,ignore"
)


class FakeArchive:
    """A transport that serves bucket listings and zips from memory, like data.binance.vision."""

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}
        self.requests: list[str] = []

    def add(self, key: str, csv: str) -> None:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(key.rsplit("/", 1)[1].replace(".zip", ".csv"), csv)
        self.files[key] = buffer.getvalue()

    def get(self, url: str) -> bytes:
        self.requests.append(url)
        if url.startswith(LISTING_URL):
            return self._listing(parse_qs(urlparse(url).query)["prefix"][0]).encode()
        key = url.removeprefix(DOWNLOAD_URL)
        if key not in self.files:
            raise ProviderError(f"not in the Binance archive: {url}")
        return self.files[key]

    def _listing(self, prefix: str) -> str:
        folders, contents = set(), []
        for key, content in sorted(self.files.items()):
            if not key.startswith(prefix):
                continue
            rest = key[len(prefix) :]
            if "/" in rest:
                folders.add(prefix + rest.split("/", 1)[0] + "/")
            else:
                etag = hashlib.md5(content).hexdigest()
                contents.append(
                    f"<Contents><Key>{key}</Key><ETag>&quot;{etag}&quot;</ETag>"
                    f"<Size>{len(content)}</Size></Contents>"
                )
        common = "".join(
            f"<CommonPrefixes><Prefix>{folder}</Prefix></CommonPrefixes>" for folder in sorted(folders)
        )
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
            f"<IsTruncated>false</IsTruncated>{''.join(contents)}{common}</ListBucketResult>"
        )

    def add_klines(
        self, folder: str, symbol: str, granularity: str, frame: pd.DataFrame, header: bool = False
    ) -> None:
        """Monthly kline zips for `frame` (index: UTC open times; columns open..quote_volume).

        Like the real archive: milliseconds until 2024, microseconds from 2025.
        """
        step = 86_400_000 if granularity == "1d" else 3_600_000
        for month, rows in frame.groupby(frame.index.strftime("%Y-%m")):
            scale = 1000 if month >= "2025-01" else 1
            opened = rows.index.as_unit("ms").astype("int64")
            lines = [
                f"{t * scale},{r.open},{r.high},{r.low},{r.close},{r.volume},"
                f"{(t + step - 1) * scale},{r.quote_volume},100,{r.volume / 2},{r.quote_volume / 2},0"
                for t, r in zip(opened, rows.itertuples())
            ]
            if header:
                lines.insert(0, KLINE_HEADER)
            key = f"{folder}/{symbol}/{granularity}/{symbol}-{granularity}-{month}.zip"
            self.add(key, "\n".join(lines) + "\n")


def make_klines(
    start: str,
    end: str,
    granularity: str = "1d",
    price: float = 100.0,
    daily_quote_volume: float = 1e6,
    volatility: float = 0.03,
    seed: int = 0,
) -> pd.DataFrame:
    """A random-walk coin: tz-naive UTC open times, OHLC, base and quote volume."""
    per_day = 1 if granularity == "1d" else 24
    last = pd.Timestamp(end) + pd.Timedelta(hours=per_day - 1)
    index = pd.date_range(start, last, freq="D" if per_day == 1 else "h")
    rng = np.random.default_rng(seed)
    close = price * np.exp(np.cumsum(rng.normal(0, volatility / np.sqrt(per_day), len(index))))
    open_ = np.concatenate([[price], close[:-1]])
    quote_volume = np.full(len(index), daily_quote_volume / per_day)
    return pd.DataFrame(
        {
            "open": open_,
            "high": np.maximum(open_, close) * 1.001,
            "low": np.minimum(open_, close) * 0.999,
            "close": close,
            "volume": quote_volume / close,
            "quote_volume": quote_volume,
        },
        index=index,
    )


CRYPTO_START, CRYPTO_END = "2022-09-01", "2025-03-31"
CRYPTO_COINS = {
    # symbol: (first day, last day, daily quote volume, daily volatility)
    "BTCUSDT": (CRYPTO_START, CRYPTO_END, 9e8, 0.03),
    "ETHUSDT": (CRYPTO_START, CRYPTO_END, 5e8, 0.04),
    "SOLUSDT": (CRYPTO_START, CRYPTO_END, 2e8, 0.05),
    "ADAUSDT": (CRYPTO_START, CRYPTO_END, 1e8, 0.05),
    "XRPUSDT": (CRYPTO_START, CRYPTO_END, 5e7, 0.05),
    "DEADUSDT": (CRYPTO_START, "2023-03-20", 3e8, 0.06),
    "LATEUSDT": ("2024-06-10", CRYPTO_END, 4e8, 0.06),
    "USDCUSDT": (CRYPTO_START, CRYPTO_END, 8e8, 0.0002),
    "TINYUSDT": (CRYPTO_START, CRYPTO_END, 1e3, 0.05),
}
CRYPTO_RULES = UniverseRules(size=4, tier_two_count=1)
"""Top 4: BTC, ETH, DEAD, SOL at first; ADA once DEAD is delisted; LATE from 2024-08."""


def crypto_archive() -> FakeArchive:
    archive = FakeArchive()
    for number, (symbol, (first, last, volume, volatility)) in enumerate(CRYPTO_COINS.items()):
        for granularity in ("1d", "1h"):
            frame = make_klines(first, last, granularity, 100.0, volume, volatility, seed=number)
            archive.add_klines("data/spot/monthly/klines", symbol, granularity, frame)
    hours = pd.date_range(CRYPTO_START, pd.Timestamp(CRYPTO_END) + pd.Timedelta(hours=23), freq="h")
    events = hours[::8]
    for perp in ("BTCUSDT", "1000ADAUSDT"):
        premium = pd.DataFrame(
            {"open": 1e-4, "high": 2e-4, "low": 0.0, "close": np.arange(len(hours)) * 1e-8,
             "volume": 0.0, "quote_volume": 0.0},
            index=hours,
        )
        folder = "data/futures/um/monthly/premiumIndexKlines"
        archive.add_klines(folder, perp, "1h", premium, header=True)
        for month in sorted(set(events.strftime("%Y-%m"))):
            stamps = events[events.strftime("%Y-%m") == month]
            lines = ["calc_time,funding_interval_hours,last_funding_rate"]
            # A few milliseconds late, as in the real files.
            lines += [f"{stamp + 3},8,0.0001" for stamp in stamps.as_unit("ms").astype("int64")]
            key = f"data/futures/um/monthly/fundingRate/{perp}/{perp}-fundingRate-{month}.zip"
            archive.add(key, "\n".join(lines) + "\n")
    return archive


@pytest.fixture(scope="session")
def crypto_root(tmp_path_factory):
    """A Store rebuilt from the fake archive: daily and hourly bars, universe, funding, basis."""
    from trading.data.rebuild import rebuild

    root = tmp_path_factory.mktemp("crypto-store")
    provider = BinanceArchive(raw_dir=root / "raw" / "binance", transport=crypto_archive(), workers=2)
    rebuild(root, provider, rules=CRYPTO_RULES, log=lambda line: None, workers=2)
    return root


def git(repo, *arguments: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *arguments], capture_output=True, text=True, check=True
    )
    return done.stdout


@pytest.fixture
def repo(tmp_path):
    """An empty git repository with a `research/` records folder."""
    path = tmp_path / "repo"
    (path / "research" / "hypotheses").mkdir(parents=True)
    git(path, "init", "-q")
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    git(path, "config", "commit.gpgsign", "false")
    (path / "README.md").write_text("test repository\n")
    git(path, "add", ".")
    git(path, "commit", "-q", "-m", "start")
    return path
