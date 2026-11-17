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


def test_inverse_vol_trend_gives_the_calmer_symbol_the_larger_slice():
    index = pd.bdate_range("2020-01-01", periods=40, name="date")
    wiggle = np.where(np.arange(40) % 2 == 0, 1.0, -1.0)
    prices = pd.DataFrame(
        {
            "CALM": 100 + np.arange(40) + 0.5 * wiggle,
            "WILD": 100 + np.arange(40) + 2.0 * wiggle,
            "FALLING": 200 - np.arange(40) + 0.5 * wiggle,
        },
        index=index,
    )

    weights = rules.inverse_vol_trend(prices, lookback=20, vol_window=10)
    last = weights.iloc[-1]

    assert last["CALM"] > last["WILD"] > 0
    assert last["FALLING"] == 0.0
    assert last.sum() < 1.0  # the falling symbol's slice is left in cash


def test_inverse_vol_trend_uses_no_data_after_the_decision_date():
    prices = random_prices()
    full = rules.inverse_vol_trend(prices, lookback=60, vol_window=20)

    for cut in (120, 250, 333):
        truncated = rules.inverse_vol_trend(prices.iloc[: cut + 1], lookback=60, vol_window=20)
        pd.testing.assert_series_equal(truncated.iloc[-1], full.loc[prices.index[cut]])


def test_volatility_cap_scales_down_a_volatile_portfolio_and_never_up():
    prices = random_prices(seed=1)  # about 16% annual volatility per symbol
    weights = rules.fixed_mix(prices, {"A": 1.0})

    capped = rules.volatility_cap(weights, prices, target_vol=0.08, window=20)
    loose = rules.volatility_cap(weights, prices, target_vol=5.0, window=20)

    assert (capped["A"].iloc[30:] < 1.0).all()
    assert (capped["A"] > 0).all()
    pd.testing.assert_frame_equal(loose, weights)
    realized = prices["A"].pct_change().rolling(20).std().iloc[-1] * np.sqrt(252)
    assert capped["A"].iloc[-1] == pytest.approx(0.08 / realized)


def test_volatility_cap_uses_no_data_after_the_decision_date():
    prices = random_prices(seed=1)
    weights = rules.equal_weight(prices)
    full = rules.volatility_cap(weights, prices, target_vol=0.05, window=20)

    cut = 250
    truncated = rules.volatility_cap(
        weights.iloc[: cut + 1], prices.iloc[: cut + 1], target_vol=0.05, window=20
    )
    pd.testing.assert_series_equal(truncated.iloc[-1], full.iloc[cut])


def test_turn_of_month_holds_the_last_day_and_first_three_days():
    sessions = pd.bdate_range("2024-01-01", "2024-03-29", name="date")
    prices = pd.DataFrame({"A": 100.0}, index=sessions[sessions <= "2024-02-29"])

    weights = rules.turn_of_month(prices, sessions, symbol="A", days_before=1, days_after=3)
    held_on = weights["A"].shift(1)  # row t is the position held during t+1

    january_end = pd.Timestamp("2024-01-31")
    assert held_on.loc[january_end] == 1.0
    assert held_on.loc["2024-02-01":"2024-02-05"].tolist() == [1.0, 1.0, 1.0]
    assert held_on.loc["2024-02-06"] == 0.0
    assert held_on.loc["2024-01-30"] == 0.0
    # The last price date still gets a row, because the calendar knows the next session.
    assert weights["A"].loc["2024-02-29"] == 1.0


def test_relative_momentum_holds_the_strongest_candidates_with_positive_returns():
    index = pd.bdate_range("2020-01-01", periods=4, name="date")
    prices = pd.DataFrame(
        {"A": [10, 10, 10, 13], "B": [10, 10, 10, 12], "C": [10, 10, 10, 9], "SAFE": [5.0] * 4},
        index=index,
    )

    top_two = rules.relative_momentum(prices, ["A", "B", "C"], lookback=1, holdings=2)
    assert top_two.iloc[-1].to_dict() == {"A": 0.5, "B": 0.5, "C": 0.0, "SAFE": 0.0}

    # Only one candidate is rising: the second slot falls back to SAFE, or to cash.
    prices.loc[index[-1], "B"] = 8
    with_fallback = rules.relative_momentum(prices, ["A", "B", "C"], 1, 2, fallback="SAFE")
    assert with_fallback.iloc[-1].to_dict() == {"A": 0.5, "B": 0.0, "C": 0.0, "SAFE": 0.5}
    in_cash = rules.relative_momentum(prices, ["A", "B", "C"], 1, 2)
    assert in_cash.iloc[-1].sum() == 0.5


def test_relative_momentum_uses_no_data_after_the_decision_date():
    prices = random_prices()
    full = rules.relative_momentum(prices, ["A", "B", "C"], lookback=60, holdings=2, fallback="D")

    for cut in (120, 250, 333):
        truncated = rules.relative_momentum(
            prices.iloc[: cut + 1], ["A", "B", "C"], lookback=60, holdings=2, fallback="D"
        )
        pd.testing.assert_series_equal(truncated.iloc[-1], full.loc[prices.index[cut]])
    assert (full.sum(axis=1) <= 1 + 1e-12).all()
    assert (full["D"][prices["D"].reindex(full.index).isna()] == 0).all()
