"""The sealed holdout: run ONCE, at the very end, for the one chosen finalist.

This is the only file that reads bars from 2024-11-17 onward. It refuses to run a second
time: the result is written to `research/holdout_result.txt` and that file's existence
blocks a rerun, so the number cannot be quietly improved.

The account starts with $10,000 on the first holdout session. Signals use all history up
to each decision date (the row decided on 2024-11-15 is the first one traded). Baselines
are run on the same days for comparison only; the finalist was fixed before this ran.

Run: uv run python research/holdout.py
     uv run python research/holdout.py --rehearsal   (same code on sealed data only,
         2022-11-17 .. 2024-11-15, writes nothing; used to check the script before the real run)
"""

import sys
from pathlib import Path

import pandas as pd

from common import (
    COST_BPS,
    HOLDOUT_START,
    INITIAL_CASH,
    SEAL_END,
    SYMBOLS,
    format_table,
    results_table,
)
from trading.backtest import Market, run_backtest
from trading.data import load_panel
from trading.strategies import rules

RESULT = Path(__file__).parent / "holdout_result.txt"

# The finalist, fixed from the walk-forward results (see REPORT.md) before running.
FINALIST = "Trend-switched + capped 60/40"

if __name__ == "__main__":
    rehearsal = "--rehearsal" in sys.argv
    if not rehearsal and RESULT.exists():
        sys.exit(f"{RESULT.name} already exists: the holdout has been run. Read it; do not rerun.")

    data_end = SEAL_END if rehearsal else None
    window_start = "2022-11-17" if rehearsal else HOLDOUT_START
    market = Market.from_store(SYMBOLS, end=data_end)
    prices = load_panel(SYMBOLS, "adj_close", end=data_end)
    mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})

    strategies = {
        FINALIST: (
            rules.volatility_cap(rules.trend_switched_mix(prices), prices, 0.08, 20),
            0.05,
        ),
        "Capped 60/40 (comparison only)": (rules.volatility_cap(mix, prices, 0.08, 20), 0.05),
        "SPY buy & hold": (rules.fixed_mix(prices, {"SPY": 1.0}), 0.0),
        "Equal weight (1/N)": (rules.equal_weight(prices), 0.0),
        "60/40 SPY/IEF": (mix, 0.0),
        "TSMOM 12m, 1/N": (rules.time_series_momentum(prices, 252), 0.0),
        "SPY>SMA200 else IEF": (rules.trend_filter(prices, "SPY", "IEF", 200), 0.0),
    }

    lines = [
        ("REHEARSAL on sealed data, not the holdout" if rehearsal else "Holdout")
        + f" run at {pd.Timestamp.now():%Y-%m-%d %H:%M}",
        f"Finalist: {FINALIST}",
        f"Window: {window_start} .. {market.dates.max().date()}, "
        f"${INITIAL_CASH:,.0f}, next-open fill",
    ]
    for cost in (COST_BPS, 2.0):
        results = {
            name: run_backtest(
                market, targets, initial_cash=INITIAL_CASH, cost_bps=cost,
                rebalance_band=band, start=window_start,
            )
            for name, (targets, band) in strategies.items()
        }
        lines += ["", f"### {cost:g} bps per side", "", format_table(results_table(results))]
        if cost == COST_BPS:
            finalist = results[FINALIST]
            lines += [
                "",
                f"Finalist sessions: {len(finalist.equity)}  "
                f"final equity ${finalist.equity.iloc[-1]:,.2f}  "
                f"average invested {finalist.weights.sum(axis=1).mean():.0%}",
            ]

    text = "\n".join(lines) + "\n"
    if not rehearsal:
        RESULT.write_text(text, encoding="utf-8")
    print(text)
