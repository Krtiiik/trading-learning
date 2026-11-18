"""H1001's experiment on the synthetic Store: which weights it produces and which it never does."""

import numpy as np
import pandas as pd
import pytest

from trading.experiments import h1001
from trading.research.evaluate import Context
from trading.research.market import ResearchData
from trading.research.split import DEV_END, window

PARAMS = {
    "lookback_days": 20,
    "rebalance": "bar",
    "benchmark": "equal_weight_same_schedule",
    "start": "2019-07-01",
}


@pytest.fixture
def dev(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path)


def context(data: ResearchData) -> Context:
    class Stub:
        id = "H1001"
        direction = "positive"

    return Context(Stub(), "dev", window("dev"), data, PARAMS, seed=1001)  # type: ignore[arg-type]


def test_weights_are_one_row_per_bar_long_or_flat_and_inside_the_universe(dev):
    market = dev.market("1d")

    weights = h1001.panel(dev, PARAMS)

    values = weights.to_numpy()
    assert weights.index.equals(market.index) and list(weights.columns) == list(market.symbols)
    assert np.isfinite(values).all() and values.min() >= 0 and values.max() <= 1
    assert values.sum(axis=1).max() <= 1 + 1e-12
    assert not (values > 0)[~market.member_next].any()


def test_weights_equal_a_plain_loop_over_bars_and_coins(dev):
    market = dev.market("1d")
    expected = np.zeros(market.close.shape)
    for bar in range(len(market.index)):
        eligible = market.member_next[bar] & np.isfinite(market.close[bar])
        for coin in np.flatnonzero(eligible):
            closes = market.close[max(bar - 19, 0) : bar + 1, coin]
            if len(closes) == 20 and np.isfinite(closes).all() and closes[-1] > closes.mean():
                expected[bar, coin] = 1 / eligible.sum()

    weights = h1001.panel(dev, PARAMS).to_numpy()

    assert np.allclose(weights, expected)
    # The filter is on for some member-days and off for others, so both branches were compared.
    assert 0.2 < (expected > 0).sum() / market.member_next.sum() < 0.8


def test_a_coin_is_flat_until_it_has_a_close_on_every_bar_of_the_lookback(dev):
    market = dev.market("1d")
    # LATE's first bar is 2024-06-10 and it is a member from August: 52 closes when it joins.
    joins, full = pd.Timestamp("2024-07-31"), pd.Timestamp("2024-08-08")

    weights = h1001.panel(dev, PARAMS | {"lookback_days": 60})["LATEUSDT"]

    assert market.member_next[market.index.get_loc(joins), market.column("LATEUSDT")]
    assert (weights.loc[joins : full - pd.Timedelta(days=1)] == 0).all()
    assert (weights.loc[full:] > 0).any()


def test_a_member_that_stopped_trading_is_flat_and_the_others_share_the_slots(dev):
    # DEAD's last bar is 2023-03-20; it stays a member until April's reconstitution.
    weights = h1001.panel(dev, PARAMS).loc["2023-03-21":"2023-03-30"]

    assert (weights["DEADUSDT"] == 0).all()
    assert set(np.unique(weights.to_numpy())) == {0.0, 1 / 3}


def test_removing_later_bars_leaves_earlier_weights_unchanged(dev):
    cut = pd.Timestamp("2024-03-10")

    again = h1001.panel(dev.truncated(cut), PARAMS)

    pd.testing.assert_frame_equal(again, h1001.panel(dev, PARAMS).loc[:cut])


def test_the_registered_benchmark_is_the_same_slots_without_the_filter(dev):
    market = dev.market("1d")

    filtered = h1001.test(context(dev), h1001.panel(dev, PARAMS))
    unfiltered = h1001.test(context(dev), h1001.slots(market, PARAMS))

    assert unfiltered.estimate == 0 and unfiltered.double_cost_estimate == 0
    assert filtered.n == 731 and np.isfinite(filtered.estimate)
    assert filtered.double_cost_estimate is not None
    assert filtered.metrics["average_weight_invested"] < unfiltered.metrics["average_weight_invested"]
    assert filtered.metrics["benchmark"] == unfiltered.metrics["strategy"]
