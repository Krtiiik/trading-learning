"""The Store's crypto side: manifests, the point-in-time universe, and the one-command rebuild."""

import numpy as np
import pandas as pd
import pytest

from trading.cli import main
from trading.data.manifest import (
    ManifestError,
    build_manifest,
    content_hash,
    dataset_id,
    read_manifest,
    verify_manifest,
)
from trading.data.pit_universe import (
    UniverseRules,
    base_asset,
    build_universe,
    exclusion,
    membership_panel,
)
from trading.data.providers.binance import BinanceArchive
from trading.data.rebuild import read_universe, rebuild
from trading.data.storage import BarStore, SeriesStore, load_bars, load_panel

from conftest import CRYPTO_RULES, crypto_archive, make_bars

# Manifests


def test_manifest_gives_a_dataset_an_identity_that_follows_its_content(store):
    store.write("SPY", "1d", make_bars("2024-01-02", 5))
    first = build_manifest(store.root, "1d", "fake")

    store.write("SPY", "1d", make_bars("2024-01-02", 5))  # same content, rewritten
    same = build_manifest(store.root, "1d", "fake")
    store.write("SPY", "1d", make_bars("2024-01-02", 6))
    changed = build_manifest(store.root, "1d", "fake")

    assert first.id == same.id != changed.id
    assert first.files["SPY.parquet"].rows == 5
    assert first.files["SPY.parquet"].first.startswith("2024-01-02")
    assert read_manifest(store.root, "1d").id == changed.id


def test_manifest_records_where_the_rows_came_from(store):
    store.write("SPY", "1d", make_bars("2024-01-02", 5))

    manifest = build_manifest(store.root, "1d", "fake", {"SPY.parquet": [("a.zip", "md5a"), ("b.zip", "md5b")]})

    assert manifest.files["SPY.parquet"].source_files == 2
    assert len(manifest.files["SPY.parquet"].source_digest) == 64


def test_changed_missing_and_extra_files_are_detected(store):
    store.write("SPY", "1d", make_bars("2024-01-02", 5))
    store.write("QQQ", "1d", make_bars("2024-01-02", 5))
    build_manifest(store.root, "1d", "fake")
    assert verify_manifest(store.root, "1d") == []
    assert verify_manifest(store.root, "1d", deep=True) == []

    store.write("SPY", "1d", make_bars("2024-01-02", 7))
    store.path("QQQ", "1d").unlink()
    store.write("IWM", "1d", make_bars("2024-01-02", 5))

    problems = " | ".join(verify_manifest(store.root, "1d", deep=True))
    assert "SPY.parquet: content differs" in problems
    assert "QQQ.parquet: listed in the manifest but missing" in problems
    assert "IWM.parquet: on disk but not in the manifest" in problems
    with pytest.raises(ManifestError, match="does not match its manifest"):
        dataset_id(store.root, "1d")


def test_dataset_without_manifest_explains_what_to_run(store):
    with pytest.raises(ManifestError, match="trading rebuild"):
        dataset_id(store.root, "binance/spot/1d")


def test_content_hash_sees_values_index_and_column_names():
    bars = make_bars("2024-01-02", 5)
    moved = bars.copy()
    moved.index = moved.index + pd.Timedelta(days=1)

    assert content_hash(bars) == content_hash(bars.copy())
    assert content_hash(bars) != content_hash(moved)
    assert content_hash(bars) != content_hash(bars.rename(columns={"open": "o"}))
    assert content_hash(bars) != content_hash(bars.assign(close=bars["close"] + 1e-9))


def test_fetch_writes_a_manifest_for_the_etf_bars(tmp_path, capsys):
    from conftest import FakeProvider

    provider = FakeProvider({"SPY": make_bars("2024-01-02", 9)})

    main(["fetch", "--symbols", "SPY", "--data-dir", str(tmp_path)], provider)

    assert "Dataset 1d: 1 files, id " in capsys.readouterr().out
    assert verify_manifest(tmp_path, "1d") == []


# Store


def test_store_keeps_extra_columns_and_separates_datasets(store):
    bars = make_bars("2024-01-02", 3).assign(quote_volume=5.0, unrelated=1.0)
    crypto = BarStore(store.root, "binance/spot")

    crypto.write("btcusdt", "1d", bars)

    assert crypto.path("BTCUSDT", "1d") == store.root / "binance" / "spot" / "1d" / "BTCUSDT.parquet"
    assert list(crypto.read("BTCUSDT", "1d").columns)[-1] == "quote_volume"
    assert "unrelated" not in crypto.read("BTCUSDT", "1d").columns
    assert store.symbols("1d") == [] or "BTCUSDT" not in store.symbols("1d")
    assert load_panel(["BTCUSDT"], field="quote_volume", store=crypto)["BTCUSDT"].iloc[0] == 5.0


