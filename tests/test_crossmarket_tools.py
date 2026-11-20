"""The cross-market helpers on the synthetic Store: exact lookbacks, the leader signal, no look-ahead."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from trading.experiments import crossmarket_tools as tools
from trading.experiments import h4001, h4002
from trading.research.evaluate import Context
from trading.research.market import FIELDS, PANELS, Market, ResearchData
from trading.research.split import DEV_END, window

HOURLY = {"leader": "BTCUSDT", "lookback_bars": 1, "skip_bars": 0, "horizon_bars": 1, "start": "2019-07-01"}


@pytest.fixture(scope="module")
def dev(crypto_root, tmp_path_factory) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path_factory.mktemp("records"))


def context(data: ResearchData, params: dict) -> Context:
    class Stub:
        id = "H4001"
        direction = "positive"

    return Context(Stub(), "dev", window("dev"), data, params, seed=4001)  # type: ignore[arg-type]


def without_rows(market: Market, rows: slice) -> Market:
    """The market as it looks after an outage: the bars of `rows` exist for no coin."""
    keep = np.ones(len(market.index), dtype=bool)
    keep[rows] = False
    arrays = {name: getattr(market, name)[keep] for name in (*FIELDS, *PANELS)}
    return replace(market, index=market.index[keep], **arrays)


def test_a_lookback_is_a_span_of_time_not_a_number_of_rows(dev):
    market = without_rows(dev.market("1h"), slice(100, 103))
    close = market.frame("close")

    one, day = tools.grid_return(market, 1), tools.grid_return(market, 24)

    plain = close / close.shift(1) - 1
    assert one.index.equals(market.index)
    assert one.iloc[100].isna().all() and plain.iloc[100].notna().any()  # first bar after the outage
    pd.testing.assert_frame_equal(one.drop(one.index[100]), plain.drop(plain.index[100]))
    ends = market.index[130]
    expected = close.loc[ends] / close.loc[ends - pd.Timedelta(hours=24)] - 1
    pd.testing.assert_series_equal(day.loc[ends], expected, check_names=False)
    assert day.iloc[100 + 21 : 100 + 24].isna().all().all()  # windows that start inside the outage


def test_the_leader_signal_is_the_leaders_past_return_for_every_other_coin(dev):
    market = dev.market("1h")
    btc = market.frame("close")["BTCUSDT"].pct_change(fill_method=None)

    now = tools.leader_signal(market, "BTCUSDT", 1)
    skipped = tools.leader_signal(market, "BTCUSDT", 1, skip=1)

    assert now["BTCUSDT"].isna().all()
    has_bar = market.frame("close")["ETHUSDT"].notna()
    pd.testing.assert_series_equal(now["ETHUSDT"][has_bar], btc[has_bar], check_names=False)
    pd.testing.assert_series_equal(skipped["ETHUSDT"].iloc[1:], btc.shift(1).iloc[1:], check_names=False)
    # A coin without a bar has no signal: LATE before its first bar, DEAD after its last.
    assert now["LATEUSDT"].loc[:"2024-06-09"].isna().all() and now["LATEUSDT"].loc["2024-06-11":].notna().all()
    assert now["DEADUSDT"].loc["2023-03-21":].isna().all()


def test_a_bar_without_a_trade_gives_no_signal(dev):
    market = dev.market("1h")
    volume = market.quote_volume.copy()
    volume[500, market.column("SOLUSDT")] = 0.0

    signal = tools.leader_signal(replace(market, quote_volume=volume), "BTCUSDT", 1)

    assert np.isnan(signal["SOLUSDT"].iloc[500]) and np.isfinite(signal["ETHUSDT"].iloc[500])


def test_removing_later_bars_leaves_earlier_signals_unchanged(dev):
    cut = pd.Timestamp("2024-03-10 05:00", tz="UTC")

    again = h4001.panel(dev.truncated(cut), HOURLY)

    pd.testing.assert_frame_equal(again, h4001.panel(dev, HOURLY).loc[:cut])


def test_the_leader_test_reports_the_pooled_slope_and_its_diagnostics(dev):
    daily = HOURLY | {"start": "2023-01-01"}

    result = h4002.test(context(dev, daily), h4002.panel(dev, daily))

    assert np.isfinite(result.estimate) and 0 <= result.p_value <= 1
    assert set(result.metrics["diagnostics"]) == {"one_more_bar_skipped", "tiers_1_and_2", "tier_3"}
    within = result.metrics["diagnostics"]
    assert within["tiers_1_and_2"]["n"] + within["tier_3"]["n"] == result.n


def test_only_tiers_keeps_the_coins_of_those_tiers(dev):
    market = dev.market("1d")
    signal = tools.leader_signal(market, "BTCUSDT", 1)

    liquid = tools.only_tiers(market, signal, (1, 2))

    assert liquid.to_numpy()[market.tier == 3].size > 0
    assert np.isnan(liquid.to_numpy()[market.tier == 3]).all()
    assert np.array_equal(liquid.to_numpy()[market.tier != 3], signal.to_numpy()[market.tier != 3], equal_nan=True)
