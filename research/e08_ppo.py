"""E08: a PPO allocation agent (stable-baselines3), as the canonical RL candidate.

Specification, fixed before the first run:
- assets: SPY, IEF, GLD plus cash (one representative each for stocks, bonds, gold; all
  three have features from late 2005, which leaves room to train before testing)
- observation: the nine features of each asset, standardised on the training window and
  clipped to +-5, plus the weights currently held (31 numbers)
- action: 4 numbers in [-1, 1]; weights = softmax(3 * action), cash last
- reward: 100 * log(1 + net return), where weights decided at close t earn the
  close(t+1) -> close(t+2) return minus 5 bps times the change in weights
- episodes: 252 consecutive days from a random start inside the training window
- PPO with library defaults, MLP policy 2x32, 150,000 steps, deterministic at test time
- walk-forward: test blocks 2012-14, 2015-17, 2018-20, 2021-24; expanding training
  window from the first date with features; 5-session embargo
- 5 seeds, every seed reported, plus the seed-averaged weights
- evaluation in the real engine: next-open fill, 5 bps, 5% band, on 2012 .. seal

Run: uv run python research/e08_ppo.py <seed>      (trains one seed, saves its weights)
     uv run python research/e08_ppo.py report      (evaluates all saved seeds)
"""

import sys
import time
from pathlib import Path

import gymnasium as gym
import numpy as np
import pandas as pd

from common import COST_BPS, evaluate, format_table, research_market, research_prices, results_table
from ml_common import HORIZON, sealed_features
from trading.strategies import rules
from trading.strategies.features import FEATURES

ASSETS = ["SPY", "IEF", "GLD"]
BLOCKS = [("2012-01-01", "2014-12-31"), ("2015-01-01", "2017-12-31"),
          ("2018-01-01", "2020-12-31"), ("2021-01-01", "2024-11-16")]
TEST_START = "2012-01-03"
EPISODE = 252
STEPS = 150_000
SEEDS = range(5)
OUT = Path(__file__).parent / "out"


def softmax(z: np.ndarray) -> np.ndarray:
    e = np.exp(z - z.max())
    return e / e.sum()


class AllocationEnv(gym.Env):
    """One step per day: observe features at the close, choose weights for the next day."""

    def __init__(self, features: np.ndarray, returns: np.ndarray, seed: int) -> None:
        self.features = features.astype(np.float32)  # (days, assets * features)
        self.returns = returns  # (days, assets), close-to-close
        self.n_assets = returns.shape[1]
        self.rng = np.random.default_rng(seed)
        size = self.features.shape[1] + self.n_assets + 1
        self.observation_space = gym.spaces.Box(-5.0, 5.0, (size,), np.float32)
        self.action_space = gym.spaces.Box(-1.0, 1.0, (self.n_assets + 1,), np.float32)

    def _observation(self) -> np.ndarray:
        return np.concatenate([self.features[self.t], self.weights]).astype(np.float32)

    def reset(self, *, seed=None, options=None):
        last_start = len(self.features) - EPISODE - 2
        self.t = int(self.rng.integers(0, max(last_start, 1)))
        self.end = min(self.t + EPISODE, len(self.features) - 2)
        self.weights = np.zeros(self.n_assets + 1, dtype=np.float32)
        self.weights[-1] = 1.0
        return self._observation(), {}

    def step(self, action):
        target = softmax(3.0 * np.asarray(action, dtype=np.float64))
        turnover = np.abs(target[:-1] - self.weights[:-1]).sum()
        gross = float(target[:-1] @ self.returns[self.t + 2])
        net = gross - COST_BPS * 1e-4 * turnover
        self.weights = target.astype(np.float32)
        self.t += 1
        return self._observation(), 100.0 * float(np.log1p(net)), False, self.t >= self.end, {}


