from datetime import date

import pandas as pd
import pytest

from trading.data.bars import BAR_COLUMNS, EXTRA_COLUMNS, knowable_at
from trading.data.providers import ProviderError
from trading.data.providers.binance import (
    ArchiveFile,
    BinanceArchive,
    perp_symbol_for,
    spot_symbols,
)

from conftest import FakeArchive, make_klines

SPOT = "data/spot/monthly/klines"


def archive_with(symbol: str, granularity: str, start: str, end: str, **options) -> FakeArchive:
    archive = FakeArchive()
    archive.add_klines(SPOT, symbol, granularity, make_klines(start, end, granularity), **options)
    return archive


def test_daily_bars_have_the_normalized_shape_and_utc_date_labels():
    provider = BinanceArchive(transport=archive_with("BTCUSDT", "1d", "2024-11-20", "2025-02-10"))

    bars = provider.fetch("btcusdt", "1d")

    assert list(bars.columns) == [*BAR_COLUMNS, *EXTRA_COLUMNS]
    assert bars.index.name == "date" and bars.index.tz is None
    assert bars.index[0] == pd.Timestamp("2024-11-20") and bars.index[-1] == pd.Timestamp("2025-02-10")
    assert len(bars) == 83
    # Crypto has no dividends or splits, so the adjusted close is the close.
    assert (bars["adj_close"] == bars["close"]).all()
    assert (bars["dividends"] == 0).all() and (bars["splits"] == 0).all()
    assert bars["volume"].dtype == "float64"


def test_timestamps_switch_from_milliseconds_to_microseconds_without_a_seam():
    provider = BinanceArchive(transport=archive_with("BTCUSDT", "1h", "2024-12-30", "2025-01-02"))

    bars = provider.fetch("BTCUSDT", "1h")

    assert str(bars.index.tz) == "UTC"
    assert (bars.index.to_series().diff().dropna() == pd.Timedelta(hours=1)).all()
    assert len(bars) == 4 * 24


def test_files_with_and_without_a_header_row_parse_alike():
    plain = BinanceArchive(transport=archive_with("BTCUSDT", "1d", "2024-01-01", "2024-01-31"))
    headed = BinanceArchive(
        transport=archive_with("BTCUSDT", "1d", "2024-01-01", "2024-01-31", header=True)
    )

    pd.testing.assert_frame_equal(plain.fetch("BTCUSDT", "1d"), headed.fetch("BTCUSDT", "1d"))


def test_fetch_filters_inclusive_dates_and_downloads_only_overlapping_months():
    transport = archive_with("BTCUSDT", "1d", "2024-01-01", "2024-06-30")
    provider = BinanceArchive(transport=transport)

    bars = provider.fetch("BTCUSDT", "1d", start=date(2024, 3, 15), end=date(2024, 4, 2))

    assert bars.index[0] == pd.Timestamp("2024-03-15") and bars.index[-1] == pd.Timestamp("2024-04-02")
    downloaded = [url for url in transport.requests if url.endswith(".zip")]
    assert sorted(url[-11:-4] for url in downloaded) == ["2024-03", "2024-04"]


def test_unknown_symbol_gives_empty_bars():
    provider = BinanceArchive(transport=FakeArchive())

    assert provider.fetch("NOPEUSDT", "1d").empty


def test_a_corrupted_download_is_rejected():
    transport = archive_with("BTCUSDT", "1d", "2024-01-01", "2024-01-31")
    key = next(iter(transport.files))
    listing = transport.get  # the listing still advertises the original checksum

    class Corrupting:
        def get(self, url: str) -> bytes:
            content = listing(url)
            return content[:-1] + b"X" if url.endswith(".zip") else content

    provider = BinanceArchive(transport=Corrupting())

    with pytest.raises(ProviderError, match=f"checksum mismatch for {key}"):
        provider.fetch("BTCUSDT", "1d")


def test_verified_downloads_are_cached_and_reused(tmp_path):
    transport = archive_with("BTCUSDT", "1d", "2024-01-01", "2024-02-29")
    provider = BinanceArchive(raw_dir=tmp_path, transport=transport)
    provider.fetch("BTCUSDT", "1d")
    downloads = sum(url.endswith(".zip") for url in transport.requests)

    again = BinanceArchive(raw_dir=tmp_path, transport=transport).fetch("BTCUSDT", "1d")

    assert sum(url.endswith(".zip") for url in transport.requests) == downloads == 2
    assert len(again) == 60
    assert not list(tmp_path.rglob("*.partial"))


def test_a_zip_with_unexpected_contents_is_refused():
    import hashlib
    import io
    import zipfile

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        bundle.writestr("a.csv", "1\n")
        bundle.writestr("b.csv", "2\n")
    transport = FakeArchive()
    key = f"{SPOT}/BTCUSDT/1d/BTCUSDT-1d-2024-01.zip"
    transport.files[key] = buffer.getvalue()
    provider = BinanceArchive(transport=transport)

    with pytest.raises(ProviderError, match="unexpected contents"):
        provider.fetch("BTCUSDT", "1d")
    assert hashlib.md5(buffer.getvalue()).hexdigest()  # the checksum itself was fine


def test_a_reused_symbol_is_served_as_two_coins():
    transport = FakeArchive()
    old = make_klines("2022-04-01", "2022-05-13", price=80.0)
    new = make_klines("2022-05-31", "2022-07-31", price=6.0, seed=1)
    transport.add_klines(SPOT, "LUNAUSDT", "1d", pd.concat([old, new]))
    provider = BinanceArchive(transport=transport)

    later = provider.fetch("LUNAUSDT", "1d")
    earlier = provider.fetch("LUNAUSDT-2022", "1d")

    assert later.index[0] == pd.Timestamp("2022-05-31")
    assert earlier.index[-1] == pd.Timestamp("2022-05-13") and len(earlier) == len(old)
    assert spot_symbols(["LUNAUSDT", "BTCUSDT", "BTCBUSD"]) == ["BTCUSDT", "LUNAUSDT", "LUNAUSDT-2022"]


