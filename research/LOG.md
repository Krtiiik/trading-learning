# Research log

Overnight session 2026-11-17 → 2026-11-18. One entry per experiment, appended as I go.

Conventions for every experiment unless stated otherwise:

- Universe: the 25 ETFs in `universe.toml`. Data: Yahoo daily bars fetched into this worktree's
  `data/` with `uv run trading fetch` on 2026-11-17 (the worktree had no data, it is gitignored).
- Sealed holdout: 2024-11-17 onward. All research code loads through `research/common.py`, which
  truncates at 2024-11-16. Only `research/holdout.py` may read past it, once, at the end.
- Evaluation window: 2005-01-03 .. 2024-11-15 (19.9 years). By 2005 the bond, gold and REIT
  ETFs exist; later listings (SLV, DBC 2006, HYG 2007, XLRE 2015, XLC 2018) join when they have bars.
- Account: $10,000, fractional shares, no commission, 5 bps per side (the pessimistic end of the
  brief), cash earns 0%. Signal on the close of day t, fill at the raw open of day t+1.
- Sharpe uses a zero risk-free rate. Turnover is one-way per year.
- Trial count is tracked at the bottom of this file, to be honest about multiple testing.

---

## E00 — Backtester and data check

**Hypothesis.** The engine's accounting matches known quantities on real data.

**Setup.** `research/e00_data_check.py`. Buy and hold SPY 2005 → seal in the engine, three ways.

**Result.**

- No interior gaps in any of the 25 symbols; no missing opens. Four overnight gaps above 15%
  (XLF 2008-09-19, XLE 2020-03-09, XLB and XLF 2020-03-16): all real market events.
- SPY total return: engine with daily reinvestment 6.075 vs adjusted close 6.071 (the 0.07%
  gap is reinvesting at the next open instead of the ex-date close). Price-only is 3.869 and
  dividends-kept-as-cash 4.543, so dividends are accounted for correctly.

**Verdict.** Engine is trustworthy. 30 unit tests cover the accounting, the cost model, the
t+1 lag, dividends and late listings; each rule has a truncation test proving no look-ahead.

---

## E01 — Baselines

**Hypothesis.** None; these set the bar. Parameters are the textbook ones, not tuned.

**Setup.** `research/e01_baselines.py`.

**Result (5 bps, fill at next open).**

| strategy | net P&L $ | $/yr | CAGR | vol | Sharpe | maxDD | turnover/yr | costs $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY buy & hold | 59,860 | 3,015 | 10.3% | 19.1% | 0.61 | -55.2% | 0.0x | 9 |
| Equal weight (1/N) | 42,918 | 2,162 | 8.8% | 14.8% | 0.64 | -41.9% | 0.8x | 387 |
| 60/40 SPY/IEF | 35,160 | 1,771 | 7.9% | 10.9% | 0.75 | -31.6% | 0.5x | 227 |
| TSMOM 12m, 1/N | 23,032 | 1,160 | 6.2% | 8.8% | 0.73 | -15.6% | 3.3x | 1,295 |
| SPY>SMA200 else IEF | 29,848 | 1,503 | 7.2% | 12.4% | 0.62 | -27.3% | 5.8x | 2,154 |
| SPY>SMA200 else cash | 28,928 | 1,457 | 7.1% | 11.6% | 0.65 | -24.4% | 2.9x | 1,029 |
| RSI2 pullback SPY | 5,843 | 294 | 2.3% | 6.4% | 0.40 | -15.0% | 8.1x | 1,977 |
| XS 5d reversal, 5 worst | 19,672 | 991 | 5.6% | 20.1% | 0.37 | -49.1% | 89.8x | 36,338 |

Sharpe by sub-period (5 bps):

