import numpy as np
import pandas as pd
import pytest

from trading.strategies import rules


def random_prices(days: int = 400, seed: int = 0) -> pd.DataFrame:
    """A random-walk panel in which C lists 50 days late and D 300 days late."""
    rng = np.random.default_rng(seed)
    index = pd.bdate_range("2020-01-01", periods=days, name="date")
    steps = rng.normal(0.0003, 0.01, size=(days, 4))
    prices = pd.DataFrame(100 * np.exp(steps.cumsum(axis=0)), index=index, columns=list("ABCD"))
    prices.iloc[:50, 2] = np.nan
    prices.iloc[:300, 3] = np.nan
    return prices


STRATEGIES = {
    "fixed_mix": lambda p: rules.fixed_mix(p, {"A": 0.6, "C": 0.4}),
    "equal_weight": rules.equal_weight,
    "time_series_momentum": lambda p: rules.time_series_momentum(p, lookback=60),
    "trend_filter": lambda p: rules.trend_filter(p, risky="A", safe="B", window=50),
    "trend_filter_cash": lambda p: rules.trend_filter(p, risky="A", safe=None, window=50),
    "rsi_pullback": lambda p: rules.rsi_pullback(p, symbol="A", trend_window=50),
    "cross_sectional_reversal": lambda p: rules.cross_sectional_reversal(p, holdings=1),
}


@pytest.mark.parametrize("name", STRATEGIES)
def test_weights_use_no_data_after_the_decision_date(name):
    prices = random_prices()
    strategy = STRATEGIES[name]
    full = strategy(prices)

    for cut in (120, 250, 333):
        truncated = strategy(prices.iloc[: cut + 1])
        date = prices.index[cut]
        pd.testing.assert_series_equal(truncated.loc[date], full.loc[date])


@pytest.mark.parametrize("name", STRATEGIES)
def test_weights_are_long_only_unlevered_and_only_in_listed_symbols(name):
    prices = random_prices()
    weights = STRATEGIES[name](prices)

    assert (weights >= 0).all().all()
    assert (weights.sum(axis=1) <= 1 + 1e-12).all()
    assert (weights[prices.reindex(weights.index).isna()].fillna(0.0) == 0).all().all()


def test_equal_weight_spreads_over_listed_symbols_only():
    weights = rules.equal_weight(random_prices())

    assert weights.iloc[0].tolist() == pytest.approx([0.5, 0.5, 0.0, 0.0])
    assert weights.iloc[100].tolist() == pytest.approx([1 / 3, 1 / 3, 1 / 3, 0.0])
    assert weights.iloc[-1].tolist() == pytest.approx([0.25] * 4)


def test_fixed_mix_starts_when_every_member_is_listed():
    prices = random_prices()

    weights = rules.fixed_mix(prices, {"A": 0.6, "C": 0.4})

    assert weights.index[0] == prices.index[50]
    assert weights.iloc[0].tolist() == pytest.approx([0.6, 0.0, 0.4, 0.0])


def test_time_series_momentum_leaves_downtrending_slices_in_cash():
    index = pd.bdate_range("2020-01-01", periods=5, name="date")
    prices = pd.DataFrame({"UP": [1, 2, 3, 4, 5], "DOWN": [5, 4, 3, 2, 1]}, index=index, dtype=float)

    weights = rules.time_series_momentum(prices, lookback=2)

    assert weights.index[0] == index[2]
    assert weights.iloc[-1].tolist() == [0.5, 0.0]


def test_trend_filter_switches_to_safe_asset_below_the_average():
    index = pd.bdate_range("2020-01-01", periods=6, name="date")
    prices = pd.DataFrame(
        {"RISKY": [10, 11, 12, 13, 9, 8], "SAFE": [1.0] * 6}, index=index, dtype=float
    )

    weights = rules.trend_filter(prices, risky="RISKY", safe="SAFE", window=3)

    assert weights["RISKY"].tolist() == [1.0, 1.0, 0.0, 0.0]
    assert weights["SAFE"].tolist() == [0.0, 0.0, 1.0, 1.0]


def test_rsi_is_100_after_only_gains_and_0_after_only_losses():
    rising = pd.Series([1.0, 2.0, 3.0, 4.0])
    falling = pd.Series([4.0, 3.0, 2.0, 1.0])

    assert rules.rsi(rising, 2).iloc[-1] == pytest.approx(100.0)
    assert rules.rsi(falling, 2).iloc[-1] == pytest.approx(0.0)


def test_rsi_pullback_buys_the_dip_and_sells_the_bounce():
    index = pd.bdate_range("2020-01-01", periods=16, name="date")
    close = [*range(100, 126, 2), 118, 119, 123]  # steady rise, a 6-point dip, a bounce
    prices = pd.DataFrame({"A": close}, index=index, dtype=float)

    weights = rules.rsi_pullback(
        prices, symbol="A", entry_below=30.0, trend_window=10, exit_window=3
    )

    # The dip to 118 takes RSI(2) to 25 while price is still above its 10-day average
    # (116.2), so the position opens; 119 is below its 3-day average, so it is kept;
    # 123 is above it, so it closes.
    held = weights["A"]
    assert held.loc[index[12]] == 0.0
    assert held.loc[index[13]] == 1.0
    assert held.loc[index[14]] == 1.0
    assert held.loc[index[15]] == 0.0


def test_cross_sectional_reversal_holds_the_worst_recent_performers():
    index = pd.bdate_range("2020-01-01", periods=3, name="date")
    prices = pd.DataFrame(
        {"A": [10, 10, 12], "B": [10, 10, 9], "C": [10, 10, 10], "D": [10, 10, 8]},
        index=index,
        dtype=float,
    )

    weights = rules.cross_sectional_reversal(prices, lookback=1, holdings=2)

    assert weights.iloc[-1].to_dict() == {"A": 0.0, "B": 0.5, "C": 0.0, "D": 0.5}
