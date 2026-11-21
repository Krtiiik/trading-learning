At any moment, a market has two prices, not one. The **bid** is the highest price a buyer offers right now. The **ask** is the lowest price a seller wants right now. The ask is above the bid, usually by only a little.

## Where the two prices come from

An [[exchange]] keeps a list of orders that wait to be filled (carried out). These are limit orders (see [[order-types]]): "buy only at $49.98 or lower", "sell only at $50.02 or higher". This list is the **order book**.

The highest waiting buy order is the bid; the lowest waiting sell order is the ask. The bid always stays below the ask: if a buyer offered as much as a seller wanted, the two orders would make a trade (a buyer and a seller agreeing on a price) at once.

## How a trade happens

A trade happens when someone accepts one of the two prices, usually with a market order (trade now at the best price).

- A **market buy** pays the ask.
- A **market sell** gets the bid.

The prices can move just before your order fills, so you may pay a little more or less.

A limit order between the two prices does not trade. A buy limit at $50.00 waits and becomes the new bid.

## Example

The order book of a [[stock]] at one moment:

| Side  | Price  | Shares waiting |
|-------|--------|----------------|
| Sell  | $50.03 | 200            |
| Sell  | $50.02 | 100 ← ask      |
| Buy   | $49.98 | 400 ← bid      |
| Buy   | $49.97 | 150            |

- A market buy for 10 shares pays $50.02 each.
- A market sell for 10 shares gets $49.98 each.
- A market buy for 150 shares pays $50.02 for the first 100 and $50.03 for the other 50.

The more shares wait near the bid and ask, the more you can trade without moving the price. That is a big part of a stock's [[liquidity]].

The 4-cent gap between $49.98 and $50.02 is the [[spread]].

## Bid, ask and the price on a chart

For stocks, apps and [[price-chart|price charts]] usually show the price of the last trade. The bid and ask may have moved since then. If the last trade was $49.98, the app shows $49.98, but buying now costs $50.02. Check both prices before a market order. Many currency ([[forex-pair|forex]]) apps draw the chart from the bid, the price you get when you sell.

## Watch out

- **The names come from the other side.** Buyers offer the bid, so you get it when you sell. Sellers want the ask, so you pay it when you buy.
- **The gap can widen.** Outside the regular [[trading-hours]], or in a rarely traded stock, few orders wait, so the bid and ask can be far apart.

Next, see [[spread]] for what the gap costs, or [[order-types]] for the ways to place an order.
