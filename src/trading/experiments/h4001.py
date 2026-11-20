"""H4001: Bitcoin's return over the last hour against the other members' return over the next hour."""

import pandas as pd

from trading.experiments.crossmarket_tools import leader_panel, leader_test
from trading.research.evaluate import Context, Result
from trading.research.market import ResearchData


def panel(data: ResearchData, params: dict) -> pd.DataFrame:
    return leader_panel(data.market("1h"), params)


def test(ctx: Context, panel: pd.DataFrame) -> Result:
    return leader_test(ctx, panel, "1h")