def prepare():
    panels, adj_close = sealed_features()
    dates = adj_close.index
    features = np.concatenate([panels[name][ASSETS].to_numpy() for name in FEATURES], axis=1)
    returns = adj_close[ASSETS].pct_change(fill_method=None).to_numpy()
    first = int(np.argmax(~np.isnan(features).any(axis=1)))
    return dates[first:], features[first:], np.nan_to_num(returns[first:])


def train_seed(seed: int) -> pd.DataFrame:
    """Walk-forward target weights of one PPO seed over all test blocks."""
    import torch
    from stable_baselines3 import PPO

    torch.set_num_threads(1)
    dates, features, returns = prepare()
    rows = []
    for start, end in BLOCKS:
        a = int(dates.searchsorted(pd.Timestamp(start)))
        b = int(dates.searchsorted(pd.Timestamp(end), side="right"))
        train_end = a - HORIZON
        mean, std = features[:train_end].mean(axis=0), features[:train_end].std(axis=0)
        scaled = np.clip((features - mean) / std, -5, 5)
        env = AllocationEnv(scaled[:train_end], returns[:train_end], seed)
        model = PPO("MlpPolicy", env, seed=seed, verbose=0, device="cpu",
                    policy_kwargs={"net_arch": [32, 32]})
        model.learn(total_timesteps=STEPS)
        weights = np.zeros(len(ASSETS) + 1, dtype=np.float32)
        weights[-1] = 1.0
        for t in range(a, b):
            observation = np.concatenate([scaled[t].astype(np.float32), weights])
            action, _ = model.predict(observation, deterministic=True)
            weights = softmax(3.0 * action.astype(np.float64)).astype(np.float32)
            rows.append((dates[t], *weights[:-1]))
    return pd.DataFrame(rows, columns=["date", *ASSETS]).set_index("date")


def report() -> None:
    market = research_market()
    prices = research_prices()
    symbols = market.close.columns
    results, frames = {}, []
    for seed in SEEDS:
        path = OUT / f"e08_ppo_seed{seed}.parquet"
        if not path.exists():
            print(f"seed {seed}: no saved weights")
            continue
        targets = pd.read_parquet(path).reindex(columns=symbols, fill_value=0.0)
        frames.append(targets)
        results[f"PPO seed {seed}"] = evaluate(market, targets, rebalance_band=0.05, start=TEST_START)
    ensemble = sum(frames) / len(frames)
    results["PPO ensemble"] = evaluate(market, ensemble, rebalance_band=0.05, start=TEST_START)
    results["PPO ensemble, 0 bps"] = evaluate(
        market, ensemble, cost_bps=0.0, rebalance_band=0.05, start=TEST_START
    )
    thirds = rules.fixed_mix(prices, {s: 1 / 3 for s in ASSETS})
    mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
    results["SPY/IEF/GLD thirds"] = evaluate(market, thirds, start=TEST_START)
    results["60/40 SPY/IEF"] = evaluate(market, mix, start=TEST_START)
    results["Capped 60/40"] = evaluate(
        market, rules.volatility_cap(mix, prices, 0.08, 20), rebalance_band=0.05, start=TEST_START
    )
    results["SPY buy & hold"] = evaluate(market, rules.fixed_mix(prices, {"SPY": 1.0}), start=TEST_START)
    print(format_table(results_table(results)))
    print("\nPPO ensemble average weights: "
          + ", ".join(f"{s} {ensemble[s].mean():.0%}" for s in ASSETS)
          + f", cash {1 - ensemble.sum(axis=1).mean():.0%}")
    by_block = ensemble.groupby(ensemble.index.year)[ASSETS].mean()
    print((by_block * 100).round(0).T.to_string())


if __name__ == "__main__":
    if sys.argv[1] == "report":
        report()
    else:
        seed = int(sys.argv[1])
        began = time.time()
        OUT.mkdir(exist_ok=True)
        train_seed(seed).to_parquet(OUT / f"e08_ppo_seed{seed}.parquet")
        print(f"seed {seed} done in {time.time() - began:.0f}s")
