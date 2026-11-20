# Report: can a simple daily-rebalanced ETF strategy make a modest profit after costs?

**Status: finished** 2026-11-17 23:10, well before the 06:00 limit, because the honest ideas
ran out. The sealed holdout was run exactly once. Every experiment, including the failures,
is in `LOG.md`; this file is the summary.

## Verdict

**As a way to beat simply holding ETFs: no, this is not worth pursuing. As a way to make a
few hundred dollars a year on $10,000: yes, but you do not need a strategy for that.**

- The finalist made **+$777 on $10,000 over the two holdout years** (2024-11-17 to
  2026-11-17) after 5 bps per side: about **$390 a year**, 3.8% a year, Sharpe 0.51, worst
  drawdown −9.9%. That is "a few hundred dollars a year", as asked.
- **Every passive baseline made more on the same days**: 60/40 SPY/IEF +$1,879, equal weight
  +$2,610, SPY +$2,776. The finalist was the worst row in the table.
- Over 2005-2024, nothing that trades daily on signals beat a passive stock/bond mix by a
  margin that survives scrutiny. The only effect that looked real was risk management
  (holding less when markets are volatile or falling), which lowers drawdowns and lowers
  dollars earned. In the holdout it did exactly that: less risk, less money.
- Machine learning and reinforcement learning were the clearest failures of the night.

If the goal is modest profit on $10k, the evidence here says: hold a diversified mix,
rebalance rarely, and accept the drawdowns. If the goal is to learn algorithmic trading,
the backtester and the negative results are a good base, and the lesson is that the
profit came from market exposure, not from the daily decisions.

## Setup

- $10,000, the 25 ETFs in `universe.toml`, Yahoo daily bars, long-only, no leverage,
  fractional shares, no commission, **5 bps per side**, cash earns 0%.
- Signal at the close of day t, trade at the raw open of day t+1. Returns come from share
  and cash accounting at raw prices with dividends credited on the ex-date.
- Walk-forward window 2005-01-03 .. 2024-11-15 (19.9 years). Holdout from 2024-11-17,
  sealed until the final run: all research code loads through `research/common.py`, which
  truncates the data at 2024-11-16.
- Backtester in `src/trading/backtest/` (engine, cost model, metrics), rules in
  `src/trading/strategies/`. 103 tests pass, including a truncation test for every rule
  that proves it uses no data after its decision date. The engine was cross-checked on
  real data against hand calculations (SPY total return, 60/40 compounding: within 0.07%).

## The finalist

