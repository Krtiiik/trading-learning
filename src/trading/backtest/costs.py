"""The trading cost model: an exchange fee plus slippage by liquidity tier, per side."""

import numpy as np

FEE = 0.0010
"""Exchange fee per side: 10 bps."""

SLIPPAGE: dict[int, float] = {1: 0.0002, 2: 0.0005, 3: 0.0015}
"""Slippage per side by liquidity tier: BTC and ETH, the next ten coins by volume, the rest."""

DOUBLE_COST = 2.0
"""Every trading claim is also reported with all costs multiplied by this."""


def cost_per_side(tier: np.ndarray) -> np.ndarray:
    """Fee plus slippage for a panel of liquidity tiers (anything not tier 1 or 2 costs tier 3)."""
    tier = np.asarray(tier)
    slippage = np.full(tier.shape, SLIPPAGE[3])
    slippage[tier == 1] = SLIPPAGE[1]
    slippage[tier == 2] = SLIPPAGE[2]
    return FEE + slippage
