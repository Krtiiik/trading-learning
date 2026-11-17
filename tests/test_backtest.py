import numpy as np
import pandas as pd
import pytest

from trading.backtest import (
    Market,
    annual_turnover,
    cagr,
    max_drawdown,
    rebalance,
    run_backtest,
    sharpe,
    summarize,
    trade_cost,
)

from conftest import make_bars


def make_market(
    opens: dict[str, list[float]],
    closes: dict[str, list[float]] | None = None,
    dividends: dict[str, list[float]] | None = None,
    start: str = "2024-01-01",
) -> Market:
    """A market from per-symbol price lists; closes default to the opens, dividends to zero."""
    periods = len(next(iter(opens.values())))
    index = pd.bdate_range(start, periods=periods, name="date")
    open_panel = pd.DataFrame(opens, index=index, dtype=float)
    close_panel = pd.DataFrame(closes or opens, index=index, dtype=float)
    dividend_panel = pd.DataFrame(dividends or {}, index=index, dtype=float).reindex(
        columns=open_panel.columns, fill_value=0.0
    )
    return Market(open=open_panel, close=close_panel, dividends=dividend_panel.fillna(0.0))


def weights(market: Market, rows: dict[int, dict[str, float]]) -> pd.DataFrame:
    """Target rows keyed by the position of their decision date in the market."""
    return pd.DataFrame(
        {market.dates[position]: row for position, row in rows.items()}
    ).T.reindex(columns=market.symbols)


# --- cost model -------------------------------------------------------------------------


def test_trade_cost_is_proportional_to_notional_per_side():
    assert trade_cost(10_000.0, 5.0) == pytest.approx(5.0)
    assert trade_cost(10_000.0, 2.0) == pytest.approx(2.0)
    assert trade_cost(0.0, 5.0) == 0.0


def test_trade_cost_rejects_negative_rate():
    with pytest.raises(ValueError, match="non-negative"):
        trade_cost(1_000.0, -1.0)


def test_rebalance_from_cash_pays_cost_out_of_the_purchase():
    values, cash, traded, cost = rebalance(np.zeros(1), 10_000.0, np.array([1.0]), 5.0)

    # Fully invested after costs: equity E' solves E' = 10000 - 0.0005 * E'.
    assert values[0] == pytest.approx(10_000.0 / 1.0005)
    assert cash == pytest.approx(0.0, abs=1e-9)
    assert traded == pytest.approx(values[0])
    assert cost == pytest.approx(10_000.0 - values[0])


def test_rebalance_conserves_equity_minus_cost_and_hits_target_weights():
    positions = np.array([6_000.0, 1_000.0, 0.0])
    target = np.array([0.2, 0.3, 0.4])

    values, cash, traded, cost = rebalance(positions, 3_000.0, target, 5.0)

    post_equity = values.sum() + cash
    assert post_equity == pytest.approx(10_000.0 - cost)
    assert values / post_equity == pytest.approx(target)
    assert cost == pytest.approx(traded * 0.0005)
    assert traded == pytest.approx(np.abs(values - positions).sum())


def test_rebalance_to_current_weights_trades_nothing():
    positions = np.array([2_500.0, 7_500.0])

    values, cash, traded, cost = rebalance(positions, 0.0, np.array([0.25, 0.75]), 5.0)

    assert traded == pytest.approx(0.0, abs=1e-9)
    assert cost == pytest.approx(0.0, abs=1e-12)
    assert values == pytest.approx(positions)


def test_rebalance_without_costs_is_exact():
    values, cash, traded, cost = rebalance(np.array([4_000.0]), 6_000.0, np.array([0.5]), 0.0)

    assert values[0] == pytest.approx(5_000.0)
    assert cash == pytest.approx(5_000.0)
    assert traded == pytest.approx(1_000.0)
    assert cost == 0.0


# --- engine accounting --------------------------------------------------------------------


