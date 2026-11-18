"""Statistical tools for testing hypotheses.

Each tool is validated in `tests/test_stats.py` on synthetic data with a known answer: under a
true null its p-values are uniform, and a planted effect of known size is recovered. A tool
that fails that validation must not be used. Established libraries do the estimation
(statsmodels, scipy, arch); this module fixes the conventions around them.

Every test takes an `alternative`: "greater" and "less" are one-sided in the direction a
hypothesis predicted, "two-sided" is for descriptive questions.
"""

import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import statsmodels.api as sm
from arch.bootstrap import optimal_block_length
from scipy import stats as scipy_stats
from statsmodels.stats.multitest import multipletests

Alternative = Literal["greater", "less", "two-sided"]


@dataclass(frozen=True)
class TestResult:
    estimate: float
    """The effect, in the unit the tool documents."""
    p_value: float
    statistic: float
    """The t-like statistic behind the p-value, where one exists."""
    alternative: Alternative
    n: int
    """Observations the estimate rests on."""
    detail: dict[str, float] = field(default_factory=dict)

    __test__ = False  # not a pytest class, despite the name


# Regressions and means with autocorrelation-robust errors


def newey_west_lags(n: int, overlap: int = 1) -> int:
    """Lags for the Newey-West estimator: the usual rule of thumb, widened for overlap.

    `overlap` is how many periods each observation spans (an h-period forward return observed
    every period has overlap h). Overlap induces h - 1 lags of autocorrelation by construction,
    and the Bartlett kernel down-weights them, so twice that many lags are used.
    """
    rule = int(np.floor(4 * (n / 100) ** (2 / 9)))
    return max(rule, 2 * (overlap - 1))


def predictive_regression(
    y: np.ndarray,
    x: np.ndarray,
    overlap: int = 1,
    alternative: Alternative = "two-sided",
    controls: np.ndarray | None = None,
) -> TestResult:
    """OLS of `y` on `x` (plus a constant and optional controls) with Newey-West errors.

    The caller aligns the series so that `x[t]` was knowable before the period `y[t]` covers.
    The estimate is the slope on `x`. Rows with a missing value are dropped.
    """
    y = np.asarray(y, dtype="float64")
    columns = [np.asarray(x, dtype="float64")]
    if controls is not None:
        columns += list(np.asarray(controls, dtype="float64").reshape(len(y), -1).T)
    design = np.column_stack(columns)
    keep = np.isfinite(y) & np.isfinite(design).all(axis=1)
    y, design = y[keep], design[keep]
    lags = newey_west_lags(len(y), overlap)
    fit = sm.OLS(y, sm.add_constant(design, has_constant="add")).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags, "use_correction": True}
    )
    slope, error = float(fit.params[1]), float(fit.bse[1])
    statistic = slope / error
    return TestResult(
        estimate=slope,
        p_value=_p_from_t(statistic, len(y) - design.shape[1] - 1, alternative),
        statistic=statistic,
        alternative=alternative,
        n=len(y),
        detail={"standard_error": error, "lags": lags, "r_squared": float(fit.rsquared)},
    )


def mean_test(
    values: np.ndarray, overlap: int = 1, alternative: Alternative = "two-sided"
) -> TestResult:
    """Is the mean of an autocorrelated series different from zero? (Newey-West t-test.)"""
    values = np.asarray(values, dtype="float64")
    values = values[np.isfinite(values)]
    lags = newey_west_lags(len(values), overlap)
    fit = sm.OLS(values, np.ones(len(values))).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags, "use_correction": True}
    )
    mean, error = float(fit.params[0]), float(fit.bse[0])
    statistic = mean / error
    return TestResult(
        estimate=mean,
        p_value=_p_from_t(statistic, len(values) - 1, alternative),
        statistic=statistic,
        alternative=alternative,
        n=len(values),
        detail={"standard_error": error, "lags": lags},
    )