def test_an_end_day_includes_all_of_that_days_hourly_bars(crypto_root):
    store = BarStore(crypto_root, "binance/spot")

    bars = load_bars("BTCUSDT", "1h", start="2024-01-02", end="2024-01-03", store=store)

    assert len(bars) == 48
    assert bars.index[-1] == pd.Timestamp("2024-01-03 23:00", tz="UTC")


def test_series_store_round_trip(tmp_path):
    series = pd.DataFrame(
        {"rate": [0.1, 0.2]},
        index=pd.DatetimeIndex(["2024-01-01", "2024-01-02"], tz="UTC", name="time"),
    )
    store = SeriesStore("binance/funding", tmp_path)

    store.write("btcusdt", series)

    pd.testing.assert_frame_equal(store.read("BTCUSDT"), series, check_freq=False)
    assert store.symbols() == ["BTCUSDT"]
    with pytest.raises(FileNotFoundError):
        store.read("ETHUSDT")


# Point-in-time universe


def daily_panel(values: dict[str, list[float]], start: str = "2024-01-01") -> pd.DataFrame:
    length = len(next(iter(values.values())))
    return pd.DataFrame(values, index=pd.date_range(start, periods=length, freq="D"))


def wiggly(length: int, seed: int) -> list[float]:
    rng = np.random.default_rng(seed)
    return list(100 * np.exp(np.cumsum(rng.normal(0, 0.03, length))))


def test_universe_ranks_by_trailing_volume_using_only_earlier_days():
    days = 70
    volume = daily_panel({
        "BTCUSDT": [100.0] * days,
        "AAAUSDT": [50.0] * days,
        # CCC trades nothing until 1 February, then more than anyone.
        "CCCUSDT": [1.0] * 31 + [1000.0] * (days - 31),
    })
    close = daily_panel({symbol: wiggly(days, seed) for seed, symbol in enumerate(volume)})

    universe = build_universe(volume, close, UniverseRules(size=2, tier_two_count=1))

    february = universe[universe["date"] == "2024-02-01"]
    march = universe[universe["date"] == "2024-03-01"]
    # On 1 February only January's bars count, so CCC's surge that day is not yet known.
    assert list(february["symbol"]) == ["BTCUSDT", "AAAUSDT"]
    assert list(march["symbol"]) == ["CCCUSDT", "BTCUSDT"]
    assert list(march["rank"]) == [1, 2]
    assert february["quote_volume"].iloc[0] == pytest.approx(30 * 100.0)


def test_a_pair_needs_a_bar_on_every_day_of_the_lookback():
    days = 62
    volume = daily_panel({"BTCUSDT": [100.0] * days, "NEWUSDT": [np.nan] * 20 + [900.0] * (days - 20)})
    volume.loc["2024-02-20", "BTCUSDT"] = np.nan  # one missing day
    close = daily_panel({"BTCUSDT": wiggly(days, 1), "NEWUSDT": wiggly(days, 2)}).where(volume.notna())

    universe = build_universe(volume, close, UniverseRules(size=5))

    assert list(universe[universe["date"] == "2024-02-01"]["symbol"]) == ["BTCUSDT"]
    assert list(universe[universe["date"] == "2024-03-01"]["symbol"]) == ["NEWUSDT"]


def test_stablecoins_wrapped_leveraged_and_pegged_pairs_are_never_members():
    days = 40
    names = ["BTCUSDT", "USDCUSDT", "WBTCUSDT", "BTCUPUSDT", "ETHBULLUSDT", "NVDABUSDT", "JUPUSDT", "NEWPEGUSDT"]
    volume = daily_panel({symbol: [100.0] * days for symbol in names})
    close = daily_panel({symbol: wiggly(days, seed) for seed, symbol in enumerate(names)})
    close["NEWPEGUSDT"] = 1.0 + 0.0001 * np.sin(np.arange(days))  # unlisted stablecoin: caught by its calm

    universe = build_universe(volume, close)

    assert sorted(universe["symbol"].unique()) == ["BTCUSDT", "JUPUSDT"]
    assert exclusion("USDCUSDT") == "stablecoin or fiat"
    assert exclusion("btcupusdt") == "leveraged token"
    assert exclusion("JUPUSDT") is None
    assert base_asset("LUNAUSDT-2022") == "LUNA"


