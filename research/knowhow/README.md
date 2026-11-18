# Know-how

One note per lesson, pitfall, how-to or fact. Read the notes for your area and everything under
"Everyone" before you start; add a note when you learn something another agent would otherwise
rediscover (`.claude/skills/record-knowhow/SKILL.md`). Trust each note as far as it says: `high` was
measured or tested here, `medium` was seen once or is well sourced elsewhere, `low` is a lead.

## Everyone

- [Trading costs can turn a short-horizon reversal edge into a loss](costs-kill-short-horizon-reversal.md) (medium)
- [Picking the best of about thirty configurations explains an edge of about 0.2 Sharpe by itself](best-of-many-configurations.md) (medium)
- [The ETF scout's conclusions about what works are hypotheses here, not rules](etf-scout-conclusions-are-hypotheses.md) (low)
- [The models doing this research remember markets up to mid-2026, so motivations must cite sources](hindsight-guard.md) (high)

## Process

- [A rule added after seeing where the previous one failed did not hold out of sample](rules-added-after-seeing-results.md) (medium)
- [A date in a hypothesis's parameters must be quoted, or the run cannot be recorded](quote-dates-in-hypothesis-parameters.md) (medium)

## Data

- [The Binance public archive supports a point-in-time universe: delisted pairs are kept and every file is checksummed](binance-archive-coverage.md) (high)
- [The Binance archive has format quirks that are handled in the provider and nowhere else](binance-archive-quirks.md) (high)
- [The point-in-time universe has fewer than 40 members before July 2019](universe-is-smaller-than-40-before-mid-2019.md) (high)
- [A renamed coin drops out of the point-in-time universe for one to several months and its history starts again](renamed-coins-leave-the-universe-briefly.md) (medium)
- [Universe exclusions are a hand-made list, and new listings need a look](universe-exclusions-are-curated.md) (medium)
- [The stored point-in-time universe equals an independent recomputation at all 63 train reconstitutions and never reads the bar of its own date](universe-matches-hand-recomputation-on-train.md) (high)
- [Daily bars of train members are labelled by UTC date, equal the raw archive rows and the 24 hourly bars, and contain no impossible prices](daily-bars-agree-with-raw-files-and-hourly-bars.md) (high)
- [Nine train members stop trading during a month of membership; nothing else is missing from members' daily bars](members-stop-trading-mid-month.md) (high)
- [A coin joins the point-in-time universe with a median of 53 days of history, so a long lookback has no signal for many member-months](new-members-have-short-history.md) (high)
- [Before 2021 the lower ranks of the point-in-time universe traded a few million USDT a day or less](low-ranked-members-were-thin-before-2021.md) (high)
- [Hourly bars are missing for every coin during exchange outages](hourly-bars-missing-during-outages.md) (high)
- [Rebuilding the Store takes about half an hour and 3.7 GB; open interest would add hours](rebuild-cost.md) (medium)

## Engine

- [A backtest of 40 coins of hourly bars over five years takes about 0.15 seconds](engine-speed.md) (high)
- [Deciding that a bar is the last of its week from the bar after it is look-ahead](calendar-helpers-must-not-peek-at-the-next-bar.md) (high)
- [A rule that decides every day drops one slot at each member's last bar, and `dropped_weight` adds these up from the first bar of the data](dropped-weight-counts-targets-at-a-last-bar.md) (high)

## Statistics

- [Two years of data cannot separate a Sharpe ratio of 0.5 from 1.0](two-years-cannot-separate-sharpe-ratios.md) (high)
- [Every statistical tool is validated on synthetic data; these are the conditions it was validated under](statistics-toolkit-validation.md) (high)
- [A trading claim whose true Sharpe difference is 0.25 becomes a candidate one time in four and supported one time in nine, and a candidate's train estimate averages 0.7](small-sharpe-differences-rarely-climb-the-ladder.md) (medium)

## Market (descriptive facts, train data only)

- [From 2019-07 to 2022-12 the equal-weight universe re-equalised every day did worse than re-equalised monthly, so a benchmark's schedule is part of a trading claim](equal-weight-daily-against-monthly-on-train.md) (medium)

## Families

Notes specific to one family (time-series, cross-sectional, derivatives, cross-market) go under
a heading of that name here.

### Time-series

- [A 20-day trend filter evaluated every day across the 40 members turns the portfolio over 22 to 24 times a year and pays about 10% a year in costs](daily-trend-filter-turnover-and-cost.md) (high)
- [For the minimum detectable effect of a per-coin long-or-flat filter against its equal-weight benchmark, a correlation of 0.75 matches what was measured](trend-filter-correlation-with-its-benchmark.md) (medium)
