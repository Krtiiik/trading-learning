An **order** is the instruction you give your [[broker]]: what to trade, how much, and on what terms. The terms are the order type. Three types cover almost everything.

## Market order: "trade now"

You buy or sell immediately at the best price available right now. It almost always fills, but you do not know the exact price in advance. When you buy, you pay the ask; when you sell, you get the bid (see [[bid-and-ask]]). The gap between those two prices is the [[spread]]. Each market order pays about half of it, compared with the price in the middle, so buying and then selling again loses about the whole gap.

## Limit order: "only at this price or better"

You set the worst price you accept. A buy limit at $50 buys only at $50 or lower. A sell limit at $60 sells only at $60 or higher. You control the price, but the order may never fill if the market does not reach your price.

## Stop order: "once the price gets here, trade"

The order waits until the price touches a level you chose (the **stop price**), then turns into a market order. Its most common use is a [[stop-loss]]: a sell stop below the current price that gets you out if the trade goes against you.

## Example

A stock trades at $100.

| You want to…                  | Order          | What happens                                           |
|-------------------------------|----------------|--------------------------------------------------------|
| Buy right away                | Market buy     | Fills now, around $100                                  |
| Buy only if it dips           | Limit buy $95  | Waits; fills only if the price falls to $95 or lower    |
| Get out if it falls hard      | Stop sell $90  | Waits; once the price hits $90, sells at the market    |

## Watch out

A stop order becomes a market order, so in a fast fall it can fill well below the stop price. In assets with little [[liquidity]] a market order can also fill at a worse price than you expected.
