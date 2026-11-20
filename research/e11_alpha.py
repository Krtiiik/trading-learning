"""E11: how much of each rule's profit is more than stock and bond exposure?

No new configurations. Each rule's daily net returns (5 bps) are regressed on the daily
returns of buy-and-hold SPY and IEF. The intercept is what the rule earned beyond a
static stock/bond mix with the same average exposure: its "alpha", here in dollars per
year on $10,000. t-statistics use Newey-West standard errors (20 lags).

Run: uv run python research/e11_alpha.py
"""

import numpy as np
import pandas as pd

from common import blend, evaluate, research_market, research_prices
from e03_candidates import nyse_sessions
from trading.strategies import rules

market = research_market()
prices = research_prices()
mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
capped = rules.volatility_cap(mix, prices, 0.08, 20)
trend = rules.inverse_vol_trend(prices, 252, 60)
sessions = nyse_sessions(str(prices.index[0].date()), "2024-12-31")

RULES = {
    "Equal weight (1/N)": (rules.equal_weight(prices), 0.0),
    "60/40 SPY/IEF": (mix, 0.0),
    "TSMOM 12m, 1/N": (rules.time_series_momentum(prices, 252), 0.0),
    "SPY>SMA200 else IEF": (rules.trend_filter(prices, "SPY", "IEF", 200), 0.0),
    "RSI2 pullback SPY": (rules.rsi_pullback(prices, "SPY"), 0.0),
    "XS 5d reversal, 5 worst": (rules.cross_sectional_reversal(prices, 5, 5), 0.0),
    "Turn of month SPY": (rules.turn_of_month(prices, sessions, "SPY", 1, 3), 0.0),
    "InvVol trend + band": (trend, 0.05),
    "Capped 60/40": (capped, 0.05),
    "Blend trend + capped": (blend([(0.5, trend), (0.5, capped)]), 0.05),
}


def newey_west(x: np.ndarray, residual: np.ndarray, lags: int) -> np.ndarray:
    """Covariance of OLS coefficients robust to autocorrelation and heteroskedasticity."""
    n = len(x)
    xtx_inv = np.linalg.inv(x.T @ x)
    scores = x * residual[:, None]
    meat = scores.T @ scores
    for lag in range(1, lags + 1):
        weight = 1 - lag / (lags + 1)
        cross = scores[lag:].T @ scores[:-lag]
        meat += weight * (cross + cross.T)
    return xtx_inv @ meat @ xtx_inv * n / (n - x.shape[1])


factors = pd.DataFrame({
    "SPY": evaluate(market, rules.fixed_mix(prices, {"SPY": 1.0}), cost_bps=0.0).returns,
    "IEF": evaluate(market, rules.fixed_mix(prices, {"IEF": 1.0}), cost_bps=0.0).returns,
})

print(f"{'rule':<26}{'b_SPY':>7}{'b_IEF':>7}{'alpha %/yr':>12}{'alpha $/yr':>12}{'t':>7}{'R2':>6}")
for name, (targets, band) in RULES.items():
    y = evaluate(market, targets, rebalance_band=band).returns
    data = pd.concat([y.rename("y"), factors], axis=1).dropna()
    x = np.column_stack([np.ones(len(data)), data["SPY"], data["IEF"]])
    beta, *_ = np.linalg.lstsq(x, data["y"].to_numpy(), rcond=None)
    residual = data["y"].to_numpy() - x @ beta
    covariance = newey_west(x, residual, 20)
    alpha_year = beta[0] * 252
    t_stat = beta[0] / np.sqrt(covariance[0, 0])
    r2 = 1 - residual.var() / data["y"].var()
    print(f"{name:<26}{beta[1]:>7.2f}{beta[2]:>7.2f}{alpha_year:>11.1%} {alpha_year * 10_000:>11,.0f}{t_stat:>7.2f}{r2:>6.2f}")
