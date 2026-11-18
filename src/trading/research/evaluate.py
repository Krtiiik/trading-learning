"""Building blocks for experiments: benchmarks, forward returns, and the two standard tests.

An experiment computes a panel (target weights or a predictor) and hands it to
`evaluate_strategy` or `evaluate_predictor`, which run it over the segment's window with the
project's conventions (next-open fills, tiered costs, double cost, the same engine for the
benchmark) and return the `Result` the harness records.
"""

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
import pandas as pd

from trading import stats
from trading.backtest import DOUBLE_COST, BacktestResult, periods_per_year, run_backtest, summarize
from trading.data.bars import bar_length
from trading.research.market import Market, ResearchData
from trading.research.registry import Hypothesis
from trading.research.split import Segment, Window

BTC = "BTCUSDT"


@dataclass(frozen=True)
class Result:
    """What a primary test returns. The harness adds everything else to the run record."""

    estimate: float
    """The effect in the unit the hypothesis declared (for a trading claim: net of costs)."""
    p_value: float
    """One-sided, in the direction the hypothesis predicted."""
    n: int
    metrics: dict[str, Any] = field(default_factory=dict)
    double_cost_estimate: float | None = None
    double_cost_p_value: float | None = None
    """The same test at twice the trading costs; required for trading claims."""


@dataclass
class Context:
    """What the harness hands to an experiment's `test` function."""

    hypothesis: Hypothesis
    segment: Segment
    window: Window
    data: ResearchData
    params: dict[str, Any]
    seed: int

    @property
    def alternative(self) -> stats.Alternative:
        return "greater" if self.hypothesis.direction == "positive" else "less"

    def inside(self, index: pd.DatetimeIndex, start: str | None = None) -> np.ndarray:
        """Which bar labels the test evaluates: the segment's window, optionally from `start` on.

        `start` (a day, declared in the hypothesis's parameters) can only narrow the window,
        for instance to begin when the universe first has 40 members.
        """
        inside = self.window.mask(index).to_numpy()
        if start is not None:
            inside = inside & Window(pd.Timestamp(start), None).mask(index).to_numpy()
        if not inside.any():
            raise ValueError(f"no bars to evaluate on {self.segment} from {start}")
        return inside


# Weights


def to_weights(market: Market, frame: pd.DataFrame) -> np.ndarray:
    """A weights frame as the engine's array: rows the frame lacks become "hold" rows.

    The frame may list only the bars at which the strategy rebalances and only the coins it
    holds; within a listed row, coins not mentioned get weight 0.
    """
    unknown = frame.columns.difference(list(market.symbols))
    if len(unknown):
        raise ValueError(f"weights name coins the market does not have: {list(unknown)[:5]}")
    if len(frame.index.difference(market.index)):
        raise ValueError("weights have rows that are not bar labels of the market")
    listed = frame.reindex(columns=list(market.symbols)).fillna(0.0)
    return listed.reindex(market.index).to_numpy("float64")


def backtest(market: Market, weights: pd.DataFrame, cost_multiplier: float = 1.0) -> BacktestResult:
    return run_backtest(to_weights(market, weights), market.open, market.close, market.cost, cost_multiplier)


def rebalance_labels(market: Market, frequency: Literal["bar", "week", "month"]) -> pd.DatetimeIndex:
    """Bar labels at which a strategy decides: every bar, or the last bar of each week or month.

    Deciding at the close of a period's last bar trades at the open of the next period's first.
    Whether a bar is the last of its period follows from the calendar, not from which bars
    come after it, so the answer does not change when later data is removed.
    """
    if frequency == "bar":
        return market.index
    naive = market.index.tz_localize(None) if market.index.tz is not None else market.index
    code = "W-SUN" if frequency == "week" else "M"
    closes = naive + bar_length(market.granularity)
    return market.index[naive.to_period(code) != closes.to_period(code)]


def equal_weight(market: Market, labels: pd.DatetimeIndex | None = None) -> pd.DataFrame:
    """Equal weights over the universe members that have a bar, at the given decision labels.

    By default it rebalances at the last bar of each month, to the membership that takes effect
    with the next bar (the new month's reconstitution, known since the month's last close).
    """
    labels = rebalance_labels(market, "month") if labels is None else labels
    rows = market.index.get_indexer(labels)
    eligible = market.member_next[rows] & np.isfinite(market.close[rows])
    count = eligible.sum(axis=1, keepdims=True)
    weights = np.divide(eligible, count, out=np.zeros(eligible.shape), where=count > 0)
    return pd.DataFrame(weights, index=labels, columns=list(market.symbols))


def buy_and_hold(market: Market, symbol: str = BTC) -> pd.DataFrame:
    """All of the portfolio in one coin from its first bar, never rebalanced."""
    first = int(np.argmax(np.isfinite(market.close[:, market.column(symbol)])))
    return pd.DataFrame({symbol: [1.0]}, index=market.index[first : first + 1])


