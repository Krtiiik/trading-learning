"""H1001: a coin is held only while its close is above its own moving average.

Every universe member with a bar has an equal slot. The slot holds the coin while the coin's
close is above the mean of its last `lookback_days` closes, and cash otherwise. The benchmark
fills every slot on the same schedule, so the two differ by the trend filter and nothing else.
"""

import pandas as pd

from trading.research.evaluate import Context, Result, equal_weight, evaluate_strategy, rebalance_labels
from trading.research.market import Market, ResearchData

SAME_SCHEDULE = "equal_weight_same_schedule"
"""The registered benchmark: the equal-weight universe rebalanced whenever the strategy decides."""


def slots(market: Market, params: dict) -> pd.DataFrame:
    """One equal share per universe member that has a bar, at each of the rule's decisions."""
    return equal_weight(market, rebalance_labels(market, params["rebalance"]))


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    """Target weights: a slot's coin while it trends up, nothing while it does not.

    The average needs a close on each of the last `lookback_days` bars. Without that the
    comparison is false, so a coin with a short or broken history is flat.
    """
    market = data.market("1d")
    close = market.frame("close")
    lookback = int(params["lookback_days"])
    average = close.rolling(lookback, min_periods=lookback).mean()
    share = slots(market, params)
    return share.where((close > average).loc[share.index], 0.0)


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    name = ctx.params["benchmark"]
    benchmark = slots(ctx.data.market("1d"), ctx.params) if name == SAME_SCHEDULE else name
    return evaluate_strategy(ctx, panel, "1d", benchmark=benchmark, start=ctx.params["start"])