def rank_ic_series(signal: np.ndarray, forward: np.ndarray, min_assets: int = 5) -> np.ndarray:
    """Spearman correlation across assets between `signal` and `forward`, one value per row.

    Both are (periods x assets). A row with fewer than `min_assets` usable pairs gives NaN.
    """
    signal = np.asarray(signal, dtype="float64")
    forward = np.asarray(forward, dtype="float64")
    usable = np.isfinite(signal) & np.isfinite(forward)
    ranks_signal = _row_ranks(np.where(usable, signal, np.nan))
    ranks_forward = _row_ranks(np.where(usable, forward, np.nan))
    with np.errstate(invalid="ignore", divide="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # rows with no usable pair give NaN
        centred_signal = ranks_signal - np.nanmean(ranks_signal, axis=1, keepdims=True)
        centred_forward = ranks_forward - np.nanmean(ranks_forward, axis=1, keepdims=True)
        covariance = np.nansum(centred_signal * centred_forward, axis=1)
        scale = np.sqrt(np.nansum(centred_signal**2, axis=1) * np.nansum(centred_forward**2, axis=1))
        ic = covariance / scale
    ic[usable.sum(axis=1) < min_assets] = np.nan
    return ic


def rank_ic(
    signal: np.ndarray,
    forward: np.ndarray,
    overlap: int = 1,
    alternative: Alternative = "two-sided",
    min_assets: int = 5,
) -> TestResult:
    """Mean rank information coefficient, tested against zero with Newey-West errors.

    `forward` is the return over the periods after each signal row; `overlap` is its horizon
    in rows, which sets how autocorrelated the IC series is by construction.
    """
    series = rank_ic_series(signal, forward, min_assets)
    result = mean_test(series, overlap, alternative)
    spread = float(np.nanstd(series, ddof=1))
    return TestResult(
        result.estimate,
        result.p_value,
        result.statistic,
        alternative,
        result.n,
        result.detail | {"ic_std": spread},
    )


def fama_macbeth(
    signal: np.ndarray,
    forward: np.ndarray,
    overlap: int = 1,
    alternative: Alternative = "two-sided",
    min_assets: int = 5,
) -> TestResult:
    """Average cross-sectional slope of `forward` on `signal`, with Newey-West errors.

    One regression across assets per row; the estimate is the mean slope over rows.
    """
    signal = np.asarray(signal, dtype="float64")
    forward = np.asarray(forward, dtype="float64")
    usable = np.isfinite(signal) & np.isfinite(forward)
    count = usable.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # rows with no usable pair give NaN
        x = np.where(usable, signal, np.nan)
        y = np.where(usable, forward, np.nan)
        x_centred = x - np.nanmean(x, axis=1, keepdims=True)
        y_centred = y - np.nanmean(y, axis=1, keepdims=True)
        slopes = np.nansum(x_centred * y_centred, axis=1) / np.nansum(x_centred**2, axis=1)
    slopes[count < min_assets] = np.nan
    return mean_test(slopes, overlap, alternative)


# Bootstrap


def circular_block_indices(
    n: int, block: int, draws: int, rng: np.random.Generator
) -> np.ndarray:
    """Row indices of `draws` circular block bootstrap samples of a series of length `n`."""
    blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(draws, blocks))
    indices = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    return indices.reshape(draws, blocks * block)[:, :n]