| strategy | 2005-09 | 2010-14 | 2015-19 | 2020-24 |
|---|---:|---:|---:|---:|
| SPY buy & hold | 0.13 | 0.98 | 0.88 | 0.76 |
| Equal weight (1/N) | 0.39 | 0.92 | 0.87 | 0.66 |
| 60/40 SPY/IEF | 0.28 | 1.38 | 1.09 | 0.70 |
| TSMOM 12m, 1/N | 0.68 | 0.95 | 0.66 | 0.59 |
| SPY>SMA200 else IEF | 0.47 | 0.65 | 0.68 | 0.71 |
| SPY>SMA200 else cash | 0.37 | 0.68 | 0.63 | 0.87 |
| RSI2 pullback SPY | 0.44 | 0.38 | 0.18 | 0.62 |
| XS 5d reversal, 5 worst | 0.58 | 0.36 | -0.01 | 0.41 |

**Observations.**

- "A few hundred dollars a year on $10k" is a low bar in absolute terms: every baseline clears
  it, and plain SPY made about $3,000/yr (compounded, so back-loaded). The honest question is
  therefore whether anything beats the passive baselines per unit of risk, not whether it
  makes money.
- Passive mixes are hard to beat: 60/40 has the best Sharpe (0.75) at 0.5x turnover.
- 12-month TSMOM matches it on Sharpe (0.73) with a third of the drawdown (-15.6% vs -31.6%),
  but earns less in dollars because about 40% of the account sits in cash earning nothing.
- The SMA200 switch on SPY does not beat buy and hold on Sharpe here; it halves drawdown.
  Daily checking whipsaws: 5.8x turnover and $2,154 of costs for the IEF version.
- Mean reversion is the cost story: the cross-sectional 5-day reversal earns Sharpe 0.82 at
  zero cost, 0.64 at 2 bps, 0.37 at 5 bps, and 0.24 if filled at the next close instead of
  the next open. 90x turnover; $36k of costs on a $10k account. Its edge also decays by
  sub-period (0.58 → 0.36 → -0.01 → 0.41). RSI-2 on SPY is alive but small (Sharpe 0.40) and
  in the market only a fraction of the time.

**Verdict.** Bar to beat after costs: Sharpe ≈ 0.75 (60/40) or ≈ 0.73 with maxDD ≈ -16% (TSMOM).

**Next.** Literature review (E02 notes), then candidates that the evidence supports.

---

## E02 — Literature review (web research by a sub-agent, sources in its report)

Not an experiment; recorded because it decides what gets tried. Summary of what the evidence
says for this exact setup (daily bars, long-only, t+1, 2–5 bps):

- **Slow trend following** (Faber 10-month SMA, MOP time-series momentum) is the best supported
  family. Realistic expectation Sharpe 0.5–0.7 and lagging SPY in bull markets. The more
  parameters (GEM, ADM, VAA/DAA) the worse the post-publication decay.
- **Short-term mean reversion** (IBS, RSI-2, 1–5 day reversal) has decayed since about 2015 and
  is measured entering at the signal close; a t+1 entry removes much of it. Fragile.
- **Volatility targeting** reliably cuts tail risk and gives a small Sharpe gain on equity and
  credit only (Harvey et al. 2018; Barroso-Detzel 2021: only the vol-managed market survives
  costs). Without leverage it can only de-risk.
- **Calendar effects**: turn-of-the-month is old and cheap but has thin recent evidence;
  overnight anomaly and pre-FOMC drift are dead after costs; TLT month-end is vendor evidence.
- **Sector momentum** on SPDRs: weak, short sample, equity-like drawdowns.
- **RL / deep learning**: no independent replication beating 1/N after costs; results swing
  with the random seed (one project: test Sharpe +0.86 to -0.32 across seeds); FinRL's own
  authors name backtest overfitting as a core problem. Zhang-Zohren-Roberts (2020) report
  Sharpe 1.4 at 10 bps on four ETFs, but in one bull window and with VIX as an "asset".
  Simplest defensible setup: a small direct-policy model, walk-forward, many seeds, treated
  as a likely negative result.
- **Pitfalls**: log every trial (deflated Sharpe); Yahoo opens are lower quality than closes.

Sub-agent's picks: (1) trend-filtered inverse-vol asset-class core with a no-trade band,
(2) a portfolio-level volatility cap, (3) a small turn-of-month tilt.

---

## Trial count

Configurations evaluated on the walk-forward window so far (every one, including failures):

- E01: 8 baselines (no tuning).
