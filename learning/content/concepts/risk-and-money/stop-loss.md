A stop loss is a sell order placed below the price you paid. It waits, and if the price falls to that level, it sells automatically. It decides your maximum loss on a trade before you are in the middle of it and tempted to "wait and see".

Technically it is a stop order (see [[order-types]]): once the price touches the stop level, it becomes a market order.

## Example

You buy a stock at $50 and decide you will not lose more than $5 per share. You place a stop loss at $45.

- The price rises to $60: nothing happens; the stop just waits.
- The price falls to $45: the stop triggers and sells around $45. You lose about $5 per share instead of an unknown amount.

## Where to put it

- **Too close** and normal day-to-day wobbles trigger it, so you are stopped out of trades that would have worked. How much a price usually wobbles is its [[volatility]]; the [[atr]] is a common way to measure it.
- **Too far** and each loss is bigger than it needs to be.

A common approach is to choose the stop first, then pick how many shares to buy so that hitting the stop costs only a small, fixed part of your account. That is [[position-sizing]].

Knowing the stop also lets you compare the possible loss with the possible gain: the [[risk-reward]] of the trade.

## Watch out

A stop loss limits your loss, but it does not guarantee the exact price. If the price jumps past your stop, for example in a [[gap]] overnight, the order sells at the next available price, which can be well below the stop.