def cash(market: Market) -> pd.DataFrame:
    return pd.DataFrame({market.symbols[0]: [0.0]}, index=market.index[:1])


# Forward returns for predictive claims


def forward_returns(market: Market, horizon: int) -> np.ndarray:
    """Return a trader acting on bar t's close can earn: open of t+1 to open of t+1+horizon.

    NaN where either open is missing, which drops every label whose horizon runs past the end
    of the data, and so past the segment boundary.
    """
    forward = np.full(market.open.shape, np.nan)
    entry, exit_ = market.open[1:-horizon], market.open[1 + horizon :]
    forward[: len(entry)] = exit_ / entry - 1.0
    return forward


# The two standard primary tests


def evaluate_strategy(
    ctx: Context,
    weights: pd.DataFrame,
    granularity: str,
    benchmark: pd.DataFrame | Literal["btc", "equal_weight", "cash"] = "equal_weight",
    statistic: Literal["sharpe", "mean"] = "sharpe",
    draws: int = 2000,
    start: str | None = None,
) -> Result:
    """Is the strategy's net Sharpe ratio (or mean return) above the benchmark's, inside the window?

    Both run through the same engine and costs from the first bar of the data, so positions
    carried into the window are the ones the rule would really hold; only the window's bars are
    compared (from `start` on, if the hypothesis declares a later first day). The estimate is strategy minus benchmark, annualised, at normal cost; the same
    difference at double cost is reported alongside. The p-value comes from a paired block bootstrap.
    """
    market = ctx.data.market(granularity)  # type: ignore[arg-type]
    periods = periods_per_year(market.granularity)
    inside = ctx.inside(market.index, start)
    named = {"btc": buy_and_hold, "equal_weight": equal_weight, "cash": cash}
    benchmark_weights = named[benchmark](market) if isinstance(benchmark, str) else benchmark

    def compare(multiplier: float) -> tuple[stats.TestResult, BacktestResult, BacktestResult]:
        ours = backtest(market, weights, multiplier)
        theirs = backtest(market, benchmark_weights, multiplier)
        test = stats.block_bootstrap_difference(
            ours.returns[inside],
            theirs.returns[inside],
            statistic=statistic,
            periods=periods,
            draws=draws,
            seed=ctx.seed,
            alternative=ctx.alternative,
        )
        return test, ours, theirs

    normal, ours, theirs = compare(1.0)
    doubled, ours_doubled, _ = compare(DOUBLE_COST)
    metrics: dict[str, Any] = {
        "statistic": f"difference in annualised net {statistic}",
        "bootstrap": normal.detail,
        "strategy": summarize(ours.returns[inside], periods, ours.turnover[inside], ours.cost[inside]),
        "benchmark": summarize(theirs.returns[inside], periods, theirs.turnover[inside], theirs.cost[inside]),
        "strategy_double_cost": summarize(ours_doubled.returns[inside], periods),
        "average_weight_invested": float(ours.held[inside].sum(axis=1).mean()),
        "dropped_weight": ours.dropped_weight,
        "window": {"first": str(market.index[inside][0]), "last": str(market.index[inside][-1])},
    }
    for name, build in named.items():
        reference = backtest(market, build(market))
        metrics[f"reference_{name}"] = summarize(reference.returns[inside], periods)
    return Result(
        estimate=normal.estimate,
        p_value=normal.p_value,
        n=int(inside.sum()),
        metrics=metrics,
        double_cost_estimate=doubled.estimate,
        double_cost_p_value=doubled.p_value,
    )


def evaluate_predictor(
    ctx: Context,
    signal: pd.DataFrame,
    granularity: str,
    horizon: int,
    method: Literal["rank_ic", "fama_macbeth"] = "rank_ic",
    min_assets: int = 5,
    start: str | None = None,
) -> Result:
    """Does the signal at a bar's close rank (or scale with) the coins' returns over the next bars?

    Only universe members count, only signal rows inside the window, only labels whose whole
    horizon lies within the data, and only bars with at least `min_assets` scored coins. The estimate is the mean rank IC (or mean
    cross-sectional slope) with a Newey-West p-value that allows for the overlapping horizons.
    """
    market = ctx.data.market(granularity)  # type: ignore[arg-type]
    values = signal.reindex(index=market.index, columns=list(market.symbols)).to_numpy("float64")
    inside = ctx.inside(market.index, start)
    values = np.where(market.member & inside[:, None], values, np.nan)
    forward = forward_returns(market, horizon)
    tool = stats.rank_ic if method == "rank_ic" else stats.fama_macbeth
    test = tool(values, forward, overlap=horizon, alternative=ctx.alternative, min_assets=min_assets)
    return Result(
        estimate=test.estimate,
        p_value=test.p_value,
        n=test.n,
        metrics={"statistic": method, "horizon_bars": horizon, "t_statistic": test.statistic} | test.detail,
    )
