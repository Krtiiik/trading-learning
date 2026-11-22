A backtest runs a [[strategy]]'s rules on past prices as if you had traded them then. It shows how they would have done before you risk money.

## How it works

1. **Fix the rules.** Write down exactly when to enter, exit and how much to buy.
2. **Take past data.** Say, ten years of daily closes for one [[stock]].
3. **Simulate the trades.** Go through the data one day at a time, using only what was known then. Record each trade.
4. **Add up the results**, after costs such as the [[spread]] and [[fees-and-commissions|fees]].

## What it reports

- **Total return**: the account's gain or loss.
- **Number of trades**: how many the rules made.
- **Win rate**: the share of trades with a gain (see [[win-rate-and-expectancy]]).
- **Worst fall from a high**: the account's largest drop, its maximum [[drawdown]]. It shows how painful the strategy was to follow.

## Example

The [[trend-following]] rules: buy one stock on the first close above its 100-day [[moving-average]], and sell on the first close below, with a [[stop-loss|stop]] $4 below entry. On a $10,000 account, [[position-sizing]] gives 25 shares, risking about $100 (1%) if the stop is hit. The test finds 10 trades:

| Trade | Result | Account |
|-------|--------|---------|
| 1 | +$150 | $10,150 |
| 2–5 | −$25, −$40, −$30, −$25 | $10,030 |
| 6 | +$550 | $10,580 |
| 7–9 | −$50, −$20, −$30 | $10,480 |
| 10 | +$300 | $10,780 |

- **Total**: three wins make $1,000 and seven losses cost $220: +$780 (7.8%) before costs.
- **Win rate**: 3 of 10, or 30%. The few big wins pay for the many small losses.
- **Worst fall**: counted at the end of each trade, four losses took the account from $10,150 to $10,030: $120 before costs, $140 with $5 of costs per trade. Inside a trade it can fall further.
- **Costs**: at $5 per round trip (buying, then selling), 10 trades cost $50, leaving +$730.

Ten trades is few: one more big trade would change this a lot.

## Overfitting, and how to catch it

You can run many backtests, changing a setting each time (a 97-day average, a stop at $3.80), and keep the best. Go far enough and the rules fit chance moves, not a real pattern: **overfitting**. Such rules often fail later.

To catch it, tune on one stretch, such as the first seven years, then run the rules unchanged on the last three. Much worse results there suggest overfitting. Do this once: rules changed after seeing those years are not tested on unseen data.

## Watch out

- **Left-out costs.** Without the spread, fees and [[slippage]], a backtest looks better than real trading.
- **Look-ahead bias.** Using data you would not have had then. A rule that checks the day's close but buys at its open could never be traded.
- **Survivorship bias.** Picking from today's companies leaves out those that went bankrupt or were delisted (removed from the [[exchange]]). Many were losers, so results look too good.
- **The past does not repeat exactly.** It shows the rules worked then, not that they will work next.

Next, see [[win-rate-and-expectancy]], then [[drawdown]], or try the lesson [[testing-a-trading-rule]].
