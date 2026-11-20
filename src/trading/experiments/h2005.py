"""H2005: a coin's close relative to its high of the past week ranks next week's returns."""

import pandas as pd

from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    """Close over the highest high of the last `high_days` bars (the signal bar included)."""
    market = data.market("1d")
    days = int(params["high_days"])
    highest = market.frame("high").rolling(days, min_periods=days).max()
    return market.frame("close") / highest


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return evaluate_predictor(
        ctx, panel, "1d", horizon=int(ctx.params["horizon_days"]), method="rank_ic", start=ctx.params["start"]
    )
