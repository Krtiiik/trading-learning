# Report: can a simple daily-rebalanced ETF strategy make a modest profit after costs?

**Status: in progress** (last updated after E09, 2026-11-17 22:55; E07 direct policy and E08
PPO still to come). **The holdout has not been run.** See `LOG.md` for every experiment.

## Setup

$10,000, 25 ETFs, daily bars, long-only, no leverage, fractional shares, no commission,
5 bps per side, signal at close of day t, fill at open of day t+1, cash earns 0%.
Walk-forward window 2005-01-03 .. 2024-11-15 (19.9 years). Holdout from 2024-11-17 is sealed.

## Results so far (5 bps, walk-forward window)

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Baselines** | | | | | | | | |
| SPY buy & hold | 59,860 | 3,015 | 10.3% | 19.1% | 0.61 | -55.2% | 0.0x | 9 |
| Equal weight (1/N) | 42,918 | 2,162 | 8.8% | 14.8% | 0.64 | -41.9% | 0.8x | 387 |
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| TSMOM 12m, 1/N | 23,032 | 1,160 | 6.2% | 8.8% | 0.73 | -15.6% | 3.3x | 1,295 |
| SPY>SMA200 else IEF | 29,848 | 1,503 | 7.2% | 12.4% | 0.62 | -27.3% | 5.8x | 2,154 |
| RSI2 pullback SPY | 5,843 | 294 | 2.3% | 6.4% | 0.40 | -15.0% | 8.1x | 1,977 |
| XS 5d reversal, 5 worst | 19,672 | 991 | 5.6% | 20.1% | 0.37 | -49.1% | 89.8x | 36,338 |
| **Candidates** | | | | | | | | |
| Capped 60/40 (8% vol cap, 5% band) | 28,290 | 1,425 | 7.0% | 7.3% | 0.97 | -17.3% | 0.8x | 302 |
| Blend 50/50 trend + capped | 23,325 | 1,175 | 6.3% | 6.9% | 0.91 | -12.6% | 1.1x | 417 |
| InvVol trend + band | 18,610 | 937 | 5.4% | 7.2% | 0.78 | -15.0% | 2.1x | 786 |
| Turn of month SPY | 1,289 | 65 | 0.6% | 8.0% | 0.12 | -24.6% | 12.0x | 2,313 |
| Ridge top-5 (supervised ML) | 17,034 | 858 | 5.1% | 12.8% | 0.46 | -30.8% | 33.6x | 12,239 |
| GBM top-5 (supervised ML) | 16,009 | 806 | 4.9% | 14.5% | 0.40 | -38.2% | 29.9x | 10,756 |

## Leading candidate

**Capped 60/40**: hold 60% SPY / 40% IEF, scaled down each day so the portfolio's expected
volatility (20-day covariance) is at most 8% a year; the rest in cash; skip rebalances
smaller than 5% of equity.

- For: best Sharpe and near-best drawdown in the window; robust to its own parameters (all
  six target×window cells score 0.86–0.97 vs 0.75 uncapped); works on four other mixes;
  costs are irrelevant at 0.8x turnover; bootstrap interval of its Sharpe edge over plain
  60/40 excludes zero ([+0.05, +0.37]).
- Against: on 1994-2004 (outside the window, VFITX as bond proxy) it did **not** beat plain
  60/40 (Sharpe 0.86 vs 0.88) and cost 2.8 points of CAGR. Its edge comes from the fast
  crashes of 2008 and 2020. It earns fewer dollars than the passive mixes in every period.

## What we know so far

- The dollar target (a few hundred per year on $10k) is cleared by every baseline, including
  holding SPY. The real test is risk-adjusted.
- Nothing that trades often survives: daily mean reversion, turn-of-month and the supervised
  ML predictor all lose to passive mixes at 5 bps (the ML one even at 0 bps).
- Slow trend following matches 60/40 on Sharpe with half the drawdown, but is statistically
  indistinguishable from it and is weakest in 2020-24.
- The only thing that looked like an improvement is risk management (the cap), and its
  advantage is regime-dependent.

## Open questions

- Does a learned allocator (direct policy optimisation, PPO) add anything? (E07, E08)