def test_untouched_account_stays_in_cash():
    market = make_market({"A": [10, 11, 12]})

    result = run_backtest(market, weights(market, {}).reindex(columns=["A"]))

    assert list(result.equity) == [10_000.0, 10_000.0, 10_000.0]
    assert result.traded.sum() == 0.0


def test_signal_on_day_t_trades_at_open_of_day_t_plus_1():
    # Close of day 0 is 10; day 1 opens at 20 and closes at 22.
    market = make_market({"A": [10, 20, 20]}, closes={"A": [10, 22, 22]})

    result = run_backtest(market, weights(market, {0: {"A": 1.0}}), cost_bps=0.0)

    # Nothing is held on day 0, and the overnight jump from 10 to 20 is not captured.
    assert result.equity.iloc[0] == 10_000.0
    assert result.weights.iloc[0, 0] == 0.0
    assert result.equity.iloc[1] == pytest.approx(10_000.0 * 22 / 20)
    assert result.traded.iloc[1] == pytest.approx(10_000.0)


def test_fill_at_close_waits_for_the_close_of_day_t_plus_1():
    market = make_market({"A": [10, 20, 30]}, closes={"A": [10, 22, 33]})

    result = run_backtest(market, weights(market, {0: {"A": 1.0}}), cost_bps=0.0, fill="close")

    assert result.equity.iloc[1] == pytest.approx(10_000.0)  # bought at 22, closed at 22
    assert result.equity.iloc[2] == pytest.approx(10_000.0 * 33 / 22)


def test_target_decided_on_the_last_date_never_trades():
    market = make_market({"A": [10, 10, 10]})

    result = run_backtest(market, weights(market, {2: {"A": 1.0}}))

    assert result.traded.sum() == 0.0
    assert result.equity.iloc[-1] == 10_000.0


def test_buying_pays_the_cost_once_and_selling_pays_it_again():
    market = make_market({"A": [10, 10, 10, 10]})
    targets = weights(market, {0: {"A": 1.0}, 1: {"A": 0.0}})

    result = run_backtest(market, targets, cost_bps=5.0)

    after_buy = 10_000.0 / 1.0005
    assert result.equity.iloc[1] == pytest.approx(after_buy)
    assert result.costs.iloc[1] == pytest.approx(10_000.0 - after_buy)
    assert result.equity.iloc[2] == pytest.approx(after_buy * (1 - 0.0005))
    assert result.weights.iloc[2, 0] == 0.0
    assert result.costs.sum() == pytest.approx(10_000.0 - result.equity.iloc[-1])


def test_days_without_a_target_let_positions_drift_for_free():
    market = make_market({"A": [10, 10, 20, 20], "B": [10, 10, 10, 10]})
    targets = weights(market, {0: {"A": 0.5, "B": 0.5}})

    result = run_backtest(market, targets, cost_bps=0.0)

    assert result.traded.iloc[2:].sum() == 0.0
    assert result.equity.iloc[-1] == pytest.approx(15_000.0)
    assert result.weights.iloc[-1].tolist() == pytest.approx([2 / 3, 1 / 3])


def test_daily_rebalancing_trades_back_to_target_and_charges_for_it():
    market = make_market({"A": [10, 10, 20, 20], "B": [10, 10, 10, 10]})
    targets = weights(market, {day: {"A": 0.5, "B": 0.5} for day in range(3)})

    result = run_backtest(market, targets, cost_bps=0.0)

    # Day 2 opens with A doubled: 10000 + 5000 = 15000, so 2500 of A is sold for B.
    assert result.traded.iloc[2] == pytest.approx(5_000.0)
    assert result.weights.iloc[2].tolist() == pytest.approx([0.5, 0.5])
    assert result.traded.iloc[3] == pytest.approx(0.0, abs=1e-9)


