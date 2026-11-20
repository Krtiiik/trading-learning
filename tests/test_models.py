import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge

from trading.research.models import fit_predict, stack, walk_forward_folds, walk_forward_tune


def planted(seed: int = 0, bars: int = 300, coins: int = 12):
    """Two feature panels; the target is 0.2 times the first plus noise. Some cells are missing."""
    rng = np.random.default_rng(seed)
    useful, useless = rng.normal(size=(bars, coins)), rng.normal(size=(bars, coins))
    target = 0.2 * useful + rng.normal(size=(bars, coins))
    useful[:5, 0] = np.nan
    target[-3:] = np.nan
    return useful, useless, target


def test_stack_keeps_only_complete_rows_in_time_order():
    useful, useless, target = planted()

    data = stack([useful, useless], target)

    assert data.X.shape == (300 * 12 - 5 - 3 * 12, 2)
    assert (np.diff(data.bar) >= 0).all()
    assert data.y[0] == target[data.bar[0], data.coin[0]]


def test_every_fold_validates_after_what_it_was_fitted_on_with_an_embargo():
    bar = np.repeat(np.arange(100), 3)

    folds = walk_forward_folds(bar, folds=4, embargo=5)

    assert len(folds) == 4
    for fit, validate in folds:
        assert bar[fit].max() < bar[validate].min() - 5
    assert bar[folds[-1][1]].max() == 99
    assert len(folds[0][0]) < len(folds[-1][0])  # the window expands


def test_tuning_prefers_the_setting_that_predicts_better_out_of_sample():
    useful, useless, target = planted()
    data = stack([useful, useless], target)

    best, scores = walk_forward_tune(lambda alpha: Ridge(alpha=alpha), [1.0, 1e9], data, folds=4)
    features = {"useful": stack([useful], target), "useless": stack([useless], target)}
    by_feature = {
        name: walk_forward_tune(lambda alpha: Ridge(alpha=alpha), [1.0], only)[1][1.0]
        for name, only in features.items()
    }

    assert set(scores) == {1.0, 1e9}
    assert scores[best] == max(scores.values()) > 0.1
    assert by_feature["useful"] > 0.1 > abs(by_feature["useless"])


def test_predictions_after_the_fit_boundary_ignore_later_targets():
    useful, useless, target = planted()
    changed = target.copy()
    changed[200:] = 99.0  # everything from bar 200 on is altered

    first = fit_predict(Ridge(alpha=1.0), stack([useful, useless], target), 200, target.shape)
    second = fit_predict(Ridge(alpha=1.0), stack([useful, useless], changed), 200, target.shape)

    assert np.allclose(first[:297], second[:297], equal_nan=True)
    assert np.isnan(first[:5, 0]).all() and np.isfinite(first[250, 1])
    assert np.corrcoef(first[200:297].ravel(), useful[200:297].ravel())[0, 1] > 0.9


def test_tree_ensembles_fit_the_same_interface():
    useful, useless, target = planted()
    data = stack([useful, useless], target)

    panel = fit_predict(HistGradientBoostingRegressor(max_depth=2, max_iter=30), data, 200, target.shape)

    assert np.corrcoef(panel[200:297].ravel(), useful[200:297].ravel())[0, 1] > 0.5
