"""Shared by the cross-market experiments on links inside the crypto market (H4001 to H4004).

Signals here are bars x coins frames whose row t uses bars labelled t or earlier only. Returns
over a lookback are taken on the full grid of bar labels, so a lookback of N bars is N bar
lengths of time even next to an exchange outage (the hourly index has no row for a missing
hour); where either end of the window has no bar the return is NaN.
"""

from dataclasses import replace

import numpy as np
import pandas as pd

from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import Market

BTC = "BTCUSDT"


def on_grid(market: Market, frame: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """The frame on every bar label between its first and last, missing bars as NaN rows."""
    step = "D" if market.granularity == "1d" else "h"
    return frame.reindex(pd.date_range(frame.index[0], frame.index[-1], freq=step))


def grid_return(market: Market, lookback: int, skip: int = 0) -> pd.DataFrame:
    """Each coin's close-to-close return over exactly `lookback` bar lengths.

    The window ends at the close of the bar `skip` bar lengths before row t (0: the bar's own
    close). NaN where either end of the window has no bar.
    """
    close = on_grid(market, market.frame("close"))
    change = close / close.shift(lookback) - 1.0
    return change.shift(skip).reindex(market.index)


def traded(market: Market) -> np.ndarray:
    """Coin-bars with a bar in which something traded: their close is a price of that bar."""
    return np.isfinite(market.close) & (market.quote_volume > 0)


def leader_signal(market: Market, leader: str, lookback: int, skip: int = 0) -> pd.DataFrame:
    """The leader's past return as every other coin's predictor.

    Row t holds, for each coin but the leader, the leader's return over the `lookback` bar
    lengths ending `skip` bars before the close of bar t. It is NaN in the leader's own column
    and for a coin whose bar t is missing or had no trade (its last price is stale, and so may
    be the next open).
    """
    past = grid_return(market, lookback, skip)[leader].to_numpy()
    signal = np.where(traded(market), past[:, None], np.nan)
    signal[:, market.column(leader)] = np.nan
    return market.frame(signal)


def only_tiers(market: Market, signal: pd.DataFrame, tiers: tuple[int, ...]) -> pd.DataFrame:
    """The signal for coins whose liquidity tier at the bar is one of `tiers`, NaN elsewhere."""
    return signal.where(np.isin(market.tier, tiers))


def with_diagnostics(
    ctx: Context,
    result: Result,
    variants: dict[str, pd.DataFrame],
    granularity: str,
    horizon: int,
    method: str,
    start: str | None,
) -> Result:
    """Add the same test on other signals to a result's metrics. They decide nothing."""
    extra = {}
    for name, signal in variants.items():
        other = evaluate_predictor(ctx, signal, granularity, horizon, method=method, start=start)  # type: ignore[arg-type]
        extra[name] = {
            "estimate": other.estimate,
            "p_value": other.p_value,
            "n": other.n,
            "standard_error": other.metrics.get("standard_error"),
        }
    return replace(result, metrics=result.metrics | {"diagnostics": extra})


def leader_panel(market: Market, params: dict) -> pd.DataFrame:
    """The registered leader signal of H4001 and H4002, from the hypothesis's parameters."""
    return leader_signal(market, params["leader"], int(params["lookback_bars"]), int(params["skip_bars"]))


def leader_test(ctx: Context, panel: pd.DataFrame, granularity: str) -> Result:
    """Pooled slope of the other members' next return on the leader's past return.

    The diagnostics repeat the test with one more bar between signal and return (a lagged-price
    artefact would vanish there) and within liquidity tiers. They decide nothing.
    """
    market = ctx.data.market(granularity)  # type: ignore[arg-type]
    params = ctx.params
    horizon, start = int(params["horizon_bars"]), params["start"]
    result = evaluate_predictor(ctx, panel, granularity, horizon, method="panel", start=start)
    variants = {
        "one_more_bar_skipped": leader_panel(market, params | {"skip_bars": int(params["skip_bars"]) + 1}),
        "tiers_1_and_2": only_tiers(market, panel, (1, 2)),
        "tier_3": only_tiers(market, panel, (3,)),
    }
    return with_diagnostics(ctx, result, variants, granularity, horizon, "panel", start)
