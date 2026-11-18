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

## Data

- [The Binance public archive supports a point-in-time universe: delisted pairs are kept and every file is checksummed](binance-archive-coverage.md) (high)
- [The Binance archive has format quirks that are handled in the provider and nowhere else](binance-archive-quirks.md) (high)
- [The point-in-time universe has fewer than 40 members before July 2019](universe-is-smaller-than-40-before-mid-2019.md) (high)
- [A renamed coin drops out of the point-in-time universe for one or two months](renamed-coins-leave-the-universe-briefly.md) (medium)
- [Universe exclusions are a hand-made list, and new listings need a look](universe-exclusions-are-curated.md) (medium)
- [Hourly bars are missing for every coin during exchange outages](hourly-bars-missing-during-outages.md) (high)
- [Rebuilding the Store takes about half an hour and 3.7 GB; open interest would add hours](rebuild-cost.md) (medium)

## Engine

- [A backtest of 40 coins of hourly bars over five years takes about 0.15 seconds](engine-speed.md) (high)
- [Deciding that a bar is the last of its week from the bar after it is look-ahead](calendar-helpers-must-not-peek-at-the-next-bar.md) (high)

## Statistics

- [Two years of data cannot separate a Sharpe ratio of 0.5 from 1.0](two-years-cannot-separate-sharpe-ratios.md) (high)
- [Every statistical tool is validated on synthetic data; these are the conditions it was validated under](statistics-toolkit-validation.md) (high)

## Market (descriptive facts, train data only)

Nothing yet.

## Families

Notes specific to one family (time-series, cross-sectional, derivatives, cross-market) go under
a heading of that name here. Nothing yet.
