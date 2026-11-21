An **order** is the instruction you give your [[broker]]: what to trade, how much, and on what terms. The terms are the order type. Three types cover almost everything.

## Market order: "trade now"

You buy or sell immediately at the best price available right now. When you buy, you pay the ask (the lowest price a seller wants right now); when you sell, you get the bid (the highest price a buyer offers). See [[bid-and-ask]]. A market order is almost always filled (carried out), but you do not know the exact price in advance, because the bid and ask can move just before your order fills.

The gap between the bid and the ask is the [[spread]]. Compared with the mid price (halfway between the two), one market order costs about half the spread. A round trip, buying and then selling again, costs about the full spread.

## Limit order: "only at this price or better"

You set the worst price you accept. A buy limit at $50 buys only at $50 or lower. A sell limit at $60 sells only at $60 or higher. Until then, the order waits in the order book (the list of waiting orders). You control the price, but the order may never fill. Reaching your price is not always enough: orders placed earlier at the same price fill first, so if the price only touches your limit and turns back, yours may not fill.

## Stop order: "once the price gets here, trade"

The order waits until the price reaches or passes a level you chose (the **stop price**), then turns into a market order. From that moment it fills at the best price available, which can be worse than the stop price. Its most common use is a [[stop-loss]]: a sell stop below the current price that sells what you hold automatically if the price falls.

## Example

A [[stock]] trades at $100: the bid is $99.98 and the ask is $100.02.

| You want to…             | Order         | What happens                                                     |
|--------------------------|---------------|------------------------------------------------------------------|
| Buy right away           | Market buy    | Fills now at the ask, about $100.02                              |
| Buy only if it dips      | Limit buy $95 | Waits; fills only if the price falls to $95 or lower             |
| Get out if it falls hard | Stop sell $90 | Waits; once the price reaches or passes $90, sells at the market |

The market buy fills at once at the ask, about $100.02. The limit buy at $95 does nothing while the price stays above $95; if the price never falls that far, you never buy. The stop sell at $90 also waits. When the price reaches or passes $90, it becomes a market sell at the bid, usually a few cents below $90.

## Watch out

A stop order becomes a market order, so it does not guarantee the stop price. After a jump, for example an overnight [[gap]], the price can pass $90 without trading near it, and the sell fills well below. In assets with little [[liquidity]] (few orders waiting near the bid and ask), a market order can also fill at a worse price than you expected: a big order takes all the shares offered at the best price, then fills the rest at the next, worse price.

Next, see [[bid-and-ask]] and [[stop-loss]].
