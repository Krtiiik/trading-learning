"""H1002: a coin's return over the last hour against its return over the next hour.

The predictor is the hourly bar's own open-to-close return in units of the coin's recent
hourly volatility. The forward return runs from the next bar's open, so the two share no price.
"""

import pandas as pd

from trading.experiments.timeseries_tools import bar_return_zscore
from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return bar_return_zscore(data.market("1h"), int(params["volatility_hours"]), int(params["min_hours"]))


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return evaluate_predictor(ctx, panel, "1h", horizon=1, method="panel", start=ctx.params["start"])
