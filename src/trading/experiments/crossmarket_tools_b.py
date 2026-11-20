"""Shared by the cross-market experiments on links to the outside world (H4005 to H4008).

Every signal here is one market-wide series indexed by crypto bar labels. Row t uses only what
is knowable when crypto bar t closes.
"""

from dataclasses import replace

import numpy as np
import pandas as pd

from trading.research.evaluate import Context, Result, evaluate_market_predictor
from trading.research.market import Market

SIGNAL = "signal"
"""The single column of a market-wide panel."""


def volume_growth(market: Market, clip: float) -> pd.Series:
    """Change from the previous bar in the log of the members' total quote volume.

    Both bars are summed over the same coins: the members in force at bar t that have a bar at
    t and at t-1, so a reconstitution does not show up as a jump in volume. The change is
    limited to plus or minus `clip`: a bar cut short by an exchange outage would otherwise be
    the largest "shock" in the sample.
    """
    quote = market.frame("quote_volume")
    before = quote.shift(1)
    counted = market.member & quote.notna().to_numpy() & before.notna().to_numpy()
    now = quote.where(counted).sum(axis=1, min_count=1)
    prior = before.where(counted).sum(axis=1, min_count=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        change = np.log(now / prior)
    return change.clip(-clip, clip).rename(SIGNAL)


def market_test(ctx: Context, panel: pd.DataFrame, granularity: str, other_target: str | None = None) -> Result:
    """Slope of the market's next return on the panel's one series, as the hypothesis registered it.

    Reads `horizon_bars`, `target` and an optional `start` from the parameters. `other_target`
    repeats the test on a second target as a diagnostic that decides nothing.
    """
    params = ctx.params
    horizon, start = int(params["horizon_bars"]), params.get("start")
    result = evaluate_market_predictor(ctx, panel[SIGNAL], granularity, horizon, params["target"], start)
    if other_target is None:
        return result
    other = evaluate_market_predictor(ctx, panel[SIGNAL], granularity, horizon, other_target, start)
    diagnostic = {
        "target": other_target,
        "estimate": other.estimate,
        "p_value": other.p_value,
        "n": other.n,
        "standard_error": other.metrics.get("standard_error"),
    }
    return replace(result, metrics=result.metrics | {"diagnostic_other_target": diagnostic})
