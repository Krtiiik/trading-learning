"""H1004: returns over the UTC Friday against returns over the other days of the week.

The predictor is a dummy on the daily bar labelled Thursday: a signal at its close earns the
open of Friday's bar to the open of Saturday's, which is the UTC day Friday.
"""

import pandas as pd

from trading.experiments.timeseries_tools import calendar_dummy
from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return calendar_dummy(data.market("1d"), weekdays=[params["signal_weekday"]])


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return evaluate_predictor(ctx, panel, "1d", horizon=1, method="panel", start=ctx.params["start"])
