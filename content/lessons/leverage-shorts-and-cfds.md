---
title: "Leverage, shorts and CFDs: when one trade can cost more than you planned"
summary: "Take the planned $42 trade short and with leverage, and see how margin, financing and gaps change what you can lose."
added: 2026-11-22
step: 6
builds_on: [leverage, cfd, short-selling, forex-pair, futures, stop-loss, position-sizing, gap, slippage, fees-and-commissions, drawdown, dividend, order-types]
---
The other lessons buy [[stock|shares]] with your own money, betting on a rise (going long). There a [[stop-loss]] keeps the loss close to the plan. This lesson changes two things, one at a time: a deposit that holds a bigger position (leverage), and a bet on a fall (going short). Here a trade means one position: a buy and the later sale that closes it, or for a short, a sale and the later buy.

The trade is the one from [[planning-one-trade]]: a $10,000 account risks 1%, $100, on a $42 stock with a stop at $38, $4 away. That gives 25 shares, a position value of $1,050.

Many EU [[broker|brokers]] advertise [[cfd|CFDs]]. They are common in the EU and UK but not offered to private traders in the US. EU rules make each CFD broker show a warning in its ads and on its website: "X% of retail investor accounts lose money when trading CFDs with this provider". X is the share of its private traders' accounts that lost money over the last 12 months, and it is often 70% or more. This lesson shows some of the reasons.

## Step 1: What does leverage do to a $10,000 account?

[[leverage|Leverage]] means holding a position worth more than your own money. With a CFD you put down only a deposit, the margin. The EU and UK limits for private traders include 5:1 for a single stock and 30:1 for major [[forex-pair|forex pairs]] such as EUR/USD. At 5:1 the broker holds 1/5 of the position value as margin.

At 5:1, the 25 shares need $210 of margin. The broker's app shows the other $9,790 as money you can still use. Use the whole account as margin, and it holds about $50,000 of the stock:

| Position | Shares | Position value | Margin at 5:1 | Loss at the $38 stop | Part of the account |
|----------|--------|----------------|---------------|----------------------|---------------------|
| Sized by the stop | 25 | $1,050 | $210 | $100 | 1% |
| All the margin used | 1,190 | $49,980 | $9,996 | $4,760 | 47.6% |

Against the $210 margin, the $100 loss looks like 48%; against the account it is still 1%. The full-margin loss of 47.6% is a [[drawdown]] that needs a gain of about 91% to get back.

At the full 30:1 for forex, $10,000 holds about $300,000 of EUR/USD, so a 1% price move changes the account by about 30%. Leverage does not set your loss; the position value and the price move do.

## Step 2: How is going short different?

[[short-selling|Short selling]] is selling borrowed shares, hoping to buy them back cheaper. A CFD short borrows nothing.

Now turn the trade around and go short: sell 25 shares at $42. The stop is now a buy stop above the price, at $46: an order that buys back once the price reaches $46 (see [[order-types]]). It mirrors the $38 stop: the stock's average daily move is $1, and the stop is 4 of those above the entry. 25 × $4 = $100, the same 1% risk.

- **The loss has no limit.** A price can fall only to zero, so the most a short can gain is the $1,050, but a price can rise without limit. The stop caps the loss only if the price trades at $46. If the stock closes at $44 and jumps overnight to $50, the buy stop fills around $50: $200 lost, not $100. With a CFD, that is almost all of the $210 margin, but still 2% of the account.
- **Holding it costs more, and it can be closed early.** On real shares you pay a borrow fee each day, and many CFD brokers add one too. You also pay the [[dividend|dividends]]: at 40 cents a quarter, 25 × 40 cents = $10 each quarter. The lender or the CFD broker can also close the short early, at a price you did not choose.

## Step 3: What does holding for weeks or months cost?

Back to the long trade from Step 1: 25 shares bought at $42, or 1,190 with all the margin used. A share you paid for in full has no interest to pay while you hold it. A leveraged position does: the broker charges [[fees-and-commissions|overnight financing]], interest for each night you hold it. The rate is usually a market interest rate plus the broker's markup; this example uses 7% a year, charged on every night, weekends included.

The interest is on the full position value, not on your margin:

