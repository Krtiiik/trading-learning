"""The backtest engine: a panel of target weights against a panel of prices, as array operations.

Timing: row `t` of the weights is decided at the close of bar `t` and traded at the open of
bar `t + 1`. A row of all-NaN means "do not trade at the next open": the holdings drift.
Long or flat only: weights lie in [0, 1], a row sums to at most 1, and the rest is cash at 0%.
"""

from dataclasses import dataclass

import numpy as np

_TOLERANCE = 1e-9


@dataclass(frozen=True)
class BacktestResult:
    returns: np.ndarray
    """Net return of each bar, from its open to the next bar's open, after trading costs."""
    gross: np.ndarray
    """The same before costs."""
    cost: np.ndarray
    """Cost paid at each bar's open, as a fraction of the portfolio."""
    turnover: np.ndarray
    """Sum of absolute weight changes traded at each bar's open (buys plus sells)."""
    held: np.ndarray
    """Weights held at each bar's open, after any trade there."""
    dropped: np.ndarray
    """Target weight at each bar's open that could not be bought: the asset had no bar there."""

    @property
    def dropped_weight(self) -> float:
        """Total dropped weight over all bars."""
        return float(self.dropped.sum())


def run_backtest(
    weights: np.ndarray,
    open_: np.ndarray,
    close: np.ndarray,
    cost: np.ndarray | float = 0.0,
    cost_multiplier: float = 1.0,
) -> BacktestResult:
    """Run target `weights` (bars x assets) against `open_` and `close` prices of the same shape.

    `cost` is the per-side cost as a fraction of traded value, per bar and asset or one number.
    An asset without a bar is priced at its last close, so a coin that stops trading is sold
    at its final close. The last bar's return runs from its open to its close.
    """
    weights = np.asarray(weights, dtype="float64")
    open_ = np.asarray(open_, dtype="float64")
    close = np.asarray(close, dtype="float64")
    if not (weights.shape == open_.shape == close.shape) or weights.ndim != 2:
        raise ValueError("weights, open_ and close must be 2-D arrays of the same shape")
    bars, assets = weights.shape

    hold = np.isnan(weights).all(axis=1)
    if np.isnan(weights[~hold]).any():
        raise ValueError("a weights row must be fully specified or all-NaN (hold)")
    decided = np.where(hold[:, None], 0.0, weights)
    if (decided < -_TOLERANCE).any() or (decided.sum(axis=1) > 1 + _TOLERANCE).any():
        raise ValueError("weights must lie in [0, 1] and each row must sum to at most 1")

    # price[t] values a holding at the open of bar t; price[bars] at the close of the last bar.
    last_close = _forward_fill(close)
    price = np.empty((bars + 1, assets))
    price[0] = open_[0]
    price[1:bars] = np.where(np.isfinite(open_[1:]), open_[1:], last_close[:-1])
    price[bars] = last_close[-1]

    # A decision at bar t becomes a trade at the open of bar t + 1.
    trade = np.zeros(bars, dtype=bool)
    trade[1:] = ~hold[:-1]
    target = np.zeros((bars, assets))
    target[1:] = decided[:-1]
    untradable = ~np.isfinite(open_)
    dropped = np.where(untradable & trade[:, None], target, 0.0).sum(axis=1)
    target[untradable] = 0.0

    anchor = np.maximum.accumulate(np.where(trade, np.arange(bars), -1))
    invested = anchor >= 0
    anchored = np.where(invested, anchor, 0)
    anchor_weight = np.where(invested[:, None], target[anchored], 0.0)
    anchor_price = price[anchored]
    held_any = anchor_weight > 0
    with np.errstate(invalid="ignore", divide="ignore"):
        value_now = np.where(held_any, anchor_weight * price[:bars] / anchor_price, 0.0)
        value_next = np.where(held_any, anchor_weight * price[1:] / anchor_price, 0.0)
    cash = 1.0 - anchor_weight.sum(axis=1)
    total_now = cash + value_now.sum(axis=1)
    total_next = cash + value_next.sum(axis=1)
    gross = total_next / total_now - 1.0
    held = value_now / total_now[:, None]

    before_trade = np.zeros((bars, assets))
    before_trade[1:] = value_next[:-1] / total_next[:-1, None]
    traded = np.where(trade[:, None], np.abs(target - before_trade), 0.0)
    cost_paid = (traded * np.asarray(cost, dtype="float64") * cost_multiplier).sum(axis=1)
    returns = (1.0 + gross) * (1.0 - cost_paid) - 1.0
    return BacktestResult(returns, gross, cost_paid, traded.sum(axis=1), held, dropped)


def _forward_fill(values: np.ndarray) -> np.ndarray:
    """Each NaN replaced by the last finite value above it in its column."""
    rows = np.where(np.isfinite(values), np.arange(len(values))[:, None], -1)
    last = np.maximum.accumulate(rows, axis=0)
    filled = np.take_along_axis(values, np.maximum(last, 0), axis=0)
    return np.where(last >= 0, filled, np.nan)
