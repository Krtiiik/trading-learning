**Slippage** is the difference between the price you expected and the price your order filled at; usually the fill is worse. The expected price is the ask or bid you saw, or your stop price. It hits market orders and triggered stop orders (see [[order-types]]).

## Where it comes from

- **Your order is bigger than what waits at the best price.** The order book, the list of waiting orders, shows the shares at each price (see [[bid-and-ask]]). A market order takes the shares at the best price, then the next, worse price. A book with few shares has little [[liquidity]].
- **The price moves before your order fills.** After news or just after the open, the bid and ask can move before your order arrives.
- **The price jumps past your stop.** A triggered stop fills at the next price, perhaps far below.

## Example

**A bigger order.** Say the ask is $50.02 with 100 shares, then $50.03 with 200. You buy 150 shares at the market. You pay 100 × $50.02 + 50 × $50.03 = $7,503.50, not 150 × $50.02 = $7,503. The slippage is 50 cents: 1 cent on each of the last 50 shares.

**A gap past a stop.** You bought 25 shares at $42, with a [[stop-loss]] $4 below, at $38. The stock closes at $40 and opens the next morning at $35: a [[gap]] down. Your stop sells around $35: about $3 per share, or $75, of slippage. The loss is about $175 instead of the planned $100.

A thin order book costs cents per share; a jump can cost dollars.

## Slippage and the spread

The [[spread]] is the gap between the best price buyers offer and the best price sellers want. A market buy at the ask you saw pays half the spread, measured from halfway between bid and ask, but has no slippage. Slippage comes on top.

## How to limit it

- **Use limit orders.** A limit order cannot fill worse than the price you set, but it may not fill.
- **Trade when the market is busy.** For stocks, that is the exchange's main daily hours (see [[trading-hours]]), but not their first minutes.
- **Size for it.** Expect losses beyond your stop. Choose a [[position-sizing|position size]] so that a gap like the one above costs an amount you can take.

## Watch out

- **A stop-limit order does not fix it.** It becomes a limit order, not a market order, so it sells only at its limit price or better. After a jump past that limit, it may not sell at all.
- **Guaranteed stops cost extra.** Some [[cfd]] brokers sell a guaranteed stop that fills at the stop price even after a gap. You pay a fee, often only if the stop is hit.
- **Backtests often leave it out.** A [[backtest]] that fills every stop at its price looks too good. Subtract an estimate from each trade, more for stop exits.

Next, see [[liquidity]] for what keeps slippage small, or [[stop-loss]] for where to place a stop.
