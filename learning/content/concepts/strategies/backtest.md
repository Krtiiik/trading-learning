A backtest runs a [[strategy]]'s rules on past prices, step by step, as if you had traded them then. It shows how they would have done before you risk real money.

## How it works

1. **Fix the rules.** Write down exactly when to enter, exit and how much to buy.
2. **Take past data.** Say, ten years of daily closes for one [[stock]].
3. **Simulate the trades.** Go through the data one bar at a time (one day, for daily data), using only what was known then. Record each trade, from entry to exit.
4. **Add up the results**, after costs such as the [[spread]] and [[fees-and-commissions|fees]].

## What it reports

- **Total return**: the account's overall gain or loss.
- **Number of trades**: how many trades the rules made.
- **Win rate**: the share of trades that ended in a gain (see [[win-rate-and-expectancy]]).
- **Worst fall from a high**: the account's largest drop from a peak, its [[drawdown]]. It shows how painful the strategy was to follow.

## Example

The rules: buy one stock on the first close above its 100-day [[moving-average]], and sell on the first close below, with a stop $4 below entry. On a $10,000 account, 25 shares risk about $100 (1%) if the stop is hit. The test finds 10 trades:

| Trade | Result | Account |
|-------|--------|---------|
| 1 | +$150 | $10,150 |
| 2–5 | −$25, −$40, −$30, −$25 | $10,030 |
| 6 | +$550 | $10,580 |
| 7–9 | −$50, −$20, −$30 | $10,480 |
| 10 | +$300 | $10,780 |

- **Total**: three wins make $1,000 and seven losses cost $220: +$780 (7.8%) before costs.
- **Win rate**: 3 of 10, or 30%. The few big wins pay for the many small losses.
- **Worst fall**: counted at the end of each trade, four losses took the account from $10,150 to $10,030: $120 before costs, $140 with $5 of costs on each of the four trades. Inside a trade it can fall further.
- **Costs**: at $5 per round trip (buying, then selling again), 10 trades cost $50, leaving +$730.

Ten trades is few: one more big win or loss would change this a lot.

## Overfitting, and how to catch it

Each backtest uses one fixed rule set, but you can run many, changing a setting each time (a 97-day average, a stop at $3.80), and keep the best. Go far enough and the rules fit chance moves, not a real pattern: **overfitting**. Such rules often fail later.

To catch it, tune on one stretch, such as the first seven years, then run the rules unchanged on the last three. Much worse results there suggest overfitting. Do this once only: rules changed after seeing those three years have not been tested on unseen data.

## Watch out

- **Left-out costs.** Without the spread, fees and slippage (getting a worse price than the test assumed), a backtest looks better than real trading.
- **Look-ahead bias.** Using data you would not have had then. A rule that checks the day's close but buys at that day's open could never be traded.
- **Survivorship bias.** Picking from today's companies leaves out those that went bankrupt or were delisted (removed from the exchange). Many were losers, so results look too good.
- **The past does not repeat exactly.** A good backtest shows the rules worked then, not that they will work next.

Next, see [[win-rate-and-expectancy]], then [[drawdown]].
