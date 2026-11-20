"""The time-series family's signals on the synthetic Store: what each marks and what it never uses."""

import numpy as np
import pandas as pd
import pytest

from trading.experiments import h1005
from trading.experiments.timeseries_tools import (
    bar_return_zscore,
    calendar_dummy,
    universe_return,
    volatility_scale,
)
from trading.research.market import ResearchData
from trading.research.split import DEV_END


@pytest.fixture
def dev(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path)


def test_an_hour_dummy_marks_the_bars_opening_at_those_utc_hours_for_every_coin(dev):
    market = dev.market("1h")

    dummy = calendar_dummy(market, hours=[20, 21])

    assert dummy.shape == market.close.shape
    assert dummy.loc["2023-05-04 20:00+00:00"].eq(1).all() and dummy.loc["2023-05-04 21:00+00:00"].eq(1).all()
    assert dummy.loc["2023-05-04 22:00+00:00"].eq(0).all() and dummy.loc["2023-05-04 19:00+00:00"].eq(0).all()
    assert dummy.iloc[:, 0].mean() == pytest.approx(2 / 24, abs=1e-3)


def test_a_weekday_dummy_marks_the_daily_bars_labelled_that_day(dev):
    dummy = calendar_dummy(dev.market("1d"), weekdays=[3])["BTCUSDT"]

    assert dummy.loc["2023-05-04"] == 1  # a Thursday
    assert dummy.loc["2023-05-05"] == 0 and dummy.loc["2023-05-03"] == 0
    assert set(dummy.index[dummy == 1].dayofweek) == {3}


def test_the_zscore_is_the_bar_return_over_the_deviation_of_the_bars_before_it(dev):
    market = dev.market("1h")
    coin, bar = market.column("ETHUSDT"), 5000
    change = market.close[:, coin] / market.open[:, coin] - 1

    score = bar_return_zscore(market, window=168, min_periods=120)

    assert score.iloc[bar, coin] == pytest.approx(change[bar] / change[bar - 168 : bar].std(ddof=1))
    assert score.iloc[:120, coin].isna().all() and np.isfinite(score.iloc[120, coin])


def test_the_zscore_does_not_change_when_later_bars_are_removed(dev):
    cut = pd.Timestamp("2023-03-10 07:00", tz="UTC")

    again = bar_return_zscore(dev.truncated(cut).market("1h"), 168, 120)

    pd.testing.assert_frame_equal(again, bar_return_zscore(dev.market("1h"), 168, 120).loc[:cut])


def test_the_universe_return_is_the_members_average_close_to_close_return(dev):
    market = dev.market("1d")
    bar = market.index.get_loc(pd.Timestamp("2023-05-04"))
    members = np.flatnonzero(market.member[bar])

    expected = np.mean(market.close[bar, members] / market.close[bar - 1, members] - 1)

    assert len(members) == 4
    assert universe_return(market).iloc[bar] == pytest.approx(expected)


def test_the_volatility_scale_is_one_until_both_windows_are_full_and_falls_when_volatility_rises():
    rng = np.random.default_rng(7)
    returns = pd.Series(np.concatenate([rng.normal(0, 0.01, 400), rng.normal(0, 0.05, 30)]))

    scale = volatility_scale(returns, short=30, long=365)

    assert (scale.iloc[:364] == 1).all()
    assert scale.between(0, 1).all()
    assert scale.iloc[-1] < 0.5 < scale.iloc[399]


def test_h1005_scales_every_slot_alike_and_never_above_the_benchmark(dev):
    params = {"rebalance": "week", "recent_days": 30, "usual_days": 365, "start": "2019-07-01"}
    market = dev.market("1d")

    weights, benchmark = h1005.panel(dev, params), h1005.slots(market, params)

    ratio = (weights.sum(axis=1) / benchmark.sum(axis=1)).dropna()
    assert weights.index.equals(benchmark.index) and (weights <= benchmark + 1e-12).all().all()
    assert ratio.between(0, 1).all() and (ratio < 1).any() and (ratio == 1).any()
    assert not (weights.to_numpy() > 0)[~market.member_next[market.index.get_indexer(weights.index)]].any()
