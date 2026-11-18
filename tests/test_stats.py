"""Validation of every statistical tool on synthetic data with a known answer.

Two properties per tool: under a true null its p-values are uniform (so a 5% test rejects
about 5% of the time), and a planted effect of known size is recovered. The synthetic data is
deliberately awkward in the ways real data is: autocorrelated predictors, overlapping forward
returns, correlated strategies.
"""

import numpy as np
import pytest
from scipy import stats as scipy_stats

from trading import stats

SIMULATIONS = 400


def ar1(rng: np.random.Generator, shape: tuple[int, ...], rho: float) -> np.ndarray:
    """Stationary AR(1) series with unit variance, along the first axis."""
    noise = rng.normal(size=shape)
    series = np.empty(shape)
    series[0] = noise[0]
    scale = np.sqrt(1 - rho**2)
    for row in range(1, shape[0]):
        series[row] = rho * series[row - 1] + scale * noise[row]
    return series


def rolling_sum(values: np.ndarray, window: int) -> np.ndarray:
    """Sum of each row and the `window - 1` rows after it: an overlapping forward return."""
    total = np.cumsum(np.concatenate([np.zeros((1, *values.shape[1:])), values]), axis=0)
    out = np.full(values.shape, np.nan)
    out[: len(values) - window + 1] = total[window:] - total[:-window]
    return out


def assert_uniform(p_values: np.ndarray, low: float = 0.02, high: float = 0.085) -> None:
    """P-values look uniform: Kolmogorov-Smirnov does not object and a 5% test rejects ~5%."""
    p_values = np.asarray(p_values)
    assert scipy_stats.kstest(p_values, "uniform").pvalue > 0.01
    assert low <= np.mean(p_values < 0.05) <= high


def simulate(count: int, one: callable) -> list:
    return [one(np.random.default_rng(1000 + index)) for index in range(count)]


# predictive_regression


def test_predictive_regression_is_uniform_under_the_null_despite_overlap_and_persistence():
    def one(rng):
        x = ar1(rng, (800,), 0.9)
        y = rolling_sum(rng.normal(size=800), 5)
        return stats.predictive_regression(y, x, overlap=5).p_value

    assert_uniform(simulate(SIMULATIONS, one))


def test_predictive_regression_recovers_a_planted_slope():
    def one(rng):
        x = ar1(rng, (800,), 0.9)
        y = 0.15 * x + rng.normal(size=800)
        return stats.predictive_regression(y, x, alternative="greater")

    results = simulate(200, one)

    assert np.mean([result.estimate for result in results]) == pytest.approx(0.15, abs=0.01)
    assert np.mean([result.p_value < 0.05 for result in results]) > 0.9


def test_predictive_regression_drops_missing_rows_and_uses_controls():
    rng = np.random.default_rng(3)
    control = rng.normal(size=500)
    x = rng.normal(size=500)
    y = 0.5 * x + 2.0 * control + 0.1 * rng.normal(size=500)
    y[:10] = np.nan

    result = stats.predictive_regression(y, x, controls=control)

    assert result.n == 490
    assert result.estimate == pytest.approx(0.5, abs=0.02)


# mean_test


def test_mean_test_is_uniform_under_the_null_for_an_autocorrelated_series():
    assert_uniform(simulate(SIMULATIONS, lambda rng: stats.mean_test(ar1(rng, (600,), 0.5)).p_value))


def test_mean_test_recovers_a_planted_mean():
    results = simulate(200, lambda rng: stats.mean_test(0.3 + ar1(rng, (600,), 0.5), alternative="greater"))

    assert np.mean([result.estimate for result in results]) == pytest.approx(0.3, abs=0.02)
    assert np.mean([result.p_value < 0.05 for result in results]) > 0.9


# rank_ic


def test_rank_ic_is_uniform_under_the_null_with_overlapping_returns():
    def one(rng):
        signal = ar1(rng, (500, 25), 0.95)
        forward = rolling_sum(rng.normal(size=(500, 25)), 5)
        return stats.rank_ic(signal, forward, overlap=5).p_value

    assert_uniform(simulate(SIMULATIONS, one))


