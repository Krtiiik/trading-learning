import numpy as np
import pandas as pd
import pytest

from trading.strategies.features import FEATURES, feature_panels, forward_return, stack


def random_ohlc(days: int = 420, seed: int = 0):
    rng = np.random.default_rng(seed)
    index = pd.bdate_range("2020-01-01", periods=days, name="date")
    close = pd.DataFrame(
        100 * np.exp(rng.normal(0.0003, 0.01, size=(days, 3)).cumsum(axis=0)),
        index=index,
        columns=list("ABC"),
    )
    close.iloc[:80, 2] = np.nan  # C lists late
    high = close * (1 + rng.uniform(0, 0.01, size=close.shape))
    low = close * (1 - rng.uniform(0, 0.01, size=close.shape))
    return close * 0.9, high, low, close  # adjusted close is a scaled copy


def test_every_feature_is_known_at_the_close_of_its_date():
    adj, high, low, close = random_ohlc()
    full = feature_panels(adj, high, low, close)

    cut = 350
    part = feature_panels(*(frame.iloc[: cut + 1] for frame in (adj, high, low, close)))

    for name in FEATURES:
        pd.testing.assert_series_equal(part[name].iloc[-1], full[name].iloc[cut], check_names=False)


def test_features_are_missing_until_a_symbol_has_enough_history():
    adj, high, low, close = random_ohlc()
    panels = feature_panels(adj, high, low, close)

    assert panels["mom_252"]["C"].first_valid_index() == adj.index[80 + 252]
    assert np.isnan(panels["ibs"]["C"].iloc[79])
    table = stack(panels)
    assert not table.isna().any().any()
    assert list(table.columns) == list(FEATURES)
    assert table.index.names == ["date", "symbol"]


def test_ibs_is_where_the_close_sits_in_the_days_range():
    index = pd.bdate_range("2020-01-01", periods=3, name="date")
    frame = lambda values: pd.DataFrame({"A": values}, index=index, dtype=float)

    panels = feature_panels(frame([10, 10, 10]), frame([12, 11, 10]), frame([8, 9, 10]), frame([11, 9, 10]))

    assert panels["ibs"]["A"].tolist() == pytest.approx([0.75, 0.0, 0.5])  # flat bar counts as the middle


def test_scaled_momentum_is_the_return_in_units_of_expected_volatility():
    adj, high, low, close = random_ohlc()
    panels = feature_panels(adj, high, low, close)

    date = adj.index[400]
    raw = adj["A"].loc[date] / adj["A"].shift(21).loc[date] - 1
    vol = adj["A"].pct_change().rolling(60).std().loc[date]
    assert panels["mom_21"]["A"].loc[date] == pytest.approx(raw / (vol * np.sqrt(21)))
    assert panels["vol_level"]["A"].loc[date] == pytest.approx(vol * np.sqrt(252))


def test_forward_return_looks_ahead_by_exactly_its_horizon():
    adj, *_ = random_ohlc()
    label = forward_return(adj, 5)

    date = adj.index[300]
    raw = adj["A"].iloc[305] / adj["A"].iloc[300] - 1
    vol = adj["A"].pct_change().rolling(60).std().loc[date]
    assert label["A"].loc[date] == pytest.approx(raw / (vol * np.sqrt(5)))
    assert label["A"].iloc[-5:].isna().all()
