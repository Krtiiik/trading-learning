import pandas as pd
import pytest

from trading.data.storage import BarStore, default_data_dir, load_bars, load_panel

from conftest import make_bars


def test_write_then_read_round_trips_bars(store):
    bars = make_bars("2024-01-02", 5)

    store.write("spy", "1d", bars)

    pd.testing.assert_frame_equal(store.read("SPY", "1d"), bars, check_freq=False)
    assert store.path("spy", "1d") == store.root / "1d" / "SPY.parquet"
    assert store.symbols("1d") == ["SPY"]


def test_read_of_unknown_symbol_is_empty(store):
    assert store.read("SPY", "1d").empty


def test_unsupported_granularity_is_rejected(store):
    with pytest.raises(ValueError, match="unsupported granularity"):
        store.path("SPY", "1m")


def test_data_dir_can_be_overridden_by_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("TRADING_DATA_DIR", str(tmp_path))

    assert default_data_dir() == tmp_path
    assert BarStore().root == tmp_path


def test_load_bars_filters_inclusive_date_range(store):
    store.write("SPY", "1d", make_bars("2024-01-01", 10))

    bars = load_bars("SPY", start="2024-01-03", end="2024-01-05", store=store)

    assert list(bars.index.strftime("%Y-%m-%d")) == ["2024-01-03", "2024-01-04", "2024-01-05"]


def test_load_bars_explains_how_to_fetch_missing_data(store):
    with pytest.raises(FileNotFoundError, match="trading fetch --symbols QQQ"):
        load_bars("qqq", store=store)


def test_load_panel_aligns_symbols_on_date(store):
    store.write("SPY", "1d", make_bars("2024-01-01", 5, close=100))
    store.write("QQQ", "1d", make_bars("2024-01-03", 3, close=50))

    panel = load_panel(["spy", "qqq"], field="close", store=store)

    assert list(panel.columns) == ["SPY", "QQQ"]
    assert len(panel) == 5
    assert panel["QQQ"].isna().sum() == 2
    assert panel.loc["2024-01-03", "QQQ"] == 50


def test_load_panel_rejects_unknown_field(store):
    with pytest.raises(ValueError, match="unknown field"):
        load_panel(["SPY"], field="price", store=store)