def test_rank_ic_recovers_a_planted_correlation():
    rho = 0.10
    expected = 6 / np.pi * np.arcsin(rho / 2)  # Spearman of a bivariate normal with Pearson rho

    def one(rng):
        signal = rng.normal(size=(400, 30))
        forward = rho * signal + np.sqrt(1 - rho**2) * rng.normal(size=(400, 30))
        return stats.rank_ic(signal, forward, alternative="greater")

    results = simulate(100, one)

    assert np.mean([result.estimate for result in results]) == pytest.approx(expected, abs=0.005)
    assert np.mean([result.p_value < 0.05 for result in results]) > 0.95


def test_rank_ic_series_matches_scipy_and_skips_thin_rows():
    rng = np.random.default_rng(5)
    signal, forward = rng.normal(size=(3, 12)), rng.normal(size=(3, 12))
    signal[0, :3] = np.nan
    forward[2, :9] = np.nan

    series = stats.rank_ic_series(signal, forward, min_assets=5)

    assert series[0] == pytest.approx(scipy_stats.spearmanr(signal[0, 3:], forward[0, 3:]).statistic)
    assert series[1] == pytest.approx(scipy_stats.spearmanr(signal[1], forward[1]).statistic)
    assert np.isnan(series[2])


# fama_macbeth


def test_fama_macbeth_is_uniform_under_the_null():
    def one(rng):
        signal = ar1(rng, (500, 25), 0.95)
        forward = rolling_sum(rng.normal(size=(500, 25)), 3)
        return stats.fama_macbeth(signal, forward, overlap=3).p_value

    assert_uniform(simulate(SIMULATIONS, one))


def test_fama_macbeth_recovers_a_planted_slope():
    def one(rng):
        signal = rng.normal(size=(400, 30))
        return stats.fama_macbeth(signal, 0.05 * signal + rng.normal(size=(400, 30)), alternative="greater")

    results = simulate(100, one)

    assert np.mean([result.estimate for result in results]) == pytest.approx(0.05, abs=0.004)
    assert np.mean([result.p_value < 0.05 for result in results]) > 0.95


# block_bootstrap_difference


def correlated_returns(rng, n: int, correlation: float):
    """Two return series with volatility clustering in common, and the given correlation."""
    common = np.sqrt(correlation) * rng.normal(size=n)
    a = common + np.sqrt(1 - correlation) * rng.normal(size=n)
    b = common + np.sqrt(1 - correlation) * rng.normal(size=n)
    volatility = 0.02 * np.exp(0.5 * ar1(rng, (n,), 0.9))
    return volatility * a, volatility * b


def test_block_bootstrap_is_uniform_when_two_strategies_have_the_same_sharpe():
    def one(rng):
        a, b = correlated_returns(rng, 500, 0.6)
        return stats.block_bootstrap_difference(a, b, periods=365, draws=400, seed=1).p_value

    assert_uniform(simulate(300, one))


def test_block_bootstrap_recovers_a_planted_sharpe_difference():
    def one(rng):
        # Constant volatility here so the planted Sharpe ratio has a closed form.
        a = 0.02 * rng.normal(size=1500) + 0.02 * 2.0 / np.sqrt(365)
        b = 0.02 * rng.normal(size=1500)
        return stats.block_bootstrap_difference(a, b, periods=365, draws=400, seed=1)

    results = simulate(200, one)
    covered = [r.detail["interval_low"] <= 2.0 <= r.detail["interval_high"] for r in results]

    assert np.mean([result.estimate for result in results]) == pytest.approx(2.0, abs=0.1)
    assert 0.84 <= np.mean(covered) <= 0.96  # a 90% interval
    assert np.mean([result.p_value < 0.05 for result in results]) > 0.75


