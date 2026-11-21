A stop loss is a sell order that you place below the current price (usually below the price you paid). It waits, and if the price falls to that level, it sells automatically. It lets you choose the loss you plan to accept before the trade starts, while you are not yet tempted to "wait and see".

Most often it is a plain stop order (see [[order-types]]): an order that waits until the price reaches or passes a level you chose, the **stop price**. It then becomes a market order, which sells right away at the best price a buyer offers at that moment. A stop-limit version becomes a limit order instead, so it sells only at your price or better; in a fast drop it may not sell at all.

If you sold [[short-selling|short]] (sold borrowed shares, hoping to buy them back cheaper), the stop is a buy order above the price instead.

## Example

You buy a [[stock]] at $42 and decide you are willing to lose about $4 per share. You place a stop loss at $38.

- The price rises to $60: nothing happens; the stop just waits below.
- The price falls to $38: the stop turns into a market order and sells around $38. You lose about $4 per share, an amount you chose in advance.

## Where to put it

- **Too close** and normal day-to-day wobbles trigger it, so you are stopped out (sold by your stop) of trades that would have worked. How much a price usually wobbles is its [[volatility]]; the [[atr]] is a common way to measure it. A stock that often moves $2 in a day needs a wider stop than one that moves $1.
- **Too far** and each loss is bigger than it needs to be.

## What the stop lets you plan

A common approach is to choose the stop first, then pick how many shares to buy so that hitting the stop costs only a small part of your account that you choose in advance. With a $10,000 account and 1% at risk, that part is $100, so the $4 stop in the example allows $100 / $4 = 25 shares. That is [[position-sizing]].

The stop also tells you the possible loss to compare with the possible gain: the [[risk-reward]] of the trade.

## Watch out

A stop loss usually keeps your loss close to what you planned, but it does not guarantee the exact price. If the price jumps past your stop, for example in a [[gap]] overnight, the stop sells at the first price after the jump, which can be well below the stop. If the stock closes at $40 and opens the next morning at $35, the stop sells around $35: a loss of about $7 per share, not $4. With the 25 shares from above, that is about $175 instead of the planned $100.

Next, see [[position-sizing]], then [[risk-reward]].
