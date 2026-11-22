Entry and exit rules are the exact conditions in a [[strategy]] that open and close a trade. Here a trade means one position: a buy and the later sale that closes it. The **entry rule** opens it; the **exit rules** close it.

## What makes a rule exact

An exact rule needs no judgment: two people following it get the same trades. It says:

- **The condition**: what must be true, such as "the daily close is above the 100-day [[moving-average]]" (the average of the last 100 daily closes).
- **The time**: when you check and trade. The close is known only once the market closes. So the rule says either "check a few minutes before the close and treat that price as the close" or "check the close, then trade at the next day's open". Never trade at that day's open: the close was not yet known.
- **The order**: which of the [[order-types]] carries out the rule.

## Kinds of exit

- **Stop loss exit**: a [[stop-loss]] order sells if the price falls to your level. A [[gap]] can sell it lower.
- **Target exit**: a sell limit order sells at your target or higher, but may not fill if the price only touches it. With the entry price, the target and the stop give the [[risk-reward]].
- **Signal exit**: sell on a chart signal, such as a close below the moving average.
- **Time exit**: sell after a set time, for example 60 trading days.

A trade can have several exits; the first one closes it. Then cancel the other waiting orders, or a forgotten stop can later sell shares you no longer hold. Many brokers offer one-cancels-other orders for this. Plan all exits before you enter.

## Example

The vague idea "buy when the [[stock]] looks strong" is not a rule. The [[trend-following]] rules make it exact:

- **Entry**: check the price a few minutes before each close. On the first day it is above the average, buy with a market order (it trades at once).
- **Signal exit**: on the first day it is below the average, sell the same way.
- **Stop loss exit**: a stop order $4 below entry.

Near the close the stock is at $42, above its average: you buy. On a $10,000 account, [[position-sizing]] gives 25 shares, about 1% at risk, with the stop at $38. Months later it closes below the average at $64: you sell, a gain of $22 a share before costs. No target order waits, so the trade stays open with the trend. In a slow fall, the signal exit usually comes before the stop.

## Watch out

- **Vague rules cannot be tested.** A [[backtest]] cannot decide what "looks strong" means.
- **Do not change the rules during a trade.** Moving the stop lower to "give it room" breaks the tested rules. Change rules only between trades, and test them again first.
- **More conditions are not always better.** Each added condition can fit chance moves, not a real pattern: overfitting.

Next, see [[backtest]], then [[order-types]].
