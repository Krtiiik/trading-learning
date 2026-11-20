"""H2001: a coin's return over the past three weeks ranks its return over the next week.

The signal is the close over the close `lookback_days` bars earlier, minus one. The test is the
mean rank correlation, across universe members, between it and the return over the next
`horizon_days` bars from the next open.
"""

import pandas as pd

from trading.experiments.crosssection_tools import past_return
from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return past_return(data.market("1d"), int(params["lookback_days"]))


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    horizon = int(ctx.params["horizon_days"])
    return evaluate_predictor(ctx, panel, "1d", horizon, method="rank_ic", start=ctx.params["start"])