def test_unallocated_weight_stays_in_cash():
    market = make_market({"A": [10, 10, 20]}, closes={"A": [10, 10, 20]})

    result = run_backtest(market, weights(market, {0: {"A": 0.4}}), cost_bps=0.0)

    assert result.equity.iloc[1] == pytest.approx(10_000.0)
    assert result.equity.iloc[2] == pytest.approx(6_000.0 + 8_000.0)


def test_dividend_is_paid_in_cash_to_shares_held_before_the_ex_date():
    market = make_market({"A": [10, 10, 10, 10]}, dividends={"A": [0, 0, 0.5, 0]})
    targets = weights(market, {0: {"A": 1.0}})

    result = run_backtest(market, targets, cost_bps=0.0)

    assert result.dividends.iloc[2] == pytest.approx(1_000 * 0.5)
    assert result.equity.iloc[2] == pytest.approx(10_500.0)


def test_shares_bought_on_the_ex_date_receive_no_dividend():
    market = make_market({"A": [10, 10, 10]}, dividends={"A": [0, 0.5, 0]})
    targets = weights(market, {0: {"A": 1.0}})

    result = run_backtest(market, targets, cost_bps=0.0)

    assert result.dividends.sum() == 0.0
    assert result.equity.iloc[-1] == pytest.approx(10_000.0)


def test_buy_and_hold_matches_the_adjusted_close_total_return():
    # Price falls by the dividend on the ex-date; the adjusted close has no such drop.
    close = [100.0, 102.0, 99.96, 101.0]
    market = make_market({"A": close}, dividends={"A": [0, 0, 2.04, 0]})
    adj_factor_before = 1 - 2.04 / 102.0
    adj_close = [100.0 * adj_factor_before, 102.0 * adj_factor_before, 99.96, 101.0]
    targets = weights(market, {0: {"A": 1.0}})

    result = run_backtest(market, targets, cost_bps=0.0)

    # Bought at the day-1 price of 102; cash dividends are not reinvested, so compare
    # up to the ex-date, where both views hold the same value.
    assert result.equity.iloc[2] / 10_000.0 == pytest.approx(adj_close[2] / adj_close[1])


def test_symbol_listed_later_is_traded_only_once_it_has_bars():
    market = make_market({"A": [10, 10, 10, 10], "B": [np.nan, np.nan, 5, 5]})
    targets = weights(market, {0: {"A": 1.0}, 2: {"A": 0.5, "B": 0.5}})

    result = run_backtest(market, targets, cost_bps=0.0)

    assert result.weights.iloc[1].tolist() == pytest.approx([1.0, 0.0])
    assert result.weights.iloc[3].tolist() == pytest.approx([0.5, 0.5])
    assert not result.equity.isna().any()


def test_target_in_a_symbol_without_a_bar_is_rejected():
    market = make_market({"A": [10, 10, 10], "B": [np.nan, np.nan, 5]})

    with pytest.raises(ValueError, match="no bar to trade"):
        run_backtest(market, weights(market, {0: {"A": 0.5, "B": 0.5}}))


@pytest.mark.parametrize(
    ("row", "message"),
    [({"A": 0.7, "B": 0.4}, "at most 1"), ({"A": -0.1, "B": 0.5}, "non-negative")],
)
def test_leveraged_or_short_targets_are_rejected(row, message):
    market = make_market({"A": [10, 10], "B": [10, 10]})

    with pytest.raises(ValueError, match=message):
        run_backtest(market, weights(market, {0: row}))


def test_target_decided_on_a_non_market_date_is_rejected():
    market = make_market({"A": [10, 10]})
    targets = pd.DataFrame({"A": [1.0]}, index=[pd.Timestamp("2023-12-30")])

    with pytest.raises(ValueError, match="market date"):
        run_backtest(market, targets)


