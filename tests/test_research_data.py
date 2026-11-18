"""The split and its seal, the market panels research sees, and the standard evaluations."""

import numpy as np
import pandas as pd
import pytest

from trading.backtest import periods_per_year, sharpe_ratio
from trading.data.manifest import ManifestError
from trading.research import evaluate
from trading.research.evaluate import Context
from trading.research.market import ResearchData, load_market
from trading.research.split import (
    DEV_END,
    TEST_START,
    TRAIN_END,
    SealedError,
    check_end,
    open_seal,
    seal_is_open,
    window,
)

# Split and seal


def test_segments_partition_time_at_the_declared_boundaries():
    days = pd.DatetimeIndex(["2022-12-31", "2023-01-01", "2024-12-31", "2025-01-01"])

    assert window("train").mask(days).tolist() == [True, False, False, False]
    assert window("dev").mask(days).tolist() == [False, True, True, False]
    assert window("test").mask(days).tolist() == [False, False, False, True]


def test_an_hourly_bar_belongs_to_the_day_it_opens_on():
    hours = pd.DatetimeIndex(["2022-12-31 23:00", "2023-01-01 00:00"], tz="UTC")

    assert window("train").mask(hours).tolist() == [True, False]
    assert window("dev").mask(hours).tolist() == [False, True]


def test_loading_test_period_data_fails_while_the_seal_is_closed(crypto_root, tmp_path):
    """The test seal: nothing from 2025 on can be loaded for research until it is opened."""
    with pytest.raises(SealedError, match="sealed"):
        load_market("1d", TEST_START, crypto_root, records=tmp_path)
    with pytest.raises(SealedError):
        load_market("1h", pd.Timestamp("2026-06-30"), crypto_root, records=tmp_path)
    with pytest.raises(SealedError):
        ResearchData(pd.Timestamp("2200-01-01"), crypto_root, records=tmp_path)
    with pytest.raises(SealedError):
        check_end(None, tmp_path)

    last_allowed = load_market("1d", DEV_END, crypto_root, records=tmp_path)

    assert last_allowed.index[-1] == pd.Timestamp("2024-12-31")


def test_opening_the_seal_is_recorded_and_happens_once(crypto_root, tmp_path):
    record = open_seal(["H0001", "H0002"], "abc123", tmp_path)

    assert seal_is_open(tmp_path)
    assert record["finalists"] == ["H0001", "H0002"] and record["commit"] == "abc123"
    assert load_market("1d", TEST_START, crypto_root, records=tmp_path).index[-1] == TEST_START
    with pytest.raises(SealedError, match="already opened"):
        open_seal(["H0003"], "def456", tmp_path)


@pytest.mark.parametrize("finalists", [[], ["H1", "H2", "H3", "H4", "H5", "H6"], ["H1", "H1"]])
def test_the_seal_opens_only_for_one_to_five_distinct_finalists(tmp_path, finalists):
    with pytest.raises(SealedError):
        open_seal(finalists, "abc123", tmp_path)
    assert not seal_is_open(tmp_path)


# Market panels


