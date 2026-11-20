"""H2003: a coin's recent volatility ranks its return over the next week, in reverse.

The signal is the standard deviation of the last `lookback_days` daily close-to-close returns.
The test is the mean rank correlation, across universe members, between it and the return over
the next `horizon_days` bars from the next open; the hypothesis predicts a negative one.
"""

import pandas as pd

from trading.experiments.crosssection_tools import volatility
from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return volatility(data.market("1d"), int(params["lookback_days"]))


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    horizon = int(ctx.params["horizon_days"])
    return evaluate_predictor(ctx, panel, "1d", horizon, method="rank_ic", start=ctx.params["start"])
