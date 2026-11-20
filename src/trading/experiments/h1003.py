"""H1003: returns over 21:00 to 23:00 UTC against returns over the other hours of the day.

The predictor is a dummy on the hourly bars whose close starts one of the two hours: a signal
at the close of the bar labelled 20:00 earns the open of 21:00 to the open of 22:00.
"""

import pandas as pd

from trading.experiments.timeseries_tools import calendar_dummy
from trading.research.evaluate import Context, Result, evaluate_predictor
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return calendar_dummy(data.market("1h"), hours=params["signal_hours"])


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return evaluate_predictor(ctx, panel, "1h", horizon=1, method="panel", start=ctx.params["start"])