@pytest.fixture
def train(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(TRAIN_END, crypto_root, records=tmp_path)


@pytest.fixture
def dev(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path)


def test_market_ends_with_the_segment_and_holds_nothing_later(train):
    daily, hourly = train.market("1d"), train.market("1h")

    assert daily.index[-1] == pd.Timestamp("2022-12-31")
    assert hourly.index[-1] == pd.Timestamp("2022-12-31 23:00", tz="UTC")
    assert daily.close.shape == (122, len(daily.symbols))


def test_market_has_no_column_for_a_coin_that_only_becomes_a_member_later(train, dev):
    # ADA joins in April 2023 and LATE in August 2024: their columns alone would leak that.
    assert train.market("1d").symbols == ("BTCUSDT", "DEADUSDT", "ETHUSDT", "SOLUSDT")
    assert dev.market("1d").symbols == ("ADAUSDT", "BTCUSDT", "DEADUSDT", "ETHUSDT", "LATEUSDT", "SOLUSDT")


def test_membership_and_cost_follow_the_point_in_time_universe(dev):
    market = dev.market("1d")
    row = market.index.get_loc(pd.Timestamp("2023-03-31"))
    ada, dead, btc = market.column("ADAUSDT"), market.column("DEADUSDT"), market.column("BTCUSDT")

    # DEAD stopped trading on 20 March; April's reconstitution replaces it with ADA.
    assert market.member[row, dead] and not market.member[row, ada]
    assert market.member[row + 1, ada] and not market.member[row + 1, dead]
    # A decision at the close of 31 March already knows April's membership.
    assert market.member_next[row, ada] and not market.member_next[row, dead]
    assert market.member_next[row - 1, dead]
    assert market.cost[row, btc] == pytest.approx(0.0012)
    assert market.cost[row + 1, ada] == pytest.approx(0.0025)
    assert np.isnan(market.close[row, dead])


def test_truncating_removes_later_bars_only(dev):
    market = dev.market("1h")

    cut = market.truncate(pd.Timestamp("2023-06-30 12:00"))

    assert cut.index[-1] == pd.Timestamp("2023-06-30 12:00", tz="UTC")
    assert cut.symbols == market.symbols
    assert np.array_equal(cut.close, market.close[: len(cut.index)], equal_nan=True)
    assert dev.truncated(pd.Timestamp("2023-06-30")).market("1d").index[-1] == pd.Timestamp("2023-06-30")


def test_funding_is_summed_into_the_bar_in_which_it_was_paid(dev):
    daily = dev.series("funding", "1d")
    hourly = dev.series("funding", "1h")
    market_d, market_h = dev.market("1d"), dev.market("1h")
    btc = market_d.column("BTCUSDT")

    # Events at 08:00, 16:00 and 24:00 fall inside a daily bar; the one at 00:00 closes the day before.
    assert daily[5, btc] == pytest.approx(0.0003)
    assert daily[0, btc] == pytest.approx(0.0003)
    day = market_h.index.get_loc(pd.Timestamp("2023-05-05 00:00", tz="UTC"))
    paid = np.flatnonzero(np.isfinite(hourly[day : day + 24, btc]))
    assert paid.tolist() == [7, 15, 23]  # the bars that close at 08:00, 16:00 and 24:00
    assert np.isnan(daily[:, market_d.column("SOLUSDT")]).all()  # no contract
    assert np.isfinite(daily[:, market_d.column("ADAUSDT")]).any()  # via 1000ADAUSDT


def test_the_basis_of_a_bar_is_its_last_hourly_value(dev):
    daily = dev.series("premium", "1d")
    hourly = dev.series("premium", "1h")
    btc = dev.market("1d").column("BTCUSDT")

    assert hourly[100, btc] == pytest.approx(100e-8)
    assert daily[0, btc] == pytest.approx(23e-8) and daily[1, btc] == pytest.approx(47e-8)


def test_research_data_notes_every_dataset_it_touched(dev):
    dev.market("1d")
    dev.series("funding", "1d")

    assert sorted(dev.used) == ["binance/funding", "binance/spot/1d", "binance/universe"]
    assert all(len(identity) == 64 for identity in dev.used.values())


def test_a_store_that_no_longer_matches_its_manifest_is_refused(crypto_root, tmp_path):
    import shutil

    copy = tmp_path / "store"
    shutil.copytree(crypto_root / "binance", copy / "binance", ignore=shutil.ignore_patterns("raw"))
    victim = copy / "binance" / "spot" / "1d" / "BTCUSDT.parquet"
    pd.read_parquet(victim).iloc[:-1].to_parquet(victim)

    with pytest.raises(ManifestError, match="does not match its manifest"):
        load_market("1d", TRAIN_END, copy, records=tmp_path)


# Building blocks for experiments


def context(data: ResearchData, segment: str = "dev", direction: str = "positive") -> Context:
    class Stub:
        id = "H9999"

    Stub.direction = direction
    return Context(Stub(), segment, window(segment), data, {}, seed=1)  # type: ignore[arg-type]


def test_weights_frame_lists_only_rebalance_rows_and_held_coins(dev):
    market = dev.market("1d")
    frame = pd.DataFrame({"BTCUSDT": [0.5, 1.0]}, index=market.index[[3, 10]])

    weights = evaluate.to_weights(market, frame)

    assert np.isnan(weights[0]).all() and np.isnan(weights[4]).all()
    assert weights[3, market.column("BTCUSDT")] == 0.5 and weights[3].sum() == 0.5
    with pytest.raises(ValueError, match="does not have"):
        evaluate.to_weights(market, pd.DataFrame({"NOPEUSDT": [1.0]}, index=market.index[:1]))
    with pytest.raises(ValueError, match="not bar labels"):
        evaluate.to_weights(market, pd.DataFrame({"BTCUSDT": [1.0]}, index=[pd.Timestamp("1999-01-01")]))


def test_rebalance_labels_are_the_last_bars_of_weeks_and_months(dev):
    market = dev.market("1d")

    weekly = evaluate.rebalance_labels(market, "week")
    monthly = evaluate.rebalance_labels(market, "month")

    assert (weekly.day_of_week == 6).all()  # Sunday's close, traded at Monday's open
    assert monthly[0] == pd.Timestamp("2022-09-30") and (monthly + pd.Timedelta(days=1)).day.max() == 1
    # The calendar, not later data, says a bar ends its month: true for the data's last bar too.
    assert monthly[-1] == pd.Timestamp("2024-12-31")
    cut = dev.truncated(pd.Timestamp("2023-06-25")).market("1d")
    assert evaluate.rebalance_labels(cut, "week")[-1] == pd.Timestamp("2023-06-25")


def test_equal_weight_spreads_over_the_members_in_force_at_the_trade(dev):
    market = dev.market("1d")

    weights = evaluate.equal_weight(market)

    march = weights.loc[pd.Timestamp("2023-03-31")]
    assert march["ADAUSDT"] == 0.25 and march["DEADUSDT"] == 0 and march.sum() == 1
    assert weights.loc[pd.Timestamp("2022-09-30")].sum() == pytest.approx(1.0)


def test_buy_and_hold_through_the_engine_is_the_price_ratio_less_one_fee(dev):
    market = dev.market("1d")
    btc = market.column("BTCUSDT")

    result = evaluate.backtest(market, evaluate.buy_and_hold(market))

    grown = np.prod(1 + result.returns)
    # Bought on the second bar, before the first reconstitution: every coin is still tier 3.
    assert grown == pytest.approx(market.close[-1, btc] / market.open[1, btc] * (1 - 0.0025))
    assert result.turnover.sum() == pytest.approx(1.0)


def test_forward_returns_start_at_the_next_open_and_stop_before_the_data_ends(dev):
    market = dev.market("1d")
    btc = market.column("BTCUSDT")

    forward = evaluate.forward_returns(market, 3)

    assert forward[10, btc] == pytest.approx(market.open[14, btc] / market.open[11, btc] - 1)
    assert np.isfinite(forward[-5, btc]) and np.isnan(forward[-4:, btc]).all()


def test_a_strategy_equal_to_its_benchmark_shows_no_difference(dev):
    market = dev.market("1d")

    result = evaluate.evaluate_strategy(context(dev), evaluate.equal_weight(market), "1d", draws=200)

    assert result.estimate == 0 and result.double_cost_estimate == 0
    assert result.p_value > 0.5
    assert result.n == 731  # the dev window only: 2023 and 2024
    assert result.metrics["window"]["first"].startswith("2023-01-01")


def test_a_strategy_may_not_buy_a_coin_outside_the_point_in_time_universe(dev):
    market = dev.market("1d")
    early = pd.DataFrame({"LATEUSDT": [1.0]}, index=[pd.Timestamp("2024-07-10")])  # a member from August
    allowed = pd.DataFrame({"LATEUSDT": [1.0]}, index=[pd.Timestamp("2024-07-31")])  # decided at July's last close

    with pytest.raises(ValueError, match="outside the point-in-time universe, first LATEUSDT"):
        evaluate.evaluate_strategy(context(dev), early, "1d", draws=50)

    assert evaluate.evaluate_strategy(context(dev), allowed, "1d", draws=50).n == 731


def test_a_declared_start_narrows_the_evaluation_window_and_never_widens_it(dev):
    market = dev.market("1d")
    weights = evaluate.equal_weight(market)

    late = evaluate.evaluate_strategy(context(dev), weights, "1d", draws=50, start="2024-01-01")
    early = evaluate.evaluate_strategy(context(dev), weights, "1d", draws=50, start="2020-01-01")

    assert late.n == 366 and late.metrics["window"]["first"].startswith("2024-01-01")
    assert early.n == 731  # a start before the segment changes nothing
    with pytest.raises(ValueError, match="no bars to evaluate"):
        evaluate.evaluate_strategy(context(dev), weights, "1d", draws=50, start="2030-01-01")


def test_etf_bars_reach_research_only_up_to_the_segment_end(crypto_root, tmp_path):
    import shutil

    from trading.data.manifest import build_manifest
    from trading.data.storage import BarStore

    from conftest import make_bars

    root = tmp_path / "store"
    shutil.copytree(crypto_root / "binance", root / "binance", ignore=shutil.ignore_patterns("raw"))
    BarStore(root).write("SPY", "1d", make_bars("2022-11-01", 700))
    build_manifest(root, "1d", "fake")
    data = ResearchData(TRAIN_END, root, records=tmp_path)

    panel = data.etf("close")

    assert list(panel.columns) == ["SPY"] and panel.index[-1] == pd.Timestamp("2022-12-30")
    assert data.truncated(pd.Timestamp("2022-12-01")).etf("close").index[-1] == pd.Timestamp("2022-12-01")
    assert "1d" in data.used


def test_a_strategy_that_peeks_beats_the_benchmark_and_costs_show_up(dev):
    market = dev.market("1d")
    tomorrow = np.roll(market.open, -2, axis=0) / np.roll(market.open, -1, axis=0) - 1
    best = np.nanargmax(np.where(market.member_next, tomorrow, -np.inf)[:-2], axis=1)
    weights = np.zeros((len(best), len(market.symbols)))
    weights[np.arange(len(best)), best] = market.member_next[:-2].any(axis=1)  # cash while no members
    peeking = pd.DataFrame(weights, index=market.index[:-2], columns=list(market.symbols))

    result = evaluate.evaluate_strategy(context(dev), peeking, "1d", benchmark="btc", draws=200)

    assert result.estimate > 3 and result.p_value < 0.01
    assert result.double_cost_estimate < result.estimate  # it trades every day; the benchmark never
    strategy = result.metrics["strategy"]
    assert strategy["sharpe"] == pytest.approx(result.estimate + result.metrics["benchmark"]["sharpe"])
    assert strategy["turnover_per_year"] > 100
    assert set(result.metrics) >= {"reference_btc", "reference_equal_weight", "reference_cash"}
    assert result.metrics["reference_cash"]["sharpe"] == 0


def test_annualisation_uses_365_days_for_a_market_that_never_closes():
    assert periods_per_year("1d") == 365
    assert periods_per_year("1h") == 365 * 24
    assert periods_per_year("1d", "NYSE") == pytest.approx(251.6, abs=0.5)
    assert sharpe_ratio(np.array([0.01, -0.01, 0.02, 0.0]), 365) == pytest.approx(
        0.005 / np.std([0.01, -0.01, 0.02, 0.0], ddof=1) * np.sqrt(365)
    )


def test_a_predictor_that_is_the_future_return_has_a_rank_ic_of_one(dev):
    market = dev.market("1d")
    signal = pd.DataFrame(evaluate.forward_returns(market, 1), index=market.index, columns=list(market.symbols))

    result = evaluate.evaluate_predictor(context(dev), signal, "1d", horizon=1, min_assets=3)
    opposite = evaluate.evaluate_predictor(
        context(dev, direction="negative"), signal, "1d", horizon=1, min_assets=3
    )

    assert result.estimate == pytest.approx(1.0) and result.p_value < 1e-6
    assert opposite.p_value > 0.99
    assert result.n == 729  # dev days whose entry and exit opens both lie inside the data


def test_a_predictor_is_scored_on_universe_members_only(dev):
    market = dev.market("1d")
    signal = pd.DataFrame(1.0, index=market.index, columns=list(market.symbols))
    non_members_only = signal.where(~market.member)

    with pytest.raises(ValueError, match="too few observations"):
        # No member has a signal, so there is nothing to test.
        evaluate.evaluate_predictor(context(dev), non_members_only, "1d", horizon=1, min_assets=3)
