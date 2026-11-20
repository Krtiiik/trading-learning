"""H4005: a rise in the exchange's total volume today is followed by a higher Bitcoin return tomorrow."""

import pandas as pd

from trading.experiments.crossmarket_tools_b import market_test, volume_growth
from trading.research.evaluate import Context, Result
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    """Day-on-day change in the log of the members' total quote volume, known at the bar's close."""
    return volume_growth(data.market("1d"), float(params["clip"])).to_frame()


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return market_test(ctx, panel, "1d", other_target="equal_weight")
