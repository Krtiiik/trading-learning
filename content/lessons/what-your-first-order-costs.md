---
title: What your first order really costs
summary: Follow one buy order from your app to the market and back, and add up every cost on the way.
added: 2026-11-22
step: 2
builds_on: [stock, broker, exchange, order-types, bid-and-ask, spread, liquidity, volume, trading-hours, fees-and-commissions, currency-risk]
---
This lesson follows one order: you buy 100 shares of a US [[stock]] priced near $50, and later sell them again. Each step answers one question, and at the end you add up what the round trip (buying, then selling) cost. Each idea has its own short page if you want to look it up.

## Step 1: Who carries out your order?

You cannot send an order to an [[exchange]] yourself. Your [[broker]] passes it on to an exchange or another market, and holds your cash and shares. So check the broker before your first order: in Czechia, look it up in the register of the ČNB (the Czech National Bank); elsewhere in the EU, look in your national regulator's register. A firm that is not in the ČNB register may not offer you investment services in Czechia. An EU broker from another country is also listed there, as a foreign firm. The register also shows the broker's home country, and that country's compensation scheme covers you if the broker fails and cannot give back your cash and shares, up to a limit. It does not pay for losses on your trades.

In the US, large trading firms often pay brokers to send them small orders, which the firms then fill themselves ([[fees-and-commissions|payment for order flow]]). The EU bans this, so EU brokers send orders elsewhere: often to a German market such as Tradegate or gettex, not to New York. That matters for the hours (Step 4) and the currency (Step 5).

This lesson follows an order that goes to a US exchange, in dollars. On a German venue the book is in euros, but it works the same way.

## Step 2: What does the order book show?

Open the stock's order book: the list of waiting orders. Its best prices are the bid, the highest price a buyer offers, and the ask, the lowest price a seller wants (see [[bid-and-ask]]).

| Side | Price  | Shares waiting |
|------|--------|----------------|
| Sell | $50.03 | 200            |
| Sell | $50.02 | 100 ← ask      |
| Buy  | $49.98 | 400 ← bid      |
| Buy  | $49.97 | 150            |

Read three things from it:

1. **The ask, $50.02**, is what you pay with a market buy. **The bid, $49.98**, is what you get with a market sell.
2. **The [[spread]]**, the gap between the best price buyers offer and the best price sellers want, is 4 cents. The mid price, halfway between, is $50.00.
3. **The depth.** Only 100 shares wait at the ask. A bigger order fills partly at the next, worse price.

## Step 3: Market order or limit order?

The [[order-types]] page explains both. On this book:

- **A market buy for 100 shares** fills at once: 100 × $50.02 = $5,002. That is $2 more than the value at the mid price ($5,000): half the spread, 2 cents, on each of the 100 shares.
- **A market buy for 150 shares** takes the 100 shares at $50.02 and 50 at $50.03. Paying more than the best price is [[slippage]].
- **A buy limit at $49.98** pays no spread if it fills. But it waits behind the 400 shares already at the bid, and if the price rises, it may never fill.

For a first order in a large, busy stock, a market order is simple. A limit order at the ask, $50.02, gives the same fill and protects you if the price jumps just before your order arrives.

## Step 4: When does the market cost extra?

The book above has good [[liquidity]]: many shares wait near a narrow spread. Two things make it thinner.

- **A small or rarely traded stock.** Low [[volume]], few shares traded each day, usually comes with fewer waiting orders and a wider spread.
- **The hour.** The US regular session runs 9:30–16:00 New York time (15:30–22:00 CET; an hour earlier for two or three weeks in March and about one week around the end of October; see [[trading-hours]]). Some German venues, such as gettex, stay open until 23:00 CET. At 22:30 CET, the New York regular session has ended, so few orders wait. The bid might be $49.90 and the ask $50.10: a 20-cent spread, so the round trip costs $20 in spread instead of $4. The same happens in the morning, before New York opens.

So trade US stocks while New York is open, and use limit orders when the book is thin.

## Step 5: What does the whole round trip cost?

You have a CZK account. You buy 100 shares at $50.02 during US hours and sell them later at the bid, $49.98: the bid and ask have not changed, so the stock did not move. Your broker charges, for example, $2.50 per order and 0.5% for each currency conversion, CZK to dollars and back. A dollar costs 21 CZK, and the rate does not change.

| Cost | How it is counted | Dollars |
|------|-------------------|---------|
| Spread | $5,002 paid − $4,998 received | $4.00 |
| Commission | 2 orders × $2.50 | $5.00 |
| Conversion when buying | 0.5% of $5,002 | $25.01 |
| Conversion when selling | 0.5% of $4,998 | $24.99 |
| **Total** | | **$59.00** |

That is $59 × 21 = 1,239 CZK, or about 1.2% of the $5,000 you put in. The stock must rise about 59 cents a share before you break even. The spread is the smallest part; the currency conversion is the largest.

With a EUR account it works the same way: you convert euros to dollars and back. Some brokers let you hold dollars in your account, so you convert once, not on every order. On a German venue, the stock is priced in euros: a CZK account then converts koruna to euros, and a EUR account pays no conversion fee. Either way, the stock's euro price still moves with the dollar's exchange rate. A change in the exchange rate is a separate risk on top of these costs: it can add to your result or take away from it (see [[currency-risk]]).

## Try it

Open your broker's price list and the order book of one stock you might buy, and answer:

1. Is your broker in the ČNB register? If it is a foreign EU broker, which country is it from?
2. What are the bid, the ask and the spread right now, and how many shares wait at the ask?
3. What do one commission and one currency conversion cost?
4. Add up one round trip for 100 shares, as in Step 5. How far must the price rise before you break even?

If the total surprises you, compare brokers, or trade less often: each round trip pays these costs again. Next, see [[taxes-on-trading]] for what happens to your gain after that, or [[planning-one-trade]] to take one trade from entry to exit.
