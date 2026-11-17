"""Shared setup for the research scripts: sealed data loading and result formatting.

Everything here stops at `SEAL_END`. The holdout (2024-11-17 onward) is only ever
loaded by `research/holdout.py`, once, at the very end.
"""

import pandas as pd

from trading.backtest import BacktestResult, Market, run_backtest, summarize
from trading.data import load_panel
from trading.data.universe import load_universe

HOLDOUT_START = "2024-11-17"
SEAL_END = "2024-11-16"  # last date research may see (inclusive)
EVAL_START = "2005-01-03"  # first day of every walk-forward comparison
INITIAL_CASH = 10_000.0
COST_BPS = 5.0  # per side; the pessimistic end of the 2-5 bps brief

SYMBOLS = load_universe()


def research_market() -> Market:
    """Raw prices and dividends for the universe, truncated before the holdout."""
    return Market.from_store(SYMBOLS, end=SEAL_END)


def research_prices() -> pd.DataFrame:
    """Adjusted-close panel for signals, truncated before the holdout."""
    return load_panel(SYMBOLS, "adj_close", end=SEAL_END)


def evaluate(
    market: Market,
    targets: pd.DataFrame,
    *,
    cost_bps: float = COST_BPS,
    fill: str = "open",
    rebalance_band: float = 0.0,
    start: str = EVAL_START,
    end: str | None = None,
) -> BacktestResult:
    return run_backtest(
        market,
        targets,
        initial_cash=INITIAL_CASH,
        cost_bps=cost_bps,
        fill=fill,  # type: ignore[arg-type]
        rebalance_band=rebalance_band,
        start=start,
        end=end,
    )


def results_table(results: dict[str, BacktestResult]) -> pd.DataFrame:
    """One row of headline numbers per strategy."""
    return pd.DataFrame({name: summarize(result) for name, result in results.items()}).T


def format_table(table: pd.DataFrame) -> str:
    """The results table as a Markdown table with readable units."""
    shown = pd.DataFrame(
        {
            "net P&L $": table["net_pnl"].map("{:,.0f}".format),
            "$/yr": table["pnl_per_year"].map("{:,.0f}".format),
            "CAGR": table["cagr"].map("{:.1%}".format),
            "vol": table["vol"].map("{:.1%}".format),
            "Sharpe": table["sharpe"].map("{:.2f}".format),
            "maxDD": table["max_drawdown"].map("{:.1%}".format),
            "turnover/yr": table["turnover"].map("{:.1f}x".format),
            "costs $": table["costs"].map("{:,.0f}".format),
        }
    )
    header = "| strategy | " + " | ".join(shown.columns) + " |"
    rule = "|---|" + "---:|" * len(shown.columns)
    rows = [f"| {name} | " + " | ".join(row) + " |" for name, row in shown.iterrows()]
    return "\n".join([header, rule, *rows])


def sub_periods(result: BacktestResult, edges: list[str]) -> pd.DataFrame:
    """Sharpe and annualised return of a result within consecutive date ranges."""
    returns = result.returns
    rows = {}
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        part = returns.loc[lo:hi]
        if len(part) < 20:
            continue
        growth = (1 + part).prod() ** (252 / len(part)) - 1
        rows[f"{lo[:4]}-{hi[:4]}"] = {
            "cagr": growth,
            "sharpe": part.mean() / part.std() * 252**0.5,
        }
    return pd.DataFrame(rows).T
