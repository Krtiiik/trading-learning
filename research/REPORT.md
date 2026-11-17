# Report: can a simple daily-rebalanced ETF strategy make a modest profit after costs?

**Status: in progress** (updated 2026-11-17 23:00, after E11; E08 PPO is training).
**The holdout has not been run.** Every experiment is in `LOG.md`.

## Short answer (so far)

- **Making a few hundred dollars a year on $10k is easy and needs no strategy.** Every passive
  baseline did it over 2005-2024: SPY about $3,000/yr, 60/40 about $1,800/yr, compounded.
  That profit is payment for holding stocks and bonds, not for trading daily.
- **Trading daily did not add to it.** Everything that trades often (mean reversion,
  turn-of-month, a supervised ML predictor, a learned direct policy) lost to the passive
  mixes after 5 bps, and the ML ones lost even at zero cost.
- **The one thing that helped was risk management.** Scaling a 60/40 mix down when its
  recent volatility is high gave the best risk-adjusted result (Sharpe 0.97 vs 0.75,
  drawdown -17% vs -32%) but fewer dollars, and on 1994-2004 it gave no Sharpe edge at all.
- Beyond plain market exposure, the slow timing rules earned about $200 a year on $10k
  ("alpha"). That is the size asked for, but it is not statistically solid.

## Setup

$10,000, 25 ETFs, daily bars, long-only, no leverage, fractional shares, no commission,
5 bps per side, signal at the close of day t, fill at the open of day t+1, cash earns 0%.
Walk-forward window 2005-01-03 .. 2024-11-15 (19.9 years). Holdout from 2024-11-17 is sealed.
Backtester: `src/trading/backtest/`, 30 unit tests, cross-checked by hand on real data (E00).

## Results on the walk-forward window (5 bps)

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
| Direct policy, linear (5-seed ensemble) | 6,885 | 347 | 2.7% | 10.5% | 0.30 | -29.0% | 26.8x | 7,371 |
| Direct policy, MLP (5-seed ensemble) | 2,370 | 119 | 1.1% | 10.9% | 0.15 | -30.7% | 59.2x | 14,481 |

## Leading candidate

**Capped 60/40**: hold 60% SPY / 40% IEF, scaled down each day so the portfolio's expected
volatility (20-day covariance) is at most 8% a year; the rest in cash; skip rebalances
smaller than 5% of equity.

## Open

- E08: PPO agent (training).
- Final choice, holdout run, verdict.
