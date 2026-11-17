"""E07: direct policy optimisation, the simplest defensible "RL" for allocation.

A shared per-asset scoring function turns each ETF's features into a score; a softmax
over the listed ETFs plus a cash slot gives long-only weights. The policy is trained by
gradient ascent on the net-of-cost Sharpe ratio of the training window (Moody & Saffell's
direct reinforcement; Zhang, Zohren & Roberts 2020 without the LSTM).

Specification, fixed before the first run:
- policies: linear (9 features -> score) and a small MLP (9 -> 8 tanh -> 1)
- training reward: weights decided at close t earn the close(t+1) -> close(t+2) return,
  minus 5 bps times the change in weights; loss = -annualised Sharpe of that series
- Adam, lr 0.01, 300 full-batch epochs, no tuning; features standardised on the training window
- walk-forward: one fold per test year 2005..2024, expanding window from 2000, 5-session embargo
- 5 seeds per policy; report every seed and the seed-averaged weights
- evaluation in the real engine: next-open fill, 5 bps, 5% band

Run: uv run python research/e07_direct_policy.py
"""

import time

import numpy as np
import pandas as pd
import torch

from common import COST_BPS, evaluate, format_table, research_market, results_table, sub_periods
from e01_baselines import EDGES
from ml_common import folds, sealed_features
from trading.strategies.features import FEATURES

TRAIN_START = "2000-01-03"
SEEDS = range(5)
EPOCHS = 300
LEARNING_RATE = 0.01

torch.set_num_threads(4)


def make_policy(kind: str) -> torch.nn.Module:
    if kind == "linear":
        return torch.nn.Linear(len(FEATURES), 1)
    return torch.nn.Sequential(
        torch.nn.Linear(len(FEATURES), 8), torch.nn.Tanh(), torch.nn.Linear(8, 1)
    )


def weights_of(policy: torch.nn.Module, cash_score: torch.Tensor, x: torch.Tensor, mask: torch.Tensor):
    """Softmax weights over listed assets plus cash: shape (days, assets + 1), cash last."""
    scores = policy(x).squeeze(-1).masked_fill(~mask, -1e9)
    cash = cash_score.expand(len(x), 1)
    return torch.softmax(torch.cat([scores, cash], dim=1), dim=1)


def train(kind: str, seed: int, x, mask, returns) -> tuple[torch.nn.Module, torch.Tensor]:
    """Fit a policy on one training window; `returns[t]` is the close-to-close return of day t."""
    torch.manual_seed(seed)
    policy = make_policy(kind)
    cash_score = torch.zeros(1, requires_grad=True)
    optimiser = torch.optim.Adam([*policy.parameters(), cash_score], lr=LEARNING_RATE)
    earned = returns[2:]  # weights decided on day t earn day t+2's return
    for _ in range(EPOCHS):
        w = weights_of(policy, cash_score, x, mask)[:-2, :-1]
        gross = (w * earned).sum(dim=1)
        turnover = torch.cat([w[:1].abs().sum(dim=1), (w[1:] - w[:-1]).abs().sum(dim=1)])
        net = gross - COST_BPS * 1e-4 * turnover
        loss = -net.mean() / net.std() * np.sqrt(252)
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
    return policy, cash_score.detach()


def run(kind: str, seed: int, features: np.ndarray, valid: np.ndarray, returns: np.ndarray, dates):
    """Walk-forward target weights of one policy and seed over all test years."""
    start = int(dates.searchsorted(pd.Timestamp(TRAIN_START)))
    rows = []
    for train_end, test_start, test_end in folds(dates):
        lo, hi = start, int(dates.searchsorted(train_end)) + 1
        mean = np.nanmean(np.where(valid[lo:hi, :, None], features[lo:hi], np.nan), axis=(0, 1))
        std = np.nanstd(np.where(valid[lo:hi, :, None], features[lo:hi], np.nan), axis=(0, 1))
        scaled = torch.tensor(np.clip((features - mean) / std, -5, 5), dtype=torch.float32)
        mask = torch.tensor(valid)
        policy, cash_score = train(
            kind, seed, scaled[lo:hi], mask[lo:hi], torch.tensor(returns[lo:hi], dtype=torch.float32)
        )
        a, b = int(dates.searchsorted(test_start)), int(dates.searchsorted(test_end)) + 1
        with torch.no_grad():
            rows.append(weights_of(policy, cash_score, scaled[a:b], mask[a:b])[:, :-1].numpy())
    first = int(dates.searchsorted(folds(dates)[0][1]))
    return np.concatenate(rows), dates[first : first + sum(len(r) for r in rows)]


if __name__ == "__main__":
    market = research_market()
    panels, adj_close = sealed_features()
    dates, symbols = adj_close.index, adj_close.columns
    features = np.stack([panels[name].to_numpy() for name in FEATURES], axis=-1)
    valid = ~np.isnan(features).any(axis=-1)
    features = np.nan_to_num(features)
    returns = np.nan_to_num(adj_close.pct_change(fill_method=None).to_numpy())

    results, seed_rows = {}, []
    for kind in ("linear", "mlp"):
        stack_of_weights = []
        for seed in SEEDS:
            began = time.time()
            weights, index = run(kind, seed, features, valid, returns, dates)
            targets = pd.DataFrame(weights, index=index, columns=symbols)
            stack_of_weights.append(weights)
            result = evaluate(market, targets, rebalance_band=0.05)
            results[f"{kind} seed {seed}"] = result
            print(f"{kind} seed {seed} done in {time.time() - began:.0f}s", flush=True)
        ensemble = pd.DataFrame(np.mean(stack_of_weights, axis=0), index=index, columns=symbols)
        results[f"{kind} ensemble"] = evaluate(market, ensemble, rebalance_band=0.05)
        results[f"{kind} ensemble, 0 bps"] = evaluate(market, ensemble, cost_bps=0.0, rebalance_band=0.05)
        held = ensemble.mean().sort_values(ascending=False)
        print(f"{kind} ensemble average weights: " + ", ".join(f"{s} {w:.0%}" for s, w in held.head(8).items())
              + f", cash {1 - ensemble.sum(axis=1).mean():.0%}")

    print()
    print(format_table(results_table(results)))
    print()
    for name in ("linear ensemble", "mlp ensemble"):
        parts = sub_periods(results[name], EDGES)
        print(f"{name:<18}" + "  ".join(f"{k} {v:5.2f}" for k, v in parts["sharpe"].items()))
