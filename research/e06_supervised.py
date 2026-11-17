"""E06: walk-forward supervised return prediction (ridge and gradient boosting).

Specification, fixed before the first run:
- samples: every (date, symbol) with all nine features; label: 5-day forward return in
  volatility units, clipped to +-3
- folds: one per test year 2005..2024, expanding training window, 5-session embargo
- models: Ridge(alpha=100) on standardised features; HistGradientBoosting (depth 3,
  rate 0.05, 200 trees, min leaf 200); no tuning
- portfolio: each day the 5 symbols with the highest prediction, 20% each, only if the
  prediction is positive (else that slot is cash); target = average of the last 5 days'
  picks (overlapping 5-day holds); 5% no-trade band

Run: uv run python research/e06_supervised.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import evaluate, format_table, research_market, results_table, sub_periods
from e01_baselines import EDGES
from ml_common import HORIZON, folds, sealed_features, training_table
from trading.strategies.features import FEATURES, stack

MODELS = {
    "Ridge": lambda: make_pipeline(StandardScaler(), Ridge(alpha=100.0)),
    "GBM": lambda: HistGradientBoostingRegressor(
        max_depth=3, learning_rate=0.05, max_iter=200, min_samples_leaf=200, random_state=0
    ),
}
TOP = 5


def walk_forward_predictions(make_model, table: pd.DataFrame, live: pd.DataFrame, dates) -> pd.Series:
    """Out-of-sample predictions for every (date, symbol) in the test years."""
    features = list(FEATURES)
    table_dates = table.index.get_level_values("date")
    live_dates = live.index.get_level_values("date")
    parts = []
    for train_end, test_start, test_end in folds(dates):
        train = table[table_dates <= train_end]
        test = live[(live_dates >= test_start) & (live_dates <= test_end)]
        model = make_model().fit(train[features].to_numpy(), train["label"].to_numpy())
        parts.append(pd.Series(model.predict(test[features].to_numpy()), index=test.index))
    return pd.concat(parts)


def top_k_targets(predictions: pd.Series, columns: pd.Index) -> pd.DataFrame:
    scores = predictions.unstack("symbol").reindex(columns=columns)
    rank = scores.rank(axis=1, ascending=False, method="first")
    picks = ((rank <= TOP) & (scores > 0)).astype(float) / TOP
    return picks.rolling(HORIZON, min_periods=1).mean()


if __name__ == "__main__":
    market = research_market()
    panels, adj_close = sealed_features()
    table = training_table(panels, adj_close)
    live = stack(panels)  # features without the label, so the last 5 days are scored too
    print(f"samples {len(table):,}  from {table.index[0][0].date()}")

    results, information, by_cost = {}, {}, {}
    for name, make_model in MODELS.items():
        predictions = walk_forward_predictions(make_model, table, live, market.dates)
        targets = top_k_targets(predictions, market.close.columns)
        results[f"{name} top-5"] = evaluate(market, targets, rebalance_band=0.05)
        for cost in (0.0, 2.0):
            by_cost[f"{name} top-5 at {cost:g} bps"] = evaluate(
                market, targets, cost_bps=cost, rebalance_band=0.05
            )
        joined = pd.concat([predictions.rename("pred"), table["label"]], axis=1).dropna()
        daily_ic = joined.groupby(level="date").apply(lambda g: g["pred"].corr(g["label"], method="spearman"))
        information[name] = daily_ic
        print(f"{name}: mean daily rank IC {daily_ic.mean():+.4f}  "
              f"t-stat {daily_ic.mean() / daily_ic.std() * np.sqrt(len(daily_ic) / HORIZON):+.2f}")

    print()
    print(format_table(results_table(results)))
    print()
    for name, result in results.items():
        parts = sub_periods(result, EDGES)
        print(f"{name:<14}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))
    print("\ncost sensitivity (diagnostic)\n")
    print(format_table(results_table(by_cost)))
    print("\nmean rank IC by 5-year block")
    for name, ic in information.items():
        blocks = ic.groupby((ic.index.year - 2005) // 5).mean()
        print(f"{name:<8}" + "  ".join(f"{2005 + 5 * k}-{2009 + 5 * k} {v:+.4f}" for k, v in blocks.items()))

    ridge = MODELS["Ridge"]().fit(table[list(FEATURES)].to_numpy(), table["label"].to_numpy())
    print("\nridge coefficients on standardised features, fitted on all pre-holdout data (diagnostic)")
    for feature, coefficient in zip(FEATURES, ridge[-1].coef_, strict=True):
        print(f"  {feature:<10}{coefficient:+.4f}")