def test_block_bootstrap_mean_statistic_and_reproducibility():
    rng = np.random.default_rng(8)
    a, b = rng.normal(0.01, 0.02, 800), rng.normal(0.0, 0.02, 800)

    first = stats.block_bootstrap_difference(a, b, statistic="mean", periods=365, seed=7)
    again = stats.block_bootstrap_difference(a, b, statistic="mean", periods=365, seed=7)

    assert first.estimate == pytest.approx((a.mean() - b.mean()) * 365)
    assert first.p_value == again.p_value < 0.01


def test_circular_block_indices_are_contiguous_and_wrap():
    indices = stats.circular_block_indices(10, 4, 50, np.random.default_rng(0))

    assert indices.shape == (50, 10)
    steps = np.diff(indices[:, :4], axis=1) % 10
    assert (steps == 1).all()


# Placebo and permutation tests


def correlation_with(y: np.ndarray):
    return lambda x: float(np.corrcoef(x, y)[0, 1])


def test_circular_shift_test_is_uniform_for_independent_autocorrelated_series():
    def one(rng):
        x, y = ar1(rng, (400,), 0.9), ar1(rng, (400,), 0.9)
        return stats.circular_shift_test(correlation_with(y), x, draws=199, min_shift=20).p_value

    assert_uniform(simulate(SIMULATIONS, one))


def test_circular_shift_test_finds_a_planted_link():
    def one(rng):
        x = ar1(rng, (400,), 0.5)
        y = 0.3 * x + rng.normal(size=400)
        return stats.circular_shift_test(correlation_with(y), x, draws=199, min_shift=20).p_value

    assert np.mean(np.array(simulate(100, one)) < 0.05) > 0.9


def mean_ic_with(forward: np.ndarray):
    return lambda signal: float(np.nanmean(stats.rank_ic_series(signal, forward)))


def test_asset_permutation_test_is_uniform_for_persistent_unrelated_signals():
    def one(rng):
        signal = rng.normal(size=(1, 20)) + 0.2 * rng.normal(size=(60, 20))
        forward = rng.normal(size=(60, 20))
        return stats.asset_permutation_test(mean_ic_with(forward), signal, draws=99).p_value

    assert_uniform(simulate(300, one))


def test_asset_permutation_test_finds_a_planted_link():
    def one(rng):
        trait = rng.normal(size=(1, 20))
        signal = trait + 0.2 * rng.normal(size=(60, 20))
        forward = 0.15 * trait + rng.normal(size=(60, 20))
        return stats.asset_permutation_test(mean_ic_with(forward), signal, draws=199).p_value

    assert np.mean(np.array(simulate(100, one)) < 0.05) > 0.9


# Multiple testing


def p_values_with_effects(rng, tests: int, true_effects: int, shift: float = 3.5):
    z = rng.normal(size=tests)
    z[:true_effects] += shift
    return scipy_stats.norm.sf(z)


def test_benjamini_hochberg_keeps_the_false_discovery_rate_at_q():
    def false_discovery_proportion(rng):
        reject, _ = stats.benjamini_hochberg(p_values_with_effects(rng, 100, 20), q=0.10)
        return reject[20:].sum() / max(reject.sum(), 1), reject[:20].mean()

    outcomes = np.array(simulate(500, false_discovery_proportion))

    # With 80% true nulls the expected false-discovery rate is 0.10 * 0.8.
    assert outcomes[:, 0].mean() == pytest.approx(0.08, abs=0.015)
    assert outcomes[:, 1].mean() > 0.8


def test_benjamini_hochberg_rarely_rejects_anything_when_every_null_is_true():
    any_rejection = simulate(
        1000, lambda rng: stats.benjamini_hochberg(rng.random(40), q=0.10)[0].any()
    )

    assert np.mean(any_rejection) == pytest.approx(0.10, abs=0.03)


