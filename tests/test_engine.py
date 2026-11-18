import time

import numpy as np
import pytest

from trading.backtest import cost_per_side, run_backtest
from trading.backtest.engine import _forward_fill

NAN = float("nan")


def column(*values: float) -> np.ndarray:
    return np.array(values, dtype="float64")[:, None]


def test_single_asset_bought_at_next_open_and_charged_once():
    open_ = column(100, 110, 121)
    close = column(110, 121, 133.1)
    weights = column(1, 1, 1)

    result = run_backtest(weights, open_, close, cost=0.001)

    # Bar 0 is still cash; the buy happens at bar 1's open (110) and pays 10 bps once.
    assert result.returns[0] == 0
    assert result.returns[1] == pytest.approx(1.10 * (1 - 0.001) - 1)
    # The last bar runs from its open to its close, with nothing left to trade.
    assert result.returns[2] == pytest.approx(133.1 / 121 - 1)
    assert list(result.turnover) == pytest.approx([0, 1, 0])


def test_two_assets_drift_then_rebalance_to_target():
    open_ = np.array([[10, 20], [10, 20], [12, 20], [12, 10]], dtype="float64")
    close = open_.copy()
    weights = np.array([[0.5, 0.5], [0.5, 0.5], [0, 0], [0, 0]], dtype="float64")

    result = run_backtest(weights, open_, close, cost=0.001)

    # Bar 1: A rises 20%, B is flat, half the portfolio in each.
    assert result.gross[1] == pytest.approx(0.10)
    # At bar 2's open the weights have drifted to 0.6/1.1 and 0.5/1.1; back to 50/50.
    drift = 0.6 / 1.1 - 0.5
    assert result.turnover[2] == pytest.approx(2 * drift)
    assert result.cost[2] == pytest.approx(2 * drift * 0.001)
    # Bar 2: B halves.
    assert result.gross[2] == pytest.approx(-0.25)
    assert result.returns[2] == pytest.approx(0.75 * (1 - 2 * drift * 0.001) - 1)
    # Bar 3: everything was sold at its open.
    assert result.turnover[3] == pytest.approx(1.0)
    assert result.gross[3] == 0


def test_all_nan_row_holds_and_lets_weights_drift():
    open_ = np.array([[10, 20], [10, 20], [12, 20], [12, 10]], dtype="float64")
    weights = np.array([[0.5, 0.5], [NAN, NAN], [NAN, NAN], [NAN, NAN]])

    result = run_backtest(weights, open_, open_.copy(), cost=0.001)

    assert list(result.turnover) == pytest.approx([0, 1, 0, 0])
    # Bar 2 starts with 0.6 in A and 0.5 in B (of an initial 1); B halves.
    assert result.gross[2] == pytest.approx(0.85 / 1.1 - 1)
    assert result.held[2] == pytest.approx([0.6 / 1.1, 0.5 / 1.1])


def test_cash_earns_nothing_and_partial_weight_scales_the_return():
    open_ = column(100, 100, 120)
    close = column(100, 120, 120)

    result = run_backtest(column(0.25, 0.25, 0.25), open_, close)

    assert result.returns[1] == pytest.approx(0.25 * 0.20)


def test_coin_that_stops_trading_is_sold_at_its_last_close():
    open_ = column(10, 10, NAN, NAN)
    close = column(10, 8, NAN, NAN)

    result = run_backtest(column(1, 1, 1, 1), open_, close, cost=0.002)

    assert result.returns[1] == pytest.approx(0.8 * (1 - 0.002) - 1)
    # The position is closed at bar 2's open at the last close (8) and pays the selling cost.
    assert result.returns[2] == pytest.approx(-0.002)
    assert result.returns[3] == 0
    assert result.dropped_weight == pytest.approx(2.0)


def test_double_cost_doubles_what_is_paid():
    open_ = column(100, 100, 100)
    weights = column(1, 0, 0)

    once = run_backtest(weights, open_, open_.copy(), cost=0.001)
    twice = run_backtest(weights, open_, open_.copy(), cost=0.001, cost_multiplier=2.0)

    assert twice.cost == pytest.approx(2 * once.cost)


def test_cost_panel_charges_each_asset_its_own_tier():
    open_ = np.full((3, 3), 50.0)
    weights = np.array([[0.2, 0.3, 0.5]] * 3)
    cost = cost_per_side(np.array([[1, 2, 3]] * 3))

    result = run_backtest(weights, open_, open_.copy(), cost=cost)

    assert result.cost[1] == pytest.approx(0.2 * 0.0012 + 0.3 * 0.0015 + 0.5 * 0.0025)


@pytest.mark.parametrize(
    "weights",
    [column(1.2, 0, 0), column(-0.1, 0, 0), np.array([[0.6, 0.6]] * 3), np.array([[0.5, NAN]] * 3)],
)
def test_weights_outside_long_or_flat_are_rejected(weights):
    prices = np.full(weights.shape, 10.0)

    with pytest.raises(ValueError):
        run_backtest(weights, prices, prices)


