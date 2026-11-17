"""Daily backtest loop: target weights decided on day t are traded on day t+1.

Accounting is in shares and cash at raw prices. Dividends are credited as cash on the
ex-date to shares held before that day's trades, so equity is a total return without
relying on adjusted prices. Cash earns no interest. Long-only, no leverage.
"""

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from trading.backtest.costs import rebalance
from trading.backtest.market import Market

Fill = Literal["open", "close"]

_WEIGHT_TOLERANCE = 1e-9


@dataclass(frozen=True)
class BacktestResult:
    """What a backtest produced, one row per market date from the first to the last."""

    equity: pd.Series
    """Account value at each close: cash plus shares at raw close."""
    weights: pd.DataFrame
    """Share of equity held in each symbol at each close."""
    traded: pd.Series
    """Dollars bought plus dollars sold on each date."""
    costs: pd.Series
    """Dollars of trading cost paid on each date."""
    dividends: pd.Series
    """Dollars of dividends received on each date."""
    initial_cash: float

    @property
    def returns(self) -> pd.Series:
        """Daily simple returns of equity; the first day is measured from initial cash."""
        previous = self.equity.shift(1)
        previous.iloc[0] = self.initial_cash
        return self.equity / previous - 1.0


def run_backtest(
    market: Market,
    targets: pd.DataFrame,
    *,
    initial_cash: float = 10_000.0,
    cost_bps: float = 5.0,
    fill: Fill = "open",
    start: str | pd.Timestamp | None = None,
    end: str | pd.Timestamp | None = None,
) -> BacktestResult:
    """Simulate holding `targets` with fractional shares and proportional costs.

    `targets` is indexed by decision date: row t holds the weights chosen with data up
    to the close of t. The engine trades them on the next market date after t, at that
    day's raw open or close (`fill`), so a strategy cannot trade on the bar it used.
    Dates without a row (or with an all-NaN row) trade nothing and positions drift.
    Weights must be non-negative and sum to at most 1; the rest stays in cash.

    The account exists from `start` to `end` (default: the whole market). Rows decided
    before `start` are still honoured if their trade date falls inside the window.
    """
    dates = market.dates
    lo = 0 if start is None else int(dates.searchsorted(pd.Timestamp(start), side="left"))
    hi = len(dates) if end is None else int(dates.searchsorted(pd.Timestamp(end), side="right"))
    if lo >= hi:
        raise ValueError("backtest window contains no market dates")

    unknown = targets.columns.difference(market.close.columns)
    if len(unknown):
        raise ValueError(f"targets name symbols missing from the market: {list(unknown)}")
    if not targets.index.isin(dates).all():
        raise ValueError("every target row must be decided on a market date")

    symbols = market.symbols
    target_rows = targets.reindex(columns=symbols).dropna(how="all").fillna(0.0)
    _check_weights(target_rows)

    # Map each decision date to the following market date: the earliest it may trade.
    trade_position = dates.get_indexer(target_rows.index) + 1
    orders: dict[int, np.ndarray] = {
        int(position): row
        for position, row in zip(trade_position, target_rows.to_numpy(), strict=True)
        if lo <= position < hi
    }

    fill_prices = (market.open if fill == "open" else market.close).to_numpy()
    close = market.close.to_numpy()
    dividends = market.dividends.to_numpy()
    last_close = _last_known(close)

    n_symbols = len(symbols)
    shares = np.zeros(n_symbols)
    cash = float(initial_cash)
    equity = np.empty(hi - lo)
    weights = np.zeros((hi - lo, n_symbols))
    traded = np.zeros(hi - lo)
    costs = np.zeros(hi - lo)
    income = np.zeros(hi - lo)

    for row, day in enumerate(range(lo, hi)):
        paid = float((shares * dividends[day]).sum())
        cash += paid
        income[row] = paid

        target = orders.get(day)
        if target is not None:
            price = fill_prices[day]
            tradable = ~np.isnan(price)
            if (target[~tradable] > 0).any():
                missing = [s for s, ok, w in zip(symbols, tradable, target) if not ok and w > 0]
                raise ValueError(
                    f"target on {dates[day - 1].date()} holds {missing}, "
                    f"which have no bar to trade on {dates[day].date()}"
                )
            if (shares[~tradable] > 0).any():
                raise ValueError(
                    f"cannot rebalance on {dates[day].date()}: a held symbol has no bar"
                )
            safe_price = np.where(tradable, price, 1.0)
            values = shares * safe_price
            new_values, cash, traded[row], costs[row] = rebalance(values, cash, target, cost_bps)
            shares = new_values / safe_price

        values = np.where(shares > 0, shares * last_close[day], 0.0)
        equity[row] = cash + values.sum()
        weights[row] = values / equity[row]

    index = dates[lo:hi]
    return BacktestResult(
        equity=pd.Series(equity, index=index, name="equity"),
        weights=pd.DataFrame(weights, index=index, columns=symbols),
        traded=pd.Series(traded, index=index, name="traded"),
        costs=pd.Series(costs, index=index, name="costs"),
        dividends=pd.Series(income, index=index, name="dividends"),
        initial_cash=float(initial_cash),
    )


def _check_weights(target_rows: pd.DataFrame) -> None:
    values = target_rows.to_numpy()
    if (values < -_WEIGHT_TOLERANCE).any():
        raise ValueError("target weights must be non-negative (long-only)")
    if (values.sum(axis=1) > 1.0 + 1e-6).any():
        raise ValueError("target weights must sum to at most 1 (no leverage)")


def _last_known(prices: np.ndarray) -> np.ndarray:
    """Each price forward-filled down its column; NaN until the first bar."""
    return pd.DataFrame(prices).ffill().to_numpy()
