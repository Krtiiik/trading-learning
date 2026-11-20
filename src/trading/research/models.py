"""Fitting and tuning models inside train, for model hypotheses.

A model is allowed only on predictors that have reached "candidate", and is itself a
registered hypothesis ("model M beats the simple rule R built from the same predictors, by
this much, on dev"). Fit and tune with data up to the end of train: tuning is walk-forward
within train, and the fitted model then predicts dev once. Start with regularised linear
models and tree ensembles; anything with the scikit-learn fit/predict interface works here.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Protocol

import numpy as np
from scipy import stats as scipy_stats


class Model(Protocol):
    def fit(self, X: np.ndarray, y: np.ndarray) -> Any: ...

    def predict(self, X: np.ndarray) -> np.ndarray: ...


@dataclass(frozen=True)
class Stacked:
    """A panel problem flattened to rows: one row per (bar, coin) with every value present."""

    X: np.ndarray
    y: np.ndarray
    bar: np.ndarray
    """The bar number of each row; rows are ordered by it."""
    coin: np.ndarray


def stack(features: list[np.ndarray], target: np.ndarray) -> Stacked:
    """Flatten bars x coins feature panels and a target panel, dropping rows with any NaN.

    Rows whose target is missing are dropped too; to predict them later, pass a target of zeros.
    """
    cube = np.stack(features, axis=-1)
    usable = np.isfinite(cube).all(axis=-1) & np.isfinite(target)
    bar, coin = np.nonzero(usable)
    return Stacked(cube[bar, coin], target[bar, coin], bar, coin)


def walk_forward_folds(
    bar: np.ndarray, folds: int = 4, embargo: int = 0
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Expanding-window folds over time: (rows to fit on, rows to validate on) per fold.

    The bars are cut into `folds + 1` equal stretches; fold k fits on the first k and validates
    on the next. `embargo` bars before each validation stretch are left out of the fit, so a
    target whose horizon spans that many bars cannot straddle the boundary.
    """
    edges = np.quantile(np.unique(bar), np.linspace(0, 1, folds + 2)).astype(int)
    result = []
    for k in range(1, folds + 1):
        start, stop = edges[k], edges[k + 1] + (1 if k == folds else 0)
        fit = np.flatnonzero(bar < start - embargo)
        validate = np.flatnonzero((bar >= start) & (bar < stop))
        if len(fit) and len(validate):
            result.append((fit, validate))
    return result


def walk_forward_tune(
    make_model: Callable[[Any], Model],
    grid: Iterable[Any],
    data: Stacked,
    folds: int = 4,
    embargo: int = 0,
) -> tuple[Any, dict[Any, float]]:
    """Pick the setting from `grid` whose predictions rank the validation targets best.

    The score is the Spearman correlation between prediction and target, averaged over the
    walk-forward folds. Returns the best setting and every setting's score.
    """
    scores: dict[Any, float] = {}
    for setting in grid:
        correlations = []
        for fit, validate in walk_forward_folds(data.bar, folds, embargo):
            model = make_model(setting)
            model.fit(data.X[fit], data.y[fit])
            predicted = model.predict(data.X[validate])
            correlations.append(scipy_stats.spearmanr(predicted, data.y[validate]).statistic)
        scores[setting] = float(np.nanmean(correlations))
    return max(scores, key=lambda setting: scores[setting]), scores


def fit_predict(model: Model, data: Stacked, fit_until: int, shape: tuple[int, int]) -> np.ndarray:
    """Fit on rows of bars before `fit_until`, then predict every row: a bars x coins panel.

    Bars from `fit_until` on are predicted by a model that never saw them. NaN where a row had
    a missing feature.
    """
    fit = data.bar < fit_until
    model.fit(data.X[fit], data.y[fit])
    panel = np.full(shape, np.nan)
    panel[data.bar, data.coin] = model.predict(data.X)
    return panel
