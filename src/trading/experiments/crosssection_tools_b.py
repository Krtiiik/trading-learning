"""Shared code of the cross-sectional experiments H2005 to H2008."""

import numpy as np
import pandas as pd

from trading import stats
from trading.research.evaluate import Context, Result, forward_returns


def thirds(by: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per row, which assets lie in the lowest and in the highest third of `by` (NaN: neither).

    With n usable assets in a row each third holds floor(n/3) of them: the lowest ranks and
    the highest ranks.
    """
    by = np.asarray(by, dtype="float64")
    ranks = pd.DataFrame(by).rank(axis=1).to_numpy()
    count = np.isfinite(by).sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore"):
        return ranks <= count // 3, ranks > count - count // 3


def rank_ic_difference(
    signal: np.ndarray,
    forward: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    overlap: int = 1,
    alternative: stats.Alternative = "two-sided",
    min_assets: int = 5,
) -> stats.TestResult:
    """Is the rank IC among the assets of group `first` different from that among `second`?

    The groups are boolean (periods x assets). Each period gives one rank IC per group; the
    estimate is the mean of first minus second over the periods where both exist, tested
    against zero with Newey-West errors.
    """
    signal = np.asarray(signal, dtype="float64")
    ic_first = stats.rank_ic_series(np.where(first, signal, np.nan), forward, min_assets)
    ic_second = stats.rank_ic_series(np.where(second, signal, np.nan), forward, min_assets)
    result = stats.mean_test(ic_first - ic_second, overlap, alternative)
    both = np.isfinite(ic_first) & np.isfinite(ic_second)
    detail = {"ic_first": float(ic_first[both].mean()), "ic_second": float(ic_second[both].mean())}
    return stats.TestResult(
        result.estimate, result.p_value, result.statistic, alternative, result.n, result.detail | detail
    )


def evaluate_rank_ic_by_thirds(
    ctx: Context,
    signal: pd.DataFrame,
    by: pd.DataFrame,
    granularity: str,
    horizon: int,
    start: str | None = None,
) -> Result:
    """Rank IC of `signal` among the members in the lowest third of `by`, minus the highest third.

    Members, window and forward returns are those of `evaluate_predictor`; the thirds are
    formed at each bar among the members that have both a signal and a value of `by`.
    """
    market = ctx.data.market(granularity)  # type: ignore[arg-type]
    scored = market.member & ctx.inside(market.index, start)[:, None]
    values = signal.reindex(index=market.index, columns=list(market.symbols)).to_numpy("float64")
    sorter = by.reindex(index=market.index, columns=list(market.symbols)).to_numpy("float64")
    usable = scored & np.isfinite(values) & np.isfinite(sorter)
    lowest, highest = thirds(np.where(usable, sorter, np.nan))
    test = rank_ic_difference(
        np.where(usable, values, np.nan),
        forward_returns(market, horizon),
        lowest,
        highest,
        overlap=horizon,
        alternative=ctx.alternative,
    )
    return Result(
        estimate=test.estimate,
        p_value=test.p_value,
        n=test.n,
        metrics={
            "statistic": "rank_ic lowest third minus highest third",
            "horizon_bars": horizon,
            "t_statistic": test.statistic,
            "ic_lowest_third": test.detail["ic_first"],
            "ic_highest_third": test.detail["ic_second"],
            "assets_per_third": float(lowest[usable.any(axis=1)].sum(axis=1).mean()),
        }
        | {key: value for key, value in test.detail.items() if not key.startswith("ic_")},
    )
