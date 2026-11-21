**Liquidity** is how easily you can buy or sell an asset right now, without moving its price. In a liquid market, your order fills quickly, close to the best bid or ask.

## What makes a market liquid

A stock or crypto [[exchange]] keeps an order book, the list of waiting orders, whose best buy and sell prices are the bid and the ask (see [[bid-and-ask]]). Three things in the book show liquidity:

- **Many shares waiting near the bid and ask.** A market order (trade now at the best price, see [[order-types]]) fills at or near the best price.
- **A narrow [[spread]].** The gap between the bid and the ask is small, so each market order costs little.
- **Depth.** Many shares also wait at the prices beyond the best ones. A deep book can take a big order; a thin book cannot.

[[volume|Volume]] counts past trading; liquidity is about trading now. High volume usually comes with a liquid book.

## Example

Two [[stock|stocks]], both with a mid price (halfway between bid and ask) of $50.00. You buy 300 shares of each with a market order. It takes all the shares at the best price, then fills the rest at the next, worse price. This is called **slippage**: a worse price than you expected.

**Stock A** has the [[bid-and-ask]] order book (bid $49.98), plus 500 shares at $50.04:

| Shares | Price | Cost |
|--------|-------|------|
| 100 | $50.02 | $5,002 |
| 200 | $50.03 | $10,006 |
| **300** | | **$15,008** |

**Stock B** has a thin book: the bid is $49.90, the ask $50.10 with only 50 shares, then $50.25 with 100 and $50.50 with 150.

| Shares | Price | Cost |
|--------|-------|------|
| 50 | $50.10 | $2,505 |
| 100 | $50.25 | $5,025 |
| 150 | $50.50 | $7,575 |
| **300** | | **$15,105** |

At the mid price, 300 shares are worth $15,000. Stock A costs $8 more; stock B costs $105 more. Afterwards, A's ask is $50.04, 2 cents higher. B's is above $50.50, more than 40 cents higher.

## Liquid and illiquid assets

A large company's stock trades millions of shares a day, often with a 1-cent spread in the US and thousands of shares at each price. A small company's stock may trade a few thousand shares a day, with a wide spread and little depth. Popular currency pairs ([[forex-pair|forex]]) are very liquid; small [[cryptocurrency|cryptocurrencies]] can be very illiquid.

## Liquidity changes

- **With the time of day.** For stocks, outside the regular [[trading-hours]], fewer orders wait, so spreads widen and the book thins. Forex trades around the clock on weekdays and crypto every day; both thin out at quiet hours, crypto also at weekends.
- **In a panic.** When prices fall fast, many buyers cancel their waiting orders, so the bid drops and the book thins.

## Watch out

- **Liquidity can disappear when you need it most.** In a crash, a market sell or a plain [[stop-loss]] order fills much lower than you planned, with heavy slippage.
- **Size matters.** A book that is liquid for 10 shares can be thin for 10,000.
- **Use limit orders in thin markets.** A limit order sets the worst price you accept, but it may not fill.

Next, see [[spread]] for what each trade costs, or [[trading-hours]] for when liquidity is highest.
