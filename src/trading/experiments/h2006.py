"""H2006: the one-day reversal across coins is stronger after abnormally low volume."""

import numpy as np
import pandas as pd

from trading.experiments.crosssection_tools_b import evaluate_rank_ic_by_thirds
from trading.research.evaluate import Context, Result
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    """Each coin's daily return and volume shock, side by side under the keys `return` and `shock`.

    The shock is the log of the day's quote volume minus the log of its mean over the previous
    `shock_days` days, over the standard deviation of log quote volume in those same days. A
    day without volume in the window gives no shock.
    """
    market = data.market("1d")
    close = market.frame("close")
    days = int(params["shock_days"])
    volume = market.frame("quote_volume")
    volume = volume.where(volume > 0)
    log_volume = np.log(volume)
    before = volume.shift(1).rolling(days, min_periods=days).mean()
    spread = log_volume.shift(1).rolling(days, min_periods=days).std()
    shock = (log_volume - np.log(before)) / spread.where(spread > 0)
    return pd.concat({"return": close / close.shift(1) - 1, "shock": shock}, axis=1)


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return evaluate_rank_ic_by_thirds(
        ctx, panel["return"], panel["shock"], "1d", horizon=int(ctx.params["horizon_days"]), start=ctx.params["start"]
    )
