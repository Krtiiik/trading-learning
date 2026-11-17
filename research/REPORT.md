# Report: can a simple daily-rebalanced ETF strategy make a modest profit after costs?

**Status: in progress** (last updated after E01, 2026-11-17 22:45). The holdout has not been run.
See `LOG.md` for every experiment.

## Setup

$10,000, 25 ETFs, daily bars, long-only, no leverage, fractional shares, no commission,
5 bps per side, signal at close of day t, fill at open of day t+1, cash earns 0%.
Walk-forward window 2005-01-03 .. 2024-11-15. Holdout from 2024-11-17 is sealed.

## Baselines (the bar to beat)

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY buy & hold | 59,860 | 3,015 | 10.3% | 19.1% | 0.61 | -55.2% | 0.0x | 9 |
| Equal weight (1/N) | 42,918 | 2,162 | 8.8% | 14.8% | 0.64 | -41.9% | 0.8x | 387 |
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| TSMOM 12m, 1/N | 23,032 | 1,160 | 6.2% | 8.8% | 0.73 | -15.6% | 3.3x | 1,295 |
| SPY>SMA200 else IEF | 29,848 | 1,503 | 7.2% | 12.4% | 0.62 | -27.3% | 5.8x | 2,154 |
| RSI2 pullback SPY | 5,843 | 294 | 2.3% | 6.4% | 0.40 | -15.0% | 8.1x | 1,977 |
| XS 5d reversal, 5 worst | 19,672 | 991 | 5.6% | 20.1% | 0.37 | -49.1% | 89.8x | 36,338 |

## Best candidates so far

None yet beyond the baselines.

## What we know so far

- The dollar target (a few hundred per year) is cleared by every baseline, including doing
  nothing but holding SPY. The real test is risk-adjusted: beat Sharpe 0.75 (60/40) or match
  it with a much smaller drawdown (12-month time-series momentum: 0.73, maxDD -15.6%).
- High-turnover daily mean reversion does not survive 5 bps and a t+1 fill.

## Open questions

- Does inverse-vol weighting plus a trend filter and a no-trade band beat plain TSMOM?
- Does a learned allocator (small direct-policy model or RL) add anything over the rules?