def test_forward_fill_keeps_leading_nans():
    values = np.array([[NAN, 1.0], [2.0, NAN], [NAN, NAN]])

    assert np.array_equal(
        _forward_fill(values), np.array([[NAN, 1.0], [2.0, 1.0], [2.0, 1.0]]), equal_nan=True
    )


def random_market(seed: int, bars: int = 400, assets: int = 7):
    """Prices with late listings, an early delisting and gaps; weights with hold rows."""
    rng = np.random.default_rng(seed)
    close = 50 * np.exp(np.cumsum(rng.normal(0, 0.03, (bars, assets)), axis=0))
    open_ = close * np.exp(rng.normal(0, 0.005, (bars, assets)))
    for asset, listed in enumerate(rng.integers(0, bars // 3, assets)):
        open_[:listed, asset] = close[:listed, asset] = NAN
    open_[bars * 2 // 3 :, 0] = close[bars * 2 // 3 :, 0] = NAN
    gaps = rng.random((bars, assets)) < 0.01
    open_[gaps] = close[gaps] = NAN
    weights = rng.random((bars, assets))
    weights[rng.random((bars, assets)) < 0.5] = 0
    weights = weights / np.maximum(weights.sum(axis=1, keepdims=True), 1.0) * rng.random((bars, 1))
    weights[rng.random(bars) < 0.4] = NAN
    cost = rng.choice([0.0012, 0.0015, 0.0025], (bars, assets))
    return weights, open_, close, cost


def reference_backtest(weights, open_, close, cost):
    """The same accounting as a plain loop over bars, holding units of each asset."""
    bars, assets = weights.shape
    units, cash = np.zeros(assets), 1.0
    last_close = np.full(assets, NAN)
    returns = np.zeros(bars)
    for bar in range(bars):
        price = np.where(np.isfinite(open_[bar]), open_[bar], last_close)
        value = cash + np.nansum(units * price)
        paid = 0.0
        if bar >= 1 and not np.isnan(weights[bar - 1]).all():
            target = np.where(np.isfinite(open_[bar]), weights[bar - 1], 0.0)
            current = np.nan_to_num(units * price) / value
            paid = float(np.sum(np.abs(target - current) * cost[bar]))
            units = np.where(target > 0, target * value / price, 0.0)
            cash = value * (1 - target.sum())
        last_close = np.where(np.isfinite(close[bar]), close[bar], last_close)
        if bar + 1 < bars:
            next_price = np.where(np.isfinite(open_[bar + 1]), open_[bar + 1], last_close)
        else:
            next_price = last_close
        next_value = cash + np.nansum(units * next_price)
        returns[bar] = next_value / value * (1 - paid) - 1
        units, cash = units * (1 - paid), cash * (1 - paid)
    return returns


@pytest.mark.parametrize("seed", range(5))
def test_vectorised_engine_matches_a_loop_over_bars(seed):
    weights, open_, close, cost = random_market(seed)

    result = run_backtest(weights, open_, close, cost)

    assert result.returns == pytest.approx(reference_backtest(weights, open_, close, cost), abs=1e-12)


@pytest.mark.parametrize("cut", [50, 199, 333])
def test_results_up_to_a_bar_ignore_everything_after_it(cut):
    """No look-ahead: the returns of bars before `cut` survive any change to later data."""
    weights, open_, close, cost = random_market(11)
    before = run_backtest(weights, open_, close, cost)

    rng = np.random.default_rng(99)
    altered_open, altered_close, altered_weights = open_.copy(), close.copy(), weights.copy()
    # Bar cut-1 ends at the open of bar cut, so that open and everything before it must stay.
    altered_open[cut + 1 :] = rng.random(open_[cut + 1 :].shape) * 100
    altered_close[cut:] = rng.random(close[cut:].shape) * 100
    altered_weights[cut - 1 :] = 0.0
    altered = run_backtest(altered_weights, altered_open, altered_close, cost)
    removed = run_backtest(weights[: cut + 1], open_[: cut + 1], close[: cut + 1], cost[: cut + 1])

    assert np.array_equal(before.returns[:cut], altered.returns[:cut])
    assert np.array_equal(before.returns[:cut], removed.returns[:cut])
    assert np.array_equal(before.held[:cut], altered.held[:cut])


def test_forty_coins_of_hourly_bars_over_five_years_run_well_under_a_second():
    rng = np.random.default_rng(0)
    bars, assets = 5 * 365 * 24, 40
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, (bars, assets)), axis=0))
    weights = np.full((bars, assets), 1 / assets)
    run_backtest(weights, close, close, 0.002)  # warm-up

    started = time.perf_counter()
    run_backtest(weights, close, close, 0.002)
    elapsed = time.perf_counter() - started

    assert elapsed < 0.5
