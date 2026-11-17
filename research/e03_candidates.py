"""E03: the rule candidates the literature review supports, each run once as specified.

Configurations were written down before the first run (see LOG.md) and are not tuned.

Run: uv run python research/e03_candidates.py
"""

import pandas as pd
import pandas_market_calendars as mcal

from common import (
    EVAL_START,
    SEAL_END,
    evaluate,
    format_table,
    research_market,
    research_prices,
    results_table,
    sub_periods,
)
from e01_baselines import EDGES
from trading.strategies import rules

BAND = 0.05


def nyse_sessions(start: str, end: str) -> pd.DatetimeIndex:
    """NYSE trading days, as tz-naive dates like the bar index."""
    days = mcal.get_calendar("NYSE").valid_days(start, end)
    return pd.DatetimeIndex(days.tz_localize(None), name="date")


def candidates(prices: pd.DataFrame) -> dict[str, tuple[pd.DataFrame, float]]:
    """Name -> (targets, rebalance band)."""
    sessions = nyse_sessions(str(prices.index[0].date()), "2024-12-31")
    trend = rules.inverse_vol_trend(prices, lookback=252, vol_window=60)
    return {
        "TSMOM 12m, 1/N + band": (rules.time_series_momentum(prices, 252), BAND),
        "InvVol trend": (trend, 0.0),
        "InvVol trend + band": (trend, BAND),
        "SPY vol cap 12% + band": (
            rules.volatility_cap(rules.fixed_mix(prices, {"SPY": 1.0}), prices, 0.12, 20),
            BAND,
        ),
        "1/N vol cap 10% + band": (
            rules.volatility_cap(rules.equal_weight(prices), prices, 0.10, 60),
            BAND,
        ),
        "60/40 vol cap 8% + band": (
            rules.volatility_cap(rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4}), prices, 0.08, 20),
            BAND,
        ),
        "Turn of month SPY (-1,+3)": (rules.turn_of_month(prices, sessions, "SPY", 1, 3), 0.0),
    }


if __name__ == "__main__":
    market = research_market()
    prices = research_prices()
    assert prices.index.max() <= pd.Timestamp(SEAL_END)
    specs = candidates(prices)

    for cost in (5.0, 2.0):
        results = {
            name: evaluate(market, targets, cost_bps=cost, rebalance_band=band)
            for name, (targets, band) in specs.items()
        }
        print(f"\n### {EVAL_START} .. seal, fill at next open, {cost:g} bps per side\n")
        print(format_table(results_table(results)))

    results = {
        name: evaluate(market, targets, rebalance_band=band) for name, (targets, band) in specs.items()
    }
    print("\n### Sharpe by sub-period (5 bps)\n")
    for name, result in results.items():
        parts = sub_periods(result, EDGES)
        print(f"{name:<28}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))

    print("\n### Average weight in cash (5 bps)\n")
    for name, result in results.items():
        print(f"{name:<28}{1 - result.weights.sum(axis=1).mean():.1%}")

    close_fill = {
        name: evaluate(market, targets, fill="close", rebalance_band=band)
        for name, (targets, band) in specs.items()
    }
    print("\n### Fill at next close (5 bps)\n")
    print(format_table(results_table(close_fill)))