def test_window_starts_the_account_late_but_honours_the_prior_decision():
    market = make_market({"A": [10, 10, 10, 20]})
    targets = weights(market, {0: {"A": 1.0}, 1: {"A": 1.0}})

    result = run_backtest(market, targets, cost_bps=0.0, start=market.dates[2])

    # The row decided on day 1 trades on day 2, the first day of the window.
    assert list(result.equity.index) == list(market.dates[2:])
    assert result.traded.iloc[0] == pytest.approx(10_000.0)
    assert result.equity.iloc[-1] == pytest.approx(20_000.0)


def test_market_from_store_reads_raw_prices_and_dividends(store):
    bars = make_bars("2024-01-01", 4, close=100.0, adj_factor=0.9)
    bars.loc[bars.index[2], "dividends"] = 1.5
    store.write("SPY", "1d", bars)
    store.write("TLT", "1d", make_bars("2024-01-02", 3, close=50.0))

    market = Market.from_store(["spy", "tlt"], store=store)

    assert market.symbols == ["SPY", "TLT"]
    assert market.close["SPY"].tolist() == [100.0, 101.0, 102.0, 103.0]
    assert np.isnan(market.open["TLT"].iloc[0])
    assert market.dividends["SPY"].tolist() == [0.0, 0.0, 1.5, 0.0]
    assert market.dividends["TLT"].iloc[0] == 0.0


def test_market_rejects_misaligned_panels():
    market = make_market({"A": [10, 10]})

    with pytest.raises(ValueError, match="share the close panel"):
        Market(open=market.open.iloc[:1], close=market.close, dividends=market.dividends)


# --- metrics -----------------------------------------------------------------------------


def test_cagr_of_a_doubling_over_two_years():
    index = pd.bdate_range("2020-01-01", periods=504)
    equity = pd.Series(np.linspace(10_000.0, 20_000.0, 504), index=index)

    assert cagr(equity, 10_000.0) == pytest.approx(2**0.5 - 1)


def test_sharpe_annualises_daily_mean_over_deviation():
    returns = pd.Series([0.01, -0.01, 0.02, 0.0])

    expected = returns.mean() / returns.std(ddof=1) * np.sqrt(252)
    assert sharpe(returns) == pytest.approx(expected)
    assert np.isnan(sharpe(pd.Series([0.0, 0.0, 0.0])))


def test_max_drawdown_is_the_deepest_fall_from_a_peak():
    equity = pd.Series([100.0, 120.0, 90.0, 110.0, 80.0, 130.0])

    assert max_drawdown(equity) == pytest.approx(80.0 / 120.0 - 1.0)
    assert max_drawdown(pd.Series([100.0, 110.0])) == 0.0
    # A loss on the very first day counts against the starting cash.
    assert max_drawdown(pd.Series([90.0, 95.0]), initial_cash=100.0) == pytest.approx(-0.10)


def test_turnover_counts_one_side_per_year():
    # 252 flat days; one full switch from A to B sells 10000 and buys 10000.
    market = make_market({"A": [10.0] * 252, "B": [10.0] * 252})
    targets = weights(market, {0: {"A": 1.0}, 100: {"B": 1.0}})

    result = run_backtest(market, targets, cost_bps=0.0)

    # Initial purchase (0.5 one-way) plus the switch (1.0 one-way), over one year.
    assert annual_turnover(result) == pytest.approx(1.5)


def test_summarize_reports_dollars_and_costs():
    market = make_market({"A": [10.0] * 251 + [11.0]})
    targets = weights(market, {0: {"A": 1.0}})

    summary = summarize(run_backtest(market, targets, cost_bps=5.0))

    invested = 10_000.0 / 1.0005
    assert summary["years"] == pytest.approx(1.0)
    assert summary["final_equity"] == pytest.approx(invested * 1.1)
    assert summary["net_pnl"] == pytest.approx(invested * 1.1 - 10_000.0)
    assert summary["pnl_per_year"] == pytest.approx(summary["net_pnl"])
    assert summary["costs"] == pytest.approx(10_000.0 - invested)
    assert summary["max_drawdown"] == pytest.approx(invested / 10_000.0 - 1.0)