def default_block_length(series: np.ndarray) -> int:
    """Politis-White automatic block length for the circular bootstrap, kept within sane bounds."""
    series = np.asarray(series, dtype="float64")
    suggested = float(optimal_block_length(series)["circular"].iloc[0])
    if not np.isfinite(suggested):
        suggested = len(series) ** (1 / 3)
    return int(np.clip(np.ceil(suggested), 2, max(2, len(series) // 10)))


def block_bootstrap_difference(
    a: np.ndarray,
    b: np.ndarray,
    statistic: Literal["sharpe", "mean"] = "sharpe",
    periods: float = 1.0,
    block: int | None = None,
    draws: int = 2000,
    seed: int = 0,
    alternative: Alternative = "greater",
) -> TestResult:
    """Paired circular block bootstrap of statistic(a) - statistic(b) for two return series.

    Both series are resampled with the same blocks, which keeps their correlation and their
    autocorrelation. The p-value is for the null of no difference: the bootstrap distribution
    is centred on the observed difference before the observed value is compared with it.
    `periods` annualises: the Sharpe ratio by its square root, the mean by itself.
    """
    a = np.asarray(a, dtype="float64")
    b = np.asarray(b, dtype="float64")
    if a.shape != b.shape or a.ndim != 1:
        raise ValueError("a and b must be 1-D series of the same length")
    n = len(a)
    block = block or default_block_length(a - b)
    compute = _sharpe_rows if statistic == "sharpe" else _mean_rows
    observed = float(compute(a[None, :], periods)[0] - compute(b[None, :], periods)[0])

    rng = np.random.default_rng(seed)
    differences = np.empty(draws)
    chunk = max(1, min(draws, 8_000_000 // n))
    for start in range(0, draws, chunk):
        indices = circular_block_indices(n, block, min(chunk, draws - start), rng)
        differences[start : start + len(indices)] = compute(a[indices], periods) - compute(
            b[indices], periods
        )
    centred = differences - observed
    p_value = _p_from_null_draws(observed, centred, alternative)
    low, high = np.quantile(differences, [0.05, 0.95])
    error = float(differences.std(ddof=1))
    return TestResult(
        estimate=observed,
        p_value=p_value,
        statistic=observed / error if error > 0 else 0.0,
        alternative=alternative,
        n=n,
        detail={
            "standard_error": error,
            "interval_low": float(low),
            "interval_high": float(high),
            "block": float(block),
            "draws": float(draws),
        },
    )


# Placebo and permutation tests


def circular_shift_test(
    statistic: Callable[[np.ndarray], float],
    x: np.ndarray,
    draws: int = 1000,
    min_shift: int = 1,
    seed: int = 0,
    alternative: Alternative = "greater",
) -> TestResult:
    """Placebo test in time: is `statistic(x)` unusual among statistics of time-shifted `x`?

    `x` (a series, or periods x assets) is rolled along time by random offsets of at least
    `min_shift` rows and the statistic recomputed. Rolling keeps the autocorrelation of `x`
    and of whatever the statistic compares it with, and breaks only their alignment in time.
    """
    x = np.asarray(x)
    n = len(x)
    if n < 2 * min_shift + 1:
        raise ValueError("series too short for the requested minimum shift")
    rng = np.random.default_rng(seed)
    observed = float(statistic(x))
    shifts = rng.integers(min_shift, n - min_shift + 1, size=draws)
    placebo = np.array([statistic(np.roll(x, int(shift), axis=0)) for shift in shifts])
    return _permutation_result(observed, placebo, alternative, n)


def asset_permutation_test(
    statistic: Callable[[np.ndarray], float],
    signal: np.ndarray,
    draws: int = 1000,
    seed: int = 0,
    alternative: Alternative = "greater",
) -> TestResult:
    """Placebo test across assets: reassign each asset's whole signal history to another asset.

    One permutation of the columns per draw, the same for every row, so each signal keeps its
    behaviour over time and loses only its link to the asset it described.
    """
    signal = np.asarray(signal)
    rng = np.random.default_rng(seed)
    observed = float(statistic(signal))
    placebo = np.array(
        [statistic(signal[:, rng.permutation(signal.shape[1])]) for _ in range(draws)]
    )
    return _permutation_result(observed, placebo, alternative, signal.shape[0])


# Multiple testing


def benjamini_hochberg(p_values: list[float] | np.ndarray, q: float = 0.10) -> tuple[np.ndarray, np.ndarray]:
    """Which tests pass false-discovery control at rate `q`, and their adjusted p-values."""
    p_values = np.asarray(p_values, dtype="float64")
    if p_values.size == 0:
        return np.zeros(0, dtype=bool), np.zeros(0)
    reject, adjusted, _, _ = multipletests(p_values, alpha=q, method="fdr_bh")
    return reject, adjusted


def holm(p_values: list[float] | np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """Which tests pass Holm's family-wise correction at level `alpha`, and adjusted p-values.

    Computed directly (statsmodels' version takes tens of milliseconds per call) and checked
    against statsmodels in the tests.
    """
    p_values = np.asarray(p_values, dtype="float64")
    if p_values.size == 0:
        return np.zeros(0, dtype=bool), np.zeros(0)
    order = np.argsort(p_values)
    scaled = p_values[order] * (len(p_values) - np.arange(len(p_values)))
    adjusted = np.empty(len(p_values))
    adjusted[order] = np.minimum(np.maximum.accumulate(scaled), 1.0)
    return adjusted <= alpha, adjusted


# Power: can a hypothesis be tested at all?


def minimum_detectable_effect(
    standard_error: float,
    alpha: float = 0.05,
    power: float = 0.80,
    alternative: Alternative = "greater",
) -> float:
    """The smallest true effect a test with this standard error finds with the given power.

    Compare it with the effect a hypothesis predicts before running anything: a prediction far
    below it cannot be confirmed or rejected by this data.
    """
    tail = alpha / 2 if alternative == "two-sided" else alpha
    return float((scipy_stats.norm.ppf(1 - tail) + scipy_stats.norm.ppf(power)) * standard_error)


def sharpe_standard_error(years: float, sharpe: float = 0.0, periods: float = 365.0) -> float:
    """Standard error of an annualised Sharpe ratio measured over `years` (Lo, 2002, iid case)."""
    per_period = sharpe / np.sqrt(periods)
    return float(np.sqrt((1 + 0.5 * per_period**2) / years))


def sharpe_difference_standard_error(years: float, correlation: float) -> float:
    """Standard error of the difference of two annualised Sharpe ratios with correlated returns."""
    return float(np.sqrt(2 * (1 - correlation) / years))


def mean_standard_error(deviation: float, n: int, overlap: int = 1) -> float:
    """Standard error of a mean of `n` observations that each span `overlap` periods."""
    return float(deviation * np.sqrt(overlap / n))


# Helpers


def _p_from_t(statistic: float, dof: int, alternative: Alternative) -> float:
    distribution = scipy_stats.t(max(dof, 1))
    if alternative == "greater":
        return float(distribution.sf(statistic))
    if alternative == "less":
        return float(distribution.cdf(statistic))
    return float(2 * distribution.sf(abs(statistic)))


def _p_from_null_draws(observed: float, null_draws: np.ndarray, alternative: Alternative) -> float:
    """Share of null draws at least as extreme as the observed value (never exactly zero)."""
    if alternative == "greater":
        extreme = np.sum(null_draws >= observed)
    elif alternative == "less":
        extreme = np.sum(null_draws <= observed)
    else:
        extreme = np.sum(np.abs(null_draws) >= abs(observed))
    return float((1 + extreme) / (1 + len(null_draws)))


def _permutation_result(
    observed: float, placebo: np.ndarray, alternative: Alternative, n: int
) -> TestResult:
    centre, spread = float(np.mean(placebo)), float(np.std(placebo, ddof=1))
    null_draws = placebo - centre if alternative == "two-sided" else placebo
    reference = observed - centre if alternative == "two-sided" else observed
    return TestResult(
        estimate=observed,
        p_value=_p_from_null_draws(reference, null_draws, alternative),
        statistic=(observed - centre) / spread if spread > 0 else 0.0,
        alternative=alternative,
        n=n,
        detail={"placebo_mean": centre, "placebo_std": spread, "draws": float(len(placebo))},
    )


def _row_ranks(values: np.ndarray) -> np.ndarray:
    return scipy_stats.rankdata(values, axis=1, nan_policy="omit")


def _sharpe_rows(samples: np.ndarray, periods: float) -> np.ndarray:
    deviation = samples.std(axis=1, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(deviation > 0, samples.mean(axis=1) / deviation * np.sqrt(periods), 0.0)


def _mean_rows(samples: np.ndarray, periods: float) -> np.ndarray:
    return samples.mean(axis=1) * periods
