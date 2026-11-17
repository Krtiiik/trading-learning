"""Per-symbol features for learned strategies, each known at the close of its date.

Every feature is scaled by the symbol's own recent volatility (or is already unit-free),
so one model can be shared across ETFs as different as TLT and SLV.
"""

import numpy as np
import pandas as pd

FEATURES: tuple[str, ...] = (
    "mom_21",
    "mom_63",
    "mom_126",
    "mom_252",
    "rev_5",
    "trend_200",
    "vol_ratio",
    "vol_level",
    "ibs",
)

_VOL_WINDOW = 60


def feature_panels(
    adj_close: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    """One date-by-symbol panel per feature in `FEATURES`.

    Momentum, reversal and trend are returns divided by the volatility expected over
    their horizon, so they read as "how many standard deviations did it move".
    """
    returns = adj_close.pct_change(fill_method=None)
    daily_vol = returns.rolling(_VOL_WINDOW).std()

    def scaled_return(days: int) -> pd.DataFrame:
        return (adj_close / adj_close.shift(days) - 1.0) / (daily_vol * np.sqrt(days))

    spread = (high - low).where(high > low)
    panels = {
        "mom_21": scaled_return(21),
        "mom_63": scaled_return(63),
        "mom_126": scaled_return(126),
        "mom_252": scaled_return(252),
        "rev_5": scaled_return(5),
        "trend_200": (adj_close / adj_close.rolling(200).mean() - 1.0)
        / (daily_vol * np.sqrt(100)),
        "vol_ratio": returns.rolling(20).std() / daily_vol,
        "vol_level": daily_vol * np.sqrt(252),
        "ibs": ((close - low) / spread).fillna(0.5).where(close.notna()),
    }
    return {name: panels[name] for name in FEATURES}


def forward_return(adj_close: pd.DataFrame, days: int) -> pd.DataFrame:
    """Return over the next `days` sessions divided by its expected volatility.

    This is a training label: the value on date t uses prices up to t + `days`.
    """
    daily_vol = adj_close.pct_change(fill_method=None).rolling(_VOL_WINDOW).std()
    return (adj_close.shift(-days) / adj_close - 1.0) / (daily_vol * np.sqrt(days))


def stack(panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Panels as one long table indexed by (date, symbol), rows with any NaN dropped."""
    table = pd.concat({name: panel.stack(future_stack=True) for name, panel in panels.items()}, axis=1)
    table.index.names = ["date", "symbol"]
    return table.dropna()
