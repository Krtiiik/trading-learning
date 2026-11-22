An **option** is a contract that gives its buyer the right, but not the duty, to buy or sell an asset at a set price, on or before a set date. Options exist on [[stock|stocks]], [[index|indices]], [[futures]] and more.

## The parts of an option

- **Call**: the right to buy. Its buyer gains if the price rises enough.
- **Put**: the right to sell. Its buyer gains if the price falls enough.
- **Strike price**: the set price.
- **Expiry date**: the last day of the right.
- **Premium**: the option's price, paid by the buyer to the seller.
- **Contract size**: in the US, one stock option usually covers 100 shares. Premiums are given per share.

Using the right is called **exercising**. A seller is then **assigned**. With a stock option, they must sell the shares (call) or buy them (put) at the strike. Index options settle in cash.

**American-style** options, such as US stock options, can be exercised any day up to expiry; **European-style** ones, such as many index options, only at expiry. Most traders close before expiry rather than exercise.

## In, at or out of the money

A call is **in the money** when the asset's price is above the strike, **at the money** at the strike, and **out of the money** below it. For a put, it is the reverse.

The premium has two parts:

- **Intrinsic value**: what exercising now would pay (for a call, the price minus the strike, never below zero).
- **Time value**: the rest, paid for the chance that the price moves further your way before expiry. It is larger with more time left and when traders expect larger moves ([[volatility|implied volatility]]).

Time value shrinks toward expiry, fastest in the last weeks and at the money: this is **time decay**. At expiry, only intrinsic value is left.

## Example

You buy one call with a $45 strike on a $42 stock, with three months to expiry, for $1.50 per share: $1.50 × 100 = $150. The call is out of the money, so the whole premium is time value.

Your **break-even price** at expiry is the strike plus the premium, $46.50.

| Price at expiry | Value of the call | Result |
|-----------------|-------------------|--------|
| $40 | $0 | $150 loss |
| $50 | ($50 − $45) × 100 = $500 | $350 gain |

## Buyer and seller

The buyer can lose at most the premium. The seller keeps it and takes the risk:

- A seller of an **uncovered call** (without the shares) who is assigned must buy them at the market price, however high, and sell them at the strike, so the loss has no limit, as with [[short-selling|short selling]].
- A put seller can lose the strike minus the premium per share if the stock falls to zero.

[[broker|Brokers]] ask sellers for a margin deposit (see [[leverage]]).

## Watch out

- **Being right is not enough.** A stock that ends at $46 makes the call worth $100: still a $50 loss.
- **EU warrants and turbos are not exchange options.** A bank issues them to private traders and sets their prices. A turbo ends, usually with most or all of your money lost, if the price touches a set level.

Next, see [[volatility]] for what makes premiums larger.