def test_benjamini_hochberg_matches_a_hand_computed_case():
    reject, adjusted = stats.benjamini_hochberg([0.01, 0.04, 0.03, 0.50], q=0.10)

    # Sorted: 0.01, 0.03, 0.04, 0.50 against thresholds 0.025, 0.05, 0.075, 0.10.
    assert list(reject) == [True, True, True, False]
    assert list(adjusted) == pytest.approx([0.04, 0.04 * 4 / 3, 0.04 * 4 / 3, 0.50])


def test_holm_controls_the_family_wise_error_rate_and_keeps_strong_effects():
    under_null = simulate(1000, lambda rng: stats.holm(rng.random(5), alpha=0.05)[0].any())
    with_effects = simulate(
        200, lambda rng: stats.holm(p_values_with_effects(rng, 5, 2, shift=5.0))[0][:2].all()
    )

    assert np.mean(under_null) == pytest.approx(0.05, abs=0.02)
    assert np.mean(with_effects) > 0.95


def test_holm_agrees_with_statsmodels():
    from statsmodels.stats.multitest import multipletests

    rng = np.random.default_rng(4)
    for _ in range(10):
        p_values = rng.random(6) ** 3
        reject, adjusted = stats.holm(p_values, alpha=0.05)
        expected_reject, expected_adjusted, _, _ = multipletests(p_values, alpha=0.05, method="holm")
        assert list(reject) == list(expected_reject)
        assert adjusted == pytest.approx(expected_adjusted)


def test_holm_matches_a_hand_computed_case():
    reject, adjusted = stats.holm([0.01, 0.04, 0.03], alpha=0.05)

    # 0.01 * 3 = 0.03 passes; 0.03 * 2 = 0.06 fails, and so does everything after it.
    assert list(reject) == [True, False, False]
    assert list(adjusted) == pytest.approx([0.03, 0.06, 0.06])


def test_empty_families_are_handled():
    assert stats.benjamini_hochberg([])[0].size == 0
    assert stats.holm([])[0].size == 0


# Minimum detectable effect


def test_an_effect_equal_to_the_minimum_detectable_effect_is_found_with_the_stated_power():
    rng = np.random.default_rng(0)
    n, deviation = 400, 2.0
    error = stats.mean_standard_error(deviation, n)
    effect = stats.minimum_detectable_effect(error, alpha=0.05, power=0.80)

    samples = rng.normal(effect, deviation, size=(4000, n))
    rejected = samples.mean(axis=1) / (samples.std(axis=1, ddof=1) / np.sqrt(n)) > 1.645

    assert rejected.mean() == pytest.approx(0.80, abs=0.03)


def test_two_sided_minimum_detectable_effect_is_larger():
    assert stats.minimum_detectable_effect(1.0, alternative="two-sided") > stats.minimum_detectable_effect(1.0)
    assert stats.minimum_detectable_effect(1.0) == pytest.approx(1.645 + 0.842, abs=0.001)


def test_sharpe_standard_errors_match_simulation():
    rng = np.random.default_rng(1)
    years, periods, correlation = 2, 365, 0.7
    n = years * periods
    common = np.sqrt(correlation) * rng.normal(size=(3000, n))
    a = common + np.sqrt(1 - correlation) * rng.normal(size=(3000, n))
    b = common + np.sqrt(1 - correlation) * rng.normal(size=(3000, n))
    sharpe_a = a.mean(axis=1) / a.std(axis=1, ddof=1) * np.sqrt(periods)
    sharpe_b = b.mean(axis=1) / b.std(axis=1, ddof=1) * np.sqrt(periods)

    assert sharpe_a.std() == pytest.approx(stats.sharpe_standard_error(years), rel=0.05)
    assert (sharpe_a - sharpe_b).std() == pytest.approx(
        stats.sharpe_difference_standard_error(years, correlation), rel=0.05
    )


def test_overlap_inflates_the_standard_error_of_a_mean():
    rng = np.random.default_rng(2)
    sums = np.array([np.nanmean(rolling_sum(rng.normal(size=600), 5)) for _ in range(2000)])

    assert sums.std() == pytest.approx(stats.mean_standard_error(np.sqrt(5), 596, overlap=5), rel=0.08)
