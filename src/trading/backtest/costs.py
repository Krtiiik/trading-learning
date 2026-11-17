"""Cost model: a proportional charge per side on traded notional, no commission."""

import numpy as np

BPS = 1e-4


def trade_cost(traded_notional: float, cost_bps: float) -> float:
    """Dollars lost to slippage and half-spread when trading `traded_notional` dollars.

    `traded_notional` is the sum of absolute dollar amounts bought and sold, so a
    round trip (buy then sell the same amount) pays the rate twice.
    """
    if cost_bps < 0:
        raise ValueError("cost_bps must be non-negative")
    return abs(traded_notional) * cost_bps * BPS


def rebalance(
    position_values: np.ndarray,
    cash: float,
    target_weights: np.ndarray,
    cost_bps: float,
) -> tuple[np.ndarray, float, float, float]:
    """Trade current dollar positions to `target_weights` of the equity left after costs.

    Returns `(new_position_values, new_cash, traded_notional, cost)`. The cost depends
    on the trade size, which depends on post-cost equity, so equity is solved by
    fixed-point iteration (a contraction with ratio about `cost_bps * 1e-4`).
    """
    equity = cash + position_values.sum()
    rate = cost_bps * BPS
    post_equity = equity
    for _ in range(8):
        traded = np.abs(target_weights * post_equity - position_values).sum()
        post_equity = equity - traded * rate
    new_values = target_weights * post_equity
    traded = float(np.abs(new_values - position_values).sum())
    cost = trade_cost(traded, cost_bps)
    new_cash = equity - cost - new_values.sum()
    return new_values, float(new_cash), traded, cost