**Trend-switched + capped 60/40.** Hold 60% SPY while SPY's 12-month return is positive
(otherwise that 60% is cash) and 40% IEF always. Each day scale the whole portfolio down so
its expected volatility (from the last 20 days' covariance) is at most 8% a year. Skip any
rebalance that would move less than 5% of the account. Decide at the close, trade at the
next open. It trades about 1.3x the account per year, so costs are a few dollars.

It was chosen, in writing and in a commit, before the holdout was run (`LOG.md`, "Finalist
choice"). It tied the capped 60/40 for the best walk-forward Sharpe, had the smaller
drawdown, and unlike the capped 60/40 it also held up on 1994-2004.

## Holdout result (run once, reported as-is)

2024-11-17 .. 2026-11-17, 501 sessions, $10,000 start, 5 bps, next-open fill.
Full output in `holdout_result.txt`.

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Finalist: trend-switched + capped 60/40** | **777** | **391** | **3.8%** | 7.9% | **0.51** | **-9.9%** | 1.3x | 26 |
| Capped 60/40 (comparison only) | 1,087 | 547 | 5.3% | 8.1% | 0.68 | -8.5% | 1.1x | 24 |
| SPY buy & hold | 2,776 | 1,396 | 13.1% | 16.9% | 0.81 | -18.8% | 0.2x | 5 |
| Equal weight (1/N) | 2,610 | 1,313 | 12.4% | 11.8% | 1.05 | -12.2% | 1.1x | 25 |
| 60/40 SPY/IEF | 1,879 | 945 | 9.0% | 10.5% | 0.88 | -10.5% | 0.7x | 15 |
| TSMOM 12m, 1/N | 1,846 | 929 | 8.9% | 9.9% | 0.91 | -11.1% | 3.1x | 68 |
| SPY>SMA200 else IEF | 1,706 | 858 | 8.2% | 12.4% | 0.70 | -11.4% | 3.0x | 64 |

At 2 bps the finalist made +$793; costs are not the story.

How to read it:

- The finalist was profitable and had the smallest volatility, but it lost to every
  baseline on dollars and on Sharpe. Its drawdown (−9.9%) was barely better than plain
  60/40 (−10.5%) on these days, so it paid for protection and got little.
- Its walk-forward Sharpe was 0.96; the holdout Sharpe is 0.51. Two years is a short
  sample (a Sharpe measured over two years has a standard error of roughly 0.7), so this
  does not prove the rule is worthless, but it gives no support for it either, and it is
  the direction the warnings below pointed.
- The simpler capped 60/40 did better than the finalist (+$1,087). The trend switch, the
  part added late after seeing where the cap failed, did not help out of sample.
- I did not analyse the holdout days further. The number stands as it is.

## Walk-forward results, 2005-01-03 .. 2024-11-15 (5 bps)

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
| **Risk-managed mixes** | | | | | | | | |
| Capped 60/40 | 28,290 | 1,425 | 7.0% | 7.3% | 0.97 | -17.3% | 0.8x | 302 |
| **Trend-switched + capped 60/40 (finalist)** | 23,830 | 1,200 | 6.3% | 6.6% | 0.96 | -13.6% | 1.5x | 570 |
| Blend 50/50 trend + capped | 23,325 | 1,175 | 6.3% | 6.9% | 0.91 | -12.6% | 1.1x | 417 |
| InvVol trend + band | 18,610 | 937 | 5.4% | 7.2% | 0.78 | -15.0% | 2.1x | 786 |
| **Other rules** | | | | | | | | |
| Sector top-3, 12m | 36,425 | 1,835 | 8.0% | 16.2% | 0.56 | -28.0% | 13.1x | 5,685 |
| Dual momentum SPY/EFA else IEF | 17,841 | 899 | 5.3% | 15.0% | 0.42 | -40.4% | 8.1x | 2,637 |
| Turn of month SPY | 1,289 | 65 | 0.6% | 8.0% | 0.12 | -24.6% | 12.0x | 2,313 |
| **Learned** | | | | | | | | |
| Ridge top-5 (supervised) | 17,034 | 858 | 5.1% | 12.8% | 0.46 | -30.8% | 33.6x | 12,239 |
| GBM top-5 (supervised) | 16,009 | 806 | 4.9% | 14.5% | 0.40 | -38.2% | 29.9x | 10,756 |
| Direct policy, linear (5-seed ensemble) | 6,885 | 347 | 2.7% | 10.5% | 0.30 | -29.0% | 26.8x | 7,371 |
| Direct policy, MLP (5-seed ensemble) | 2,370 | 119 | 1.1% | 10.9% | 0.15 | -30.7% | 59.2x | 14,481 |
| PPO agent, 2012-2024 only (5-seed ensemble) | -50 | -4 | -0.0% | 11.2% | 0.05 | -36.5% | 29.8x | 3,279 |

Dollar figures compound over 20 years, so "$/yr" is an average that is small early and
large late. `figures/walk_forward.png` shows SPY, 60/40 and the capped 60/40.

## What was tried and what happened

1. **Baselines (E01).** Every one cleared "a few hundred dollars a year". The bar to beat
   became risk-adjusted: Sharpe 0.75 for 60/40.
2. **Short-term mean reversion (E01).** Works on paper, dies in practice. The 5-day
   cross-sectional reversal has Sharpe 0.82 at zero cost, 0.37 at 5 bps and 0.24 with a
   next-close fill; it paid $36k in costs on a $10k account.
3. **Trend following (E01, E03, E05).** Matches 60/40 on Sharpe with half the drawdown,
   statistically indistinguishable from it, weakest in 2020-24. A no-trade band halves its
   costs without changing the result.
4. **Volatility cap (E03, E04).** The best walk-forward result. Robust to its parameters
   (six target×window cells: 0.86–0.97 vs 0.75 uncapped) and helpful on four other mixes.
5. **Out-of-window check on 1994-2004 (E09).** The cap's pre-registered hypothesis failed:
   Sharpe 0.86 vs 0.88 uncapped, and 2.8 points less CAGR. Its edge comes from the fast
   crashes of 2008 and 2020.
6. **Trend switch plus cap (E13).** Ties the cap in the window, holds up on 1994-2004.
   Chosen as finalist. Underperformed in the holdout.
7. **Calendar and relative momentum (E03, E12).** Turn-of-month, sector rotation and dual
   momentum all lose to buy-and-hold SPY after costs.
8. **Supervised ML (E06).** Ridge and gradient boosting on nine per-ETF features find a
   small real signal (rank IC ≈ 0.02) that is just the reversal effect again. Not enough
   even at zero cost.
9. **Direct policy optimisation (E07).** A small network trained on net-of-cost Sharpe.
   In-sample Sharpe up to 2.2, out-of-sample about zero. It either overfits into 60–130x
   turnover or collapses into mostly cash.
10. **PPO agent (E08).** Four of five seeds lost money over 2012-2024 on three assets that
    all rose; fixed thirds of the same assets made $12,978. It learned the last regime
    (67% gold in 2012, just before gold fell).
11. **Alpha regression (E11).** Beyond static stock/bond exposure, the slow timing rules
    earned roughly $140–280 a year on $10k in the window, with t-statistics of 1.2–2.7
    before any correction for the number of things tried.

## Known risks and limits

- **Multiple testing.** 29 distinct configurations were evaluated on the walk-forward
  window (plus 20 declared sensitivity runs). Their Sharpes spread with a standard
  deviation of about 0.25, so the best of 29 landing 0.2 above 60/40 is roughly what
  selection alone produces. The holdout result is consistent with that reading.
- **Regime dependence.** The 60/40 base rode falling interest rates and a negative
  stock-bond correlation for most of 2005-2020. In 2022 both legs fell (−16.5%; the
  finalist −12.1%). Nothing here protects against that.
- **The cap and the trend switch lag.** They cut exposure after volatility or losses have
  appeared and restore it late. They help in long or accelerating declines and hurt in
  sharp drops followed by quick recoveries, and in volatile rising markets (1997-99).
- **Post-hoc design.** The trend switch was added after seeing the cap fail on 1994-2004.
  That was disclosed before the holdout, and the holdout did not reward it.
- **Short holdout.** Two years cannot distinguish a Sharpe of 0.5 from 1.0.
- **Model knowledge.** I am a language model trained on data past November 2024. I did not
  read any holdout bar before the final run, but I cannot fully exclude that vague general
  knowledge of 2025 markets influenced judgment calls.
- **Data.** Yahoo daily bars, fetched into this worktree on 2026-11-17 (`data/` is
  gitignored, so numbers may differ by a hair on a later fetch because adjusted closes
  are rewritten). No gaps or bad opens were found before the seal. The last holdout bar
  (2026-11-17) was fetched about half an hour after the US close and may not be final.
  VFITX (a mutual fund) stood in for IEF before 2002 in E09 and E13 only.
- **Simplifications.** Cash earns 0% (it earned 0–5% over these years, which would add a
  little to every strategy that holds cash). No taxes. 5 bps is assumed for every ETF and
  every day, including open auctions in 2008 and 2020. Sharpe uses a zero risk-free rate.
- **Fills at the open.** Yahoo opens are lower quality than closes; the slow rules were
  re-run with next-close fills and changed by 0.03 Sharpe or less.

## If you want to continue anyway

- The engine, cost model, rules, feature code and walk-forward harness are reusable and tested.
- The one thread with some evidence is risk management of a passive mix. A fair next step
  is not more signals but a longer and broader test of that single idea (more history,
  other countries), judged on drawdown rather than Sharpe.
- I would not spend more time on ML or RL with daily bars on 25 ETFs: about 5,000 days of
  very noisy returns is too little data, and the results above show it.

## Files

- `LOG.md`: every experiment with hypothesis, setup, result and verdict, plus the trial count.
- `holdout_result.txt`: the single holdout run. `holdout.py` refuses to run again while it exists.
- `e00` … `e13`: one script per experiment; `common.py` and `ml_common.py` hold the sealed loaders.
- `figures/walk_forward.png`: equity and drawdown of SPY, 60/40 and the capped 60/40.
