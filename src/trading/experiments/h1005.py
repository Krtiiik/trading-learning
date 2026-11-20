"""H1005: the equal-weight universe held at reduced exposure while its volatility is unusually high.

Both portfolios hold every universe member in equal shares and decide on the same schedule.
The strategy multiplies the shares by the universe's usual volatility over its recent
volatility, capped at 1; the benchmark never scales. They differ by the scaling and nothing else.
"""

import pandas as pd

from trading.experiments.timeseries_tools import universe_return, volatility_scale
from trading.research.evaluate import Context, Result, equal_weight, evaluate_strategy, rebalance_labels
from trading.research.market import Market, ResearchData


def slots(market: Market, params: dict) -> pd.DataFrame:
    """One equal share per universe member that has a bar, at each decision: the benchmark."""
    return equal_weight(market, rebalance_labels(market, params["rebalance"]))


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    market = data.market("1d")
    share = slots(market, params)
    scale = volatility_scale(universe_return(market), int(params["recent_days"]), int(params["usual_days"]))
    return share.mul(scale.loc[share.index], axis=0)


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    benchmark = slots(ctx.data.market("1d"), ctx.params)
    return evaluate_strategy(ctx, panel, "1d", benchmark=benchmark, start=ctx.params["start"])
