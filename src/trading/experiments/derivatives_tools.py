"""Shared by the derivatives experiments on daily bars (H3001 to H3004).

Funding and basis as predictors of spot returns: the series as frames, the part of a signal
that the coin's own trailing return does not explain (the premium rises after a rally, so an
unadjusted premium or funding signal re-tests momentum), and a pooled test against falls.
Row t of everything here uses bars labelled t or earlier.
"""

from dataclasses import replace

import numpy as np
import pandas as pd

from trading import stats
from trading.research.evaluate import Context, Result, forward_returns
from trading.research.market import Market, ResearchData

PANEL_DEMEAN = {"panel": "none", "panel_time": "time", "panel_entity": "entity"}


def series_frame(data: ResearchData, name: str) -> pd.DataFrame:
    """A daily perpetual-futures series as a frame: bar labels by coins."""
    return data.market("1d").frame(data.series(name, "1d"))


def funding(data: ResearchData) -> pd.DataFrame:
    """Funding paid during each daily bar, summed. NaN on a day without a funding payment."""
    return series_frame(data, "funding")


def premium(data: ResearchData, cap: float = 0.01) -> pd.DataFrame:
    """The day's last hourly premium index, on days the contract paid funding, within `cap`.

    The stored premium of a contract that stopped trading stays at its last value for weeks
    (and a reused spot symbol inherits it); such a contract pays no funding, so asking for a
    funding payment on the same day removes those stale values. A live contract's premium is
    within a fraction of a percent except on a handful of days (an airdrop the perpetual does
    not receive, an exchange failing), when it reaches several percent; those are limited to
    plus or minus `cap` so that one day cannot carry a pooled slope.
    """
    return series_frame(data, "premium").where(funding(data).notna()).clip(-cap, cap)


def trailing_mean(frame: pd.DataFrame, days: int) -> pd.DataFrame:
    """Mean of the last `days` daily values, the bar's own included; NaN unless all are there."""
    return frame.rolling(days, min_periods=days).mean()


def trailing_sum(frame: pd.DataFrame, days: int) -> pd.DataFrame:
    """Sum of the last `days` daily values, the bar's own included; NaN unless all are there."""
    return frame.rolling(days, min_periods=days).sum()


def trailing_log_return(market: Market, days: int) -> pd.DataFrame:
    """Log return of the close over the last `days` bars; NaN without both closes."""
    close = market.frame("close")
    return np.log(close / close.shift(days))


def beyond_past_return(
    signal: pd.DataFrame, control: pd.DataFrame, market: Market, min_observations: int = 500
) -> pd.DataFrame:
    """The signal minus what the control explains, in the signal's own units.

    At each bar one line (intercept and slope) is fitted to every member coin-day with both
    values at that bar or earlier, pooled over coins, and the residual of the bar's own
    values is returned. The fit never sees a later bar. The level shared by all coins stays
    in the residual, so this suits a question about a coin's own signal over time. NaN until
    `min_observations` coin-days have been seen.
    """
    x, y = control.to_numpy("float64"), signal.to_numpy("float64")
    usable = np.isfinite(x) & np.isfinite(y) & market.member
    xs, ys = np.where(usable, x, 0.0), np.where(usable, y, 0.0)

    def so_far(values: np.ndarray) -> np.ndarray:
        return np.cumsum(values.sum(axis=1))[:, None]

    count, sum_x, sum_y = so_far(usable.astype("float64")), so_far(xs), so_far(ys)
    safe = np.maximum(count, 1.0)
    spread = so_far(xs * xs) - sum_x**2 / safe
    with np.errstate(invalid="ignore", divide="ignore"):
        slope = (so_far(xs * ys) - sum_x * sum_y / safe) / spread
        intercept = (sum_y - slope * sum_x) / safe
        residual = y - intercept - slope * x
    residual[np.broadcast_to((count < min_observations) | (spread <= 0), residual.shape)] = np.nan
    return pd.DataFrame(residual, index=signal.index, columns=signal.columns)


def beyond_past_return_rank(signal: pd.DataFrame, control: pd.DataFrame, market: Market) -> pd.DataFrame:
    """Each bar's cross-sectional rank of the signal minus what the rank of the control explains.

    Among the universe members with both values at a bar (the cells a predictive test scores),
    both are ranked and centred; the residual is the signal's rank minus the control's rank
    times their rank correlation on that bar. A purely cross-sectional adjustment: the level
    shared by all coins is gone. NaN for a coin without both values and on a bar with fewer
    than three such coins.
    """
    eligible = signal.notna() & control.notna() & market.frame(market.member)

    def centred_rank(frame: pd.DataFrame) -> pd.DataFrame:
        ranks = frame.where(eligible).rank(axis=1)
        return ranks.sub(ranks.mean(axis=1), axis=0)

    ours, theirs = centred_rank(signal), centred_rank(control)
    spread = (theirs**2).sum(axis=1)
    correlation = ((ours * theirs).sum(axis=1) / spread.where(spread > 0)).fillna(0.0)
    residual = ours - theirs.mul(correlation, axis=0)
    return residual.where(eligible.sum(axis=1) >= 3)


def evaluate_fall_predictor(
    ctx: Context,
    signal: pd.DataFrame,
    horizon: int,
    fall: float,
    method: str = "panel_entity",
    start: str | None = None,
) -> Result:
    """Is a fall of `fall` or more over the next `horizon` daily bars likelier when the signal is higher?

    The same cells as `evaluate_predictor` (universe members, signal rows inside the window,
    forward return from the next bar's open), with the forward return replaced by 1 where it
    is at or below `-fall` and 0 elsewhere. The estimate is the pooled slope of that indicator
    on the signal (change in the probability of a fall per unit of signal), tested with
    `stats.panel_regression`, whose errors come from time blocks.
    """
    market = ctx.data.market("1d")
    values = signal.reindex(index=market.index, columns=list(market.symbols)).to_numpy("float64")
    values = np.where(market.member & ctx.inside(market.index, start)[:, None], values, np.nan)
    forward = forward_returns(market, horizon)
    fell = np.where(np.isfinite(forward), (forward <= -fall).astype("float64"), np.nan)
    test = stats.panel_regression(
        fell, values, overlap=horizon, alternative=ctx.alternative, demean=PANEL_DEMEAN[method]  # type: ignore[arg-type]
    )
    scored = np.isfinite(values) & np.isfinite(fell)
    metrics = {
        "statistic": f"{method} slope of a fall indicator",
        "horizon_bars": horizon,
        "fall": fall,
        "t_statistic": test.statistic,
        "share_of_cells_with_a_fall": float(fell[scored].mean()),
        "signal_standard_deviation": float(values[scored].std()),
        "bars_with_a_scored_coin": int(scored.any(axis=1).sum()),
    } | test.detail
    return Result(estimate=test.estimate, p_value=test.p_value, n=test.n, metrics=metrics)


def with_reference(result: Result, name: str, other: Result) -> Result:
    """The primary result with another test's estimate and p-value added to its metrics.

    For a version of the signal that decides nothing but that a reader will ask about (the
    signal before the past return was taken out).
    """
    reference = {"estimate": other.estimate, "p_value": other.p_value, "n": other.n}
    return replace(result, metrics=result.metrics | {f"reference_{name}": reference})
