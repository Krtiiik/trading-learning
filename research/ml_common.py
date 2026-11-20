"""Shared pieces of the learned-strategy experiments: sealed features and walk-forward folds."""

import pandas as pd

from common import SEAL_END, SYMBOLS
from trading.data import load_panel
from trading.strategies.features import feature_panels, forward_return, stack

HORIZON = 5
FIRST_TEST_YEAR = 2005
LAST_TEST_YEAR = 2024


def sealed_features() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Feature panels and the adjusted-close panel, truncated before the holdout."""
    panel = lambda field: load_panel(SYMBOLS, field, end=SEAL_END)
    adj_close = panel("adj_close")
    return feature_panels(adj_close, panel("high"), panel("low"), panel("close")), adj_close


def training_table(panels: dict[str, pd.DataFrame], adj_close: pd.DataFrame) -> pd.DataFrame:
    """Long (date, symbol) table of features plus the clipped forward-return label."""
    label = forward_return(adj_close, HORIZON).clip(-3.0, 3.0)
    return stack({**panels, "label": label})


def folds(dates: pd.DatetimeIndex) -> list[tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp]]:
    """(last usable training date, test start, test end) for each test year.

    Training stops `HORIZON` sessions before the test year, so no training label is
    computed from a price inside the test year.
    """
    out = []
    for year in range(FIRST_TEST_YEAR, LAST_TEST_YEAR + 1):
        test = dates[dates.year == year]
        before = dates[dates < test[0]]
        out.append((before[-HORIZON - 1], test[0], test[-1]))
    return out
