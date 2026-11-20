"""The helpers of H2005 to H2008 on synthetic data: what they select and what they detect."""

import numpy as np
import pandas as pd
import pytest

from trading.experiments import h2005, h2006
from trading.experiments.crosssection_tools_b import rank_ic_difference, thirds
from trading.research.market import ResearchData
from trading.research.split import DEV_END


def test_thirds_take_the_lowest_and_highest_third_of_the_usable_assets():
    by = np.array([[5.0, 1.0, 3.0, np.nan, 2.0, 4.0, 6.0], [np.nan, 2.0, 1.0, np.nan, np.nan, 3.0, np.nan]])

    lowest, highest = thirds(by)

    assert lowest.tolist() == [[False, True, False, False, True, False, False], [False, False, True, False, False, False, False]]
    assert highest.tolist() == [[True, False, False, False, False, False, True], [False, False, False, False, False, True, False]]


def test_panels_of_the_daily_experiments_have_a_value_per_bar_and_coin(crypto_root, tmp_path):
    data = ResearchData(DEV_END, crypto_root, records=tmp_path)
    market = data.market("1d")

    nearness = h2005.panel(data, {"high_days": 7})
    both = h2006.panel(data, {"shock_days": 30})

    assert nearness.shape == market.close.shape and nearness.max().max() <= 1 and nearness.min().min() > 0
    assert both["return"].shape == both["shock"].shape == market.close.shape
    assert np.isfinite(both["return"].to_numpy()).mean() > 0.5
    # The synthetic coins trade a constant quote volume: no spread, so no shock is defined.
    assert both["shock"].isna().all().all()


def test_volume_shock_is_the_log_volume_against_the_previous_days_only():
    days = pd.date_range("2021-01-01", periods=6)
    volume = np.array([1.0, 2.0, 4.0, 8.0, 0.0, 16.0])

    class Daily:
        def frame(self, name):
            return pd.DataFrame({"X": volume if name == "quote_volume" else np.ones(6)}, index=days)

    class Data:
        def market(self, granularity):
            return Daily()

    shock = h2006.panel(Data(), {"shock_days": 3})["shock"]["X"]  # type: ignore[arg-type]

    before = np.array([1.0, 2.0, 4.0])
    expected = (np.log(8.0) - np.log(before.mean())) / np.log(before).std(ddof=1)
    assert shock.iloc[3] == pytest.approx(expected)
    assert shock.iloc[:3].isna().all() and shock.iloc[4:].isna().all()  # a zero-volume day in the window


def simulate(seed: int, effect: float, periods: int = 300, assets: int = 30):
    rng = np.random.default_rng(seed)
    signal = rng.standard_normal((periods, assets))
    first = np.zeros((periods, assets), dtype=bool)
    first[:, : assets // 2] = True
    forward = rng.standard_normal((periods, assets)) + effect * signal * first
    return signal, forward, first, ~first


def test_rank_ic_difference_rejects_a_true_null_about_as_often_as_its_level():
    p_values = np.array([rank_ic_difference(*simulate(seed, 0.0)).p_value for seed in range(300)])

    assert 0.02 <= (p_values < 0.05).mean() <= 0.085


def test_rank_ic_difference_recovers_a_planted_difference_with_its_sign():
    result = rank_ic_difference(*simulate(7, 0.2), alternative="greater")

    assert result.p_value < 0.01 and 0.1 < result.estimate < 0.3
    assert result.detail["ic_first"] > 0.1 and abs(result.detail["ic_second"]) < 0.05
    assert rank_ic_difference(*simulate(7, 0.2), alternative="less").p_value > 0.99
