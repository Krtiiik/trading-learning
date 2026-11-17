import pandas as pd
import pytest

from trading.data.providers import ProviderError
from trading.data.update import update_symbol

from conftest import FakeProvider, make_bars


def test_first_update_downloads_full_history(store):
    provider = FakeProvider({"SPY": make_bars("2024-01-01", 10)})

    result = update_symbol(provider, store, "spy")

    assert (result.mode, result.new_bars, result.total_bars) == ("full", 10, 10)
    assert result.reason == "nothing stored yet"
    assert provider.requests == [("SPY", None, None)]
    assert len(store.read("SPY", "1d")) == 10


def test_incremental_update_fetches_from_last_stored_bar(store):
    history = make_bars("2024-01-01", 10)
    store.write("SPY", "1d", history.iloc[:6])
    provider = FakeProvider({"SPY": history})

    result = update_symbol(provider, store, "SPY")

    last_stored = history.index[5].date()
    assert provider.requests == [("SPY", last_stored, None)]
    assert (result.mode, result.new_bars, result.total_bars) == ("incremental", 4, 10)
    pd.testing.assert_frame_equal(store.read("SPY", "1d"), history, check_freq=False)


def test_incremental_update_replaces_last_bar_with_final_values(store):
    history = make_bars("2024-01-01", 5)
    in_progress = history.iloc[:3].copy()
    in_progress.loc[in_progress.index[-1], ["close", "adj_close"]] = 90.0
    store.write("SPY", "1d", in_progress)

    update_symbol(FakeProvider({"SPY": history}), store, "SPY")

    assert store.read("SPY", "1d").iloc[2]["close"] == history.iloc[2]["close"]


def test_changed_adjustment_factor_triggers_full_download(store):
    store.write("SPY", "1d", make_bars("2024-01-01", 6, adj_factor=1.0))
    readjusted = make_bars("2024-01-01", 10, adj_factor=0.98)
    provider = FakeProvider({"SPY": readjusted})

    result = update_symbol(provider, store, "SPY")

    assert (result.mode, result.reason) == ("full", "adjustments changed")
    assert provider.requests[-1] == ("SPY", None, None)
    pd.testing.assert_frame_equal(store.read("SPY", "1d"), readjusted, check_freq=False)


def test_full_flag_downloads_everything_again(store):
    history = make_bars("2024-01-01", 10)
    store.write("SPY", "1d", history)
    provider = FakeProvider({"SPY": history})

    result = update_symbol(provider, store, "SPY", full=True)

    assert (result.mode, result.new_bars, result.reason) == ("full", 0, "")
    assert provider.requests == [("SPY", None, None)]


def test_up_to_date_symbol_gains_no_bars(store):
    history = make_bars("2024-01-01", 5)
    store.write("SPY", "1d", history)

    result = update_symbol(FakeProvider({"SPY": history}), store, "SPY")

    assert (result.mode, result.new_bars, result.total_bars) == ("incremental", 0, 5)


def test_symbol_without_any_bars_is_an_error(store):
    with pytest.raises(ProviderError, match="no bars for NOPE"):
        update_symbol(FakeProvider(), store, "NOPE")
