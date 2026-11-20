The **spread** is the gap between the bid (the best price a buyer offers) and the ask (the best price a seller wants). It is usually not listed as a fee, but every trade at the market price pays part of it.

## Where the cost comes from

In the [[bid-and-ask]] order book (the list of waiting orders), the bid is $49.98 and the ask is $50.02, so the spread is $0.04. The point halfway between, $50.00, is the **mid price**. A market order usually does not trade there, but the mid price is useful for measuring the cost.

- A market buy pays the ask, $50.02: $0.02 more than the mid price.
- A market sell gets the bid, $49.98: $0.02 less than the mid price.

So one market order (see [[order-types]]) costs about **half the spread**. A **round trip**, buying and then selling again, costs about the **full spread**.

## Example

You buy 100 shares with a market order and change your mind a second later.

| Step | Price | Money |
|------|-------|-------|
| Buy at the ask | $50.02 | you pay $5,002 |
| Sell at the bid | $49.98 | you get $4,998 |
| Result | | **−$4** |

The price did not move, but you lost $4: the full spread. Each order cost $2 compared with the value at the mid price (100 × $50.00 = $5,000).

After buying at $50.02, the bid must rise $0.04 before you can sell without loss. So a trade made with market orders starts with a small loss.

## Why the percentage matters

Compare the spread with the price of each stock:

| Stock | Bid | Ask | Spread | % of price | Round trip on $1,000 |
|-------|-----|-----|--------|------------|----------------------|
| A | $49.98 | $50.02 | $0.04 | 0.08% | about $0.80 |
| B | $1.98 | $2.02 | $0.04 | 2% | about $20 |

Same spread in cents, but on the cheap stock it costs 25 times as much.

## What makes a spread wide or narrow

- **[[liquidity|Liquidity]].** Many orders near the bid and ask keep it small. In the US, large, popular [[stock|stocks]] often have a spread of just one cent, the smallest price step allowed. Rarely traded ones can be far wider.
- **[[trading-hours|Trading hours]].** The spread is usually wider before the open and after the close, when fewer orders wait, and often in the first minutes of the day.

## Avoiding it with limit orders

A limit order trades only at your price or better. A buy limit at $49.98 waits at the bid, behind the orders already there. If it fills, you pay $49.98, not $50.02: no spread. But if the price rises away from you, it may never fill.

## Watch out

The spread comes on top of any [[fees-and-commissions]]. "No commission" is not "no cost": many currency ([[forex-pair|forex]]) brokers quote a wider spread than the market and keep the difference. Zero-commission stock brokers usually fill at the market's best price, but earn in other ways, such as (in the US) payments for sending your order to a particular trading firm.

Next, see [[liquidity]] for what keeps spreads narrow, or [[fees-and-commissions]] for other costs.
