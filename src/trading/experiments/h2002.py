"""H2002: a coin's return on one day ranks its return on the next day, in reverse.

The signal is the close-to-close return of bar t (`lookback_days` is 1). The test is the mean
rank correlation, across universe members, between it and the return over the next
`horizon_days` bars from the next open; the hypothesis predicts a negative one.
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