def test_liquidity_tiers_follow_the_ranking():
    days = 40
    names = ["ETHUSDT", "AAAUSDT", "CCCUSDT", "BTCUSDT", "DDDUSDT"]
    volume = daily_panel({symbol: [float(10 - rank)] * days for rank, symbol in enumerate(names)})
    close = daily_panel({symbol: wiggly(days, seed) for seed, symbol in enumerate(names)})

    universe = build_universe(volume, close, UniverseRules(size=5, tier_two_count=2))

    tiers = dict(zip(universe["symbol"], universe["tier"]))
    assert tiers == {"ETHUSDT": 1, "AAAUSDT": 2, "CCCUSDT": 2, "BTCUSDT": 1, "DDDUSDT": 3}


def test_membership_panel_takes_the_last_reconstitution_at_or_before_each_bar():
    universe = pd.DataFrame({
        "date": pd.to_datetime(["2024-02-01", "2024-02-01", "2024-03-01"]),
        "symbol": ["BTCUSDT", "AAAUSDT", "BTCUSDT"],
        "rank": [1, 2, 1],
        "quote_volume": [1.0, 1.0, 1.0],
        "tier": [1, 2, 1],
    })
    hours = pd.DatetimeIndex(
        ["2024-01-31 23:00", "2024-02-01 00:00", "2024-02-29 23:00", "2024-03-01 00:00"], tz="UTC"
    )

    member, tier = membership_panel(universe, hours, ["BTCUSDT", "AAAUSDT", "ZZZUSDT"])

    assert member.tolist() == [[False] * 3, [True, True, False], [True, True, False], [True, False, False]]
    assert tier.tolist() == [[3, 3, 3], [1, 2, 3], [1, 2, 3], [1, 3, 3]]


# Rebuild


def test_rebuild_builds_every_dataset_with_a_manifest(crypto_root):
    for dataset in ("binance/spot/1d", "binance/spot/1h", "binance/universe", "binance/funding", "binance/premium/1h"):
        assert verify_manifest(crypto_root, dataset, deep=True) == []
    daily = BarStore(crypto_root, "binance/spot")
    assert "USDCUSDT" in daily.symbols("1d")  # every USDT pair is kept as daily bars
    assert read_manifest(crypto_root, "binance/spot/1d").files["BTCUSDT.parquet"].source_files == 31


def test_rebuilt_universe_keeps_delisted_coins_and_admits_late_ones(crypto_root):
    universe = read_universe(crypto_root)
    members = universe.groupby("date")["symbol"].apply(list)

    assert members[pd.Timestamp("2022-10-01")] == ["BTCUSDT", "ETHUSDT", "DEADUSDT", "SOLUSDT"]
    assert members[pd.Timestamp("2023-04-01")] == ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"]
    assert members[pd.Timestamp("2024-08-01")] == ["BTCUSDT", "ETHUSDT", "LATEUSDT", "SOLUSDT"]
    assert "USDCUSDT" not in set(universe["symbol"]) and "TINYUSDT" not in set(universe["symbol"])
    assert universe["date"].max() == pd.Timestamp("2025-04-01")


def test_hourly_bars_and_perpetual_series_exist_only_for_members(crypto_root):
    hourly = BarStore(crypto_root, "binance/spot").symbols("1h")

    assert hourly == ["ADAUSDT", "BTCUSDT", "DEADUSDT", "ETHUSDT", "LATEUSDT", "SOLUSDT"]
    # Stored under the spot symbol, although ADA's contract is quoted per 1000 coins.
    assert SeriesStore("binance/funding", crypto_root).symbols() == ["ADAUSDT", "BTCUSDT"]
    funding = SeriesStore("binance/funding", crypto_root).read("ADAUSDT")
    assert funding.index[1] - funding.index[0] == pd.Timedelta(hours=8)


def test_rebuilding_twice_gives_the_same_dataset_ids_and_drops_stale_files(crypto_root, tmp_path):
    provider = BinanceArchive(transport=crypto_archive(), workers=2)
    stale = BarStore(tmp_path, "binance/spot")
    stale.write("GONEUSDT", "1d", make_bars("2024-01-02", 3))

    manifests = rebuild(tmp_path, provider, steps=("spot-1d", "universe"), rules=CRYPTO_RULES, log=lambda line: None)

    assert "GONEUSDT" not in stale.symbols("1d")
    for dataset, manifest in manifests.items():
        assert manifest.id == read_manifest(crypto_root, dataset).id


def test_rebuild_command_reports_each_dataset(tmp_path, capsys):
    provider = BinanceArchive(transport=crypto_archive(), workers=2)

    code = main(["rebuild", "--steps", "spot-1d", "universe", "--data-dir", str(tmp_path)], provider)

    output = capsys.readouterr().out
    assert code == 0
    assert "binance/spot/1d: 9 files, id " in output
    assert "pairs were ever members" in output
    assert main(["verify", "--data-dir", str(tmp_path)]) == 0
