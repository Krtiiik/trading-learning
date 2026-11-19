---
title: "Every statistical tool is validated on synthetic data; these are the conditions it was validated under"
kind: fact
area: statistics
source: "tests/test_stats.py (29 tests, fixed seeds), run 2026-11-18"
trust: high
date: 2026-11-18
---

Each tool in `trading.stats` gives uniform p-values under a true null (Kolmogorov-Smirnov not rejected at 1%, and a 5% test rejecting between 2% and 8.5% of the time over 300 to 400 simulations) and recovers a planted effect:

- `predictive_regression`: a predictor with autocorrelation 0.9 against 5-period overlapping returns, 800 observations.
- `mean_test`: a series with autocorrelation 0.5.
- `rank_ic` and `fama_macbeth`: 25 assets, signals with autocorrelation 0.95, overlapping 3- to 5-period returns.
- `panel_regression` (added 2026-11-19 for predictors that work in time rather than across coins): 20 assets sharing a market factor, predictors sharing a market-wide component with autocorrelation 0.9, horizons of 1, 5, 7 and 24 periods over 600 to 3,000 periods. Its errors come from 8 to 30 time blocks; a Newey-West (Driscoll-Kraay) version rejected a true null 9 to 11 times in 100 at the 5% level on the same data and was dropped, and plain pooled errors reject it more than half the time.
- `block_bootstrap_difference`: two strategies with correlation 0.6 and clustered volatility, 500 observations; its 90% interval is required to cover a planted Sharpe difference of 2.0 in 84% to 96% of simulations, and does.
- `circular_shift_test`, `asset_permutation_test`: independent series with autocorrelation 0.9; persistent per-asset traits.
- `benjamini_hochberg`: false-discovery rate 0.08 with 80% true nulls at q = 0.10. `holm`: family-wise error 5%.
- `minimum_detectable_effect`: an effect of exactly that size is found 80% of the time.

Not validated, so do not rely on it without extending the tests: horizons longer than about 5 bars against much shorter samples; predictors correlated with return innovations (the Stambaugh bias of predictive regressions with persistent predictors such as valuation ratios or funding levels); fat tails of crypto returns (simulations are Gaussian with volatility clustering in one case); panels with fewer than about 10 assets. For overlapping horizons the Newey-West lag count is twice the overlap; with fewer lags the tests over-reject.
