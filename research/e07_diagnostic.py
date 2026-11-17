"""E07 diagnostic: in-sample versus out-of-sample reward of the direct policy, one fold.

Trains on 2000 .. 2019 and scores 2020 .. seal in the training convention (weights at
close t earn close t+1 -> t+2, 5 bps on weight changes). Explains the E07 failure; it
does not change the specification.

Run: uv run python research/e07_diagnostic.py
"""

import numpy as np
import pandas as pd
import torch

from common import COST_BPS
from e07_direct_policy import TRAIN_START, train, weights_of
from ml_common import sealed_features
from trading.strategies.features import FEATURES

panels, adj_close = sealed_features()
dates = adj_close.index
features = np.stack([panels[name].to_numpy() for name in FEATURES], axis=-1)
valid = ~np.isnan(features).any(axis=-1)
features = np.nan_to_num(features)
returns = np.nan_to_num(adj_close.pct_change(fill_method=None).to_numpy())

lo = int(dates.searchsorted(pd.Timestamp(TRAIN_START)))
split = int(dates.searchsorted(pd.Timestamp("2020-01-01")))
masked = np.where(valid[lo:split, :, None], features[lo:split], np.nan)
mean, std = np.nanmean(masked, axis=(0, 1)), np.nanstd(masked, axis=(0, 1))
x = torch.tensor(np.clip((features - mean) / std, -5, 5), dtype=torch.float32)
mask = torch.tensor(valid)
r = torch.tensor(returns, dtype=torch.float32)


def score(policy, cash, a, b):
    with torch.no_grad():
        w = weights_of(policy, cash, x[a:b], mask[a:b])[:-2, :-1]
        gross = (w * r[a:b][2:]).sum(dim=1)
        turnover = (w[1:] - w[:-1]).abs().sum(dim=1)
        net = gross[1:] - COST_BPS * 1e-4 * turnover
        sharpe = lambda s: float(s.mean() / s.std() * np.sqrt(252))
        return sharpe(gross), sharpe(net), float(turnover.mean() * 252 / 2), float(w.max(dim=1).values.mean()), float(1 - w.sum(dim=1).mean())


for kind in ("linear", "mlp"):
    for seed in (0, 1):
        policy, cash = train(kind, seed, x[lo:split], mask[lo:split], r[lo:split])
        for label, a, b in (("train 2000-2019", lo, split), ("test  2020-2024", split, len(dates))):
            gross, net, turnover, top, idle = score(policy, cash, a, b)
            print(f"{kind} seed {seed} {label}: gross Sharpe {gross:5.2f}  net {net:5.2f}  "
                  f"turnover {turnover:5.1f}x  largest weight {top:.0%}  cash {idle:.0%}")
