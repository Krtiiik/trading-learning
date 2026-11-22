A **futures contract** is an agreement to buy or sell an asset at a set price on a set future date. Futures trade on an [[exchange]], such as the CME in the US or Eurex in Germany. Each contract has an **expiry date** and a size set by its **multiplier**: the money value of a one-point move.

## Buyer and seller

- The **buyer** is **long**: they gain when the price rises.
- The **seller** is **short**: they gain when the price falls. Unlike [[short-selling|short selling]] a [[stock]], you borrow nothing.

## Margin

Instead of the full contract value, you put down **margin**: a deposit that shows you can pay your losses. Unlike a stock [[broker|broker's]] margin account, nobody lends you money (see [[leverage]]), so you pay no interest.

- **Initial margin**: the amount you need to open one contract.
- **Maintenance margin**: the lower amount your account must stay above. If it falls below, you get a margin call: add money back up to the initial margin, or close the position. Otherwise, the broker closes it.

## Daily settlement

Each trading day, the exchange sets a settlement price (that day's official price). Your broker pays each day's gain into your account and takes each day's loss out.

## Example

The **Micro E-mini S&P 500** follows the S&P 500 [[index]]. Its multiplier is $5 per index point. With the index at 6,000, the contract value is 6,000 × $5 = $30,000. Eurex's Mini-DAX and Micro-DAX futures work the same way, at €5 and €1 per DAX point.

Assume margins of $2,500 (initial) and $2,250 (maintenance). Your leverage is $30,000 / $2,500 = 12:1. You buy one contract at 6,000 and deposit $2,500.

| Day | Settlement price | Change | Paid in or out | Account |
|-----|------------------|--------|----------------|---------|
| 1 | 6,020 | +20 points | +$100 | $2,600 |
| 2 | 5,940 | −80 points | −$400 | $2,200 |

On day 2, the account falls below $2,250: a margin call. You add $300 or close. The price fell only 1% from your entry, but you lost 12% of your deposit.

## Expiry and rolling

Most traders close before expiry. At expiry, index futures settle in cash: the last gain or loss is paid. Some [[commodity]] futures, such as oil, settle by delivery of the goods; brokers usually close private traders' positions first.

To stay in, traders **roll**: they close the contract that ends soon and open the next one. When later contracts cost more, each roll loses a little: see [[commodity]].

## Watch out

- **You can lose more than your margin.** A fast move or a weekend [[gap]] can take more than your deposit, and you owe the difference. The EU's leverage caps and negative balance protection cover [[cfd|CFDs]], not futures.
- **One contract can be too big.** A $30,000 contract on a $5,000 account is leverage of 6:1. Use [[position-sizing]] and a [[stop-loss]].
- **The futures price is not the asset's price.** It includes the cost of carry until expiry (see [[commodity]]; for an index, interest minus [[dividend|dividends]]), so it is usually a little above or below.

Next, see [[leverage]] for how margin enlarges gains and losses.