def test_a_redenomination_is_adjusted_like_a_split():
    transport = FakeArchive()
    frame = make_klines("2023-07-01", "2023-07-31", price=50.0, volatility=0.0)
    frame.loc["2023-07-21":, ["open", "high", "low", "close"]] /= 1000  # QUICK: 1 old = 1000 new
    frame.loc["2023-07-21":, "volume"] *= 1000
    transport.add_klines(SPOT, "QUICKUSDT", "1d", frame)
    provider = BinanceArchive(transport=transport)

    bars = provider.fetch("QUICKUSDT", "1d")

    assert bars["close"].pct_change().abs().max() < 1e-9  # no jump across the swap
    assert bars.loc["2023-07-21", "splits"] == 1000 and bars["splits"].sum() == 1000
    before, after = bars.loc["2023-07-20"], bars.loc["2023-07-21"]
    assert before["volume"] * before["close"] == pytest.approx(before["quote_volume"])
    assert after["volume"] * after["close"] == pytest.approx(after["quote_volume"])


def test_funding_events_are_rounded_to_the_minute_and_keep_their_interval():
    transport = FakeArchive()
    transport.add(
        "data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2024-01.zip",
        "calc_time,funding_interval_hours,last_funding_rate\n"
        "1704067200003,8,0.0001\n1704096000011,8,-0.0002\n",
    )
    provider = BinanceArchive(transport=transport)

    funding, files = provider.fetch_funding("BTCUSDT")

    assert list(funding.index) == [pd.Timestamp("2024-01-01 00:00", tz="UTC"), pd.Timestamp("2024-01-01 08:00", tz="UTC")]
    assert list(funding["rate"]) == [0.0001, -0.0002]
    assert list(funding["interval_hours"]) == [8, 8]
    assert [file.period for file in files] == ["2024-01"]


def test_premium_index_is_labelled_like_hourly_bars():
    transport = FakeArchive()
    frame = make_klines("2024-01-01", "2024-01-02", "1h", price=1.0)
    transport.add_klines("data/futures/um/monthly/premiumIndexKlines", "BTCUSDT", "1h", frame, header=True)
    provider = BinanceArchive(transport=transport)

    premium, _ = provider.fetch_premium("BTCUSDT")

    assert list(premium.columns) == ["open", "high", "low", "close"]
    assert premium.index[0] == pd.Timestamp("2024-01-01 00:00", tz="UTC") and len(premium) == 48


def test_open_interest_keeps_the_last_snapshot_of_each_hour():
    transport = FakeArchive()
    header = (
        "create_time,symbol,sum_open_interest,sum_open_interest_value,"
        "count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,"
        "count_long_short_ratio,sum_taker_long_short_vol_ratio\n"
    )
    rows = (
        "2024-01-01 00:05:00,BTCUSDT,100,1000,1.1,1.2,1.3,0.9\n"
        "2024-01-01 00:55:00,BTCUSDT,110,1100,1.1,1.2,1.3,0.9\n"
        "2024-01-01 01:00:00,BTCUSDT,120,1200,1.1,1.2,1.3,0.9\n"
    )
    key = "data/futures/um/daily/metrics/BTCUSDT/BTCUSDT-metrics-2024-01-01.zip"
    transport.add(key, header + rows)
    provider = BinanceArchive(transport=transport)

    interest, files = provider.fetch_open_interest("BTCUSDT")

    assert list(interest["open_interest"]) == [110, 120]
    assert list(interest.index) == [pd.Timestamp("2024-01-01 00:00", tz="UTC"), pd.Timestamp("2024-01-01 01:00", tz="UTC")]
    assert files[0].period == "2024-01-01"


def test_perpetual_contract_for_a_spot_pair():
    perps = ["BTCUSDT", "1000SHIBUSDT", "LUNAUSDT"]

    assert perp_symbol_for("BTCUSDT", perps) == "BTCUSDT"
    assert perp_symbol_for("SHIBUSDT", perps) == "1000SHIBUSDT"
    assert perp_symbol_for("LUNAUSDT-2022", perps) == "LUNAUSDT"
    assert perp_symbol_for("NOPEUSDT", perps) is None


def test_archive_file_period():
    assert ArchiveFile("a/BTCUSDT-1d-2024-01.zip", 1, "x").period == "2024-01"
    assert ArchiveFile("a/BTCUSDT-metrics-2024-01-05.zip", 1, "x").period == "2024-01-05"
    assert ArchiveFile("a/BTCUSDT-fundingRate-2024-01.zip", 1, "x").period == "2024-01"


def test_a_bar_is_knowable_when_it_closes():
    daily = pd.DatetimeIndex(["2024-01-01"])
    hourly = pd.DatetimeIndex(["2024-01-01 05:00"], tz="UTC")

    assert knowable_at(daily, "1d")[0] == pd.Timestamp("2024-01-02 00:00", tz="UTC")
    assert knowable_at(hourly, "1h")[0] == pd.Timestamp("2024-01-01 06:00", tz="UTC")


@pytest.mark.network
def test_real_archive_serves_verified_bitcoin_bars():
    provider = BinanceArchive()

    bars = provider.fetch("BTCUSDT", "1d", start=date(2021, 1, 1), end=date(2021, 1, 31))

    assert len(bars) == 31
    assert bars.loc["2021-01-01", "open"] == pytest.approx(28923.63)