- **25 shares**: 7% of $1,050 is $73.50 a year, about 20 cents a night.
- **1,190 shares**: 7% of $49,980 is about $3,500 a year, about $290 a month. Almost 3% of the account each month, even if the price does not move.

The planned trade was held about eight months and sold at $64 for a $550 gain. As a CFD held those eight months, financing takes about $49 of that, almost ten times the $5 commission. A short CFD usually pays less financing, or gets a small credit, but the borrow fee and dividends from Step 2 still apply.

For a hold of weeks or months, paying for the shares in full is often cheaper. In Czechia, shares held more than 3 years can be tax-free, but CFD gains are taxed however long you hold (see [[taxes-on-trading]]).

## Step 4: What does a gap do to a leveraged position?

A [[gap]] is a jump in price, for example overnight. Stay with the long trade (25 shares bought at $42, stop at $38). On Monday the stock closes at $40. After bad earnings (its quarterly profit), it opens on Tuesday at $35. The stop sells at the open, around $35. The $3 a share between the stop and the fill is [[slippage]].

| Position | Shares | Loss at $35 | Part of the account | Left |
|----------|--------|-------------|---------------------|------|
| Sized by the stop | 25 | $175 | 1.75% | $9,825 |
| All the margin used | 1,190 | $8,330 | 83.3% | $1,670 |

The 25-share trade loses $75 more than planned. The full-margin trade loses most of the account overnight; a drawdown of 83.3% needs a gain of about 500% to get back.

The broker's [[leverage|stop out]] does not help. In the EU and UK, a CFD broker must close one or more of a private trader's positions when the account value falls to half the required margin. After the gap, the account is far below that, but the stop out also closes at the market price, around $35. It stops a loss that grows step by step; it cannot act inside a gap.

A bigger gap can take more than the account. Below about $33.60, the 1,190 shares lose more than $10,000. EU and UK private CFD traders have negative balance protection: they cannot lose more than their account. [[futures|Futures]], a US stock margin account and CFD accounts with "professional client" status (which brings more leverage) usually have no such protection, and you owe the broker the difference.

## Step 5: How do you size so leverage stays a tool?

Size by the stop distance, not by the margin you have. The [[position-sizing]] formula does not change with leverage, or for a short:

**shares = (account × risk %) / distance from entry to stop**

$100 / $4 = 25 shares, long or short, shares or CFD. Then check only that the margin fits in the account.

Leverage also removes a brake. The position-sizing page tries a stop at $41.90, only 10 cents away: the formula says 1,000 shares, $42,000. With your own money, cash stops you at 238 shares. A CFD at 5:1 needs only $8,400 of margin, so the broker lets you open all 1,000. The loss at the stop is still about $100, but the gap to $35 costs 1,000 × $7 = $7,000.

So add a second check: what would a gap like the $35 open cost this position? Keep that loss to an amount you could take.

Leverage is a tool when it lets you hold a position you sized by the stop. One mini lot of EUR/USD is 10,000 euros; at 1.0850 it is worth $10,850, more than the account. Each pip (0.0001) is worth $1 here. A stop 100 pips below, at 1.0750 (4 times an average daily move of 25 pips), risks $100, 1%. At 30:1 it needs about $362 of margin. The position is about 1.1 times the account, not 30 times: leverage makes the position possible, and the stop and the size set the risk.

## Try it

Open the website of a CFD broker you have seen advertised and answer:

1. What share of its private traders' accounts lose money, according to its warning?
2. What margin does it ask for a stock CFD and for EUR/USD? Is that the EU limit, or less leverage?
3. What is its overnight financing rate for a long stock CFD? Work out the cost of holding 25 shares at $42 for three months.
4. Does it give negative balance protection? Does it offer to make you a "professional client"? Turning that down keeps the leverage limits and the protection.
5. Plan the short from Step 2: entry $42, buy stop $46, 1% of $10,000. How many shares, what margin at 5:1, and what does a gap to $50 cost?

For question 5: 25 shares, $210 of margin, and $200, twice the plan. Before you use leverage with real money, paper trade the plan and record each trade in a [[trading-journal]]. For a long hold without leverage, see the lesson [[building-a-simple-portfolio]].
