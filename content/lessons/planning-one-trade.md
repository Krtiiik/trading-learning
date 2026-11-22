---
title: "Planning one trade, from entry to exit"
summary: "Take one trade from the written rule to the sale: stop, size, target, costs, and a look back at what happened."
added: 2026-11-22
builds_on: [entry-and-exit-rules, trend-following, moving-average, order-types, stop-loss, volatility, atr, position-sizing, risk-reward, spread, fees-and-commissions]
---
This lesson follows one trade from the first idea to the sale. Here a trade means one position: a buy and the later sale that closes it. It links the eleven ideas listed above rather than explaining them again.

The trade: a $10,000 account buys a calm [[stock]] (one that moves little each day) at $42.

## Step 1: What exactly will you do?

Write the rule before you buy, not while you watch the price. The [[entry-and-exit-rules]] page explains its three parts: the condition, the time and the order.

This trade uses the [[trend-following]] rule, with the 100-day [[moving-average]] (the average of the last 100 daily closes):

1. **Entry**: a few minutes before the close (16:00 New York time, usually 22:00 in Prague), check the price. On the first day it is above the average, buy with a market order.
2. **Signal exit**: on the first day it is below the average, sell the same way.
3. **Stop loss exit**: a sell stop order below the entry. Step 2 sets its price.

Step 4 decides whether the target is an exit too. The [[order-types]] page explains each order. When one exit closes the trade, cancel the other orders.

## Step 2: Where are you wrong?

A [[stop-loss]] is an order that sells automatically if the price falls to a level you chose. Put it where the price shows that your idea failed, not where the loss feels small. Normal wobbles must not reach it.

This lesson measures the stop in ATRs. The [[atr]] is the price's average daily move; for this stock it is $1. Four ATRs below $42 gives a stop at $38 (2 or 3 is also common; four gives more room). That is the same $4 stop the entry-and-exit-rules page uses.

## Step 3: How many shares?

Only now choose the size. [[position-sizing|Position sizing]] works back from the loss you accept:

- 1% of $10,000 is $100.
- $42 − $38 is $4 of risk per share.
- $100 / $4 = 25 shares, a position value of $1,050.

The jumpy $42 stock on the [[volatility]] page has an ATR of $2, so four ATRs put its stop at $34, $8 away: $100 / $8 = 12.5, rounded down to 12 shares. The wider stop gives fewer shares, and the money at risk stays about $100.

## Step 4: Is the trade worth it?

Set a target, the price where you plan to sell for a gain, and check the [[risk-reward]]. A target of $54 is $12 above the entry, three times the $4 risk: 3 to 1. At 3 to 1 you need to win only 1 trade in 4 to break even; at 1 to 1, 1 in 2. If the ratio is low, skip the trade. Do not move the stop closer to make the ratio look better.

Also write into the rule what happens at $54: a sell limit order can sell there, or the target is only a check. This rule uses $54 only as a check: no order waits there, and the signal exit closes the trade.

## Step 5: What does it cost?

Costs come off every gain and add to every loss:

- **The [[spread]]**, the gap between the best price buyers offer and the best price sellers want. A large US stock often has a 1-cent spread, so the round trip (buying, then selling) costs about 25 cents for 25 shares.
- **Commission**: at $2.50 per order, $5 for the round trip (see [[fees-and-commissions]]).

Leaving out the small spread, the $5 commission makes the plan $295 of possible gain against $105 of possible loss: about 2.8 to 1, not 3 to 1.

If your account is in CZK or EUR, the [[broker]] also converts your money into dollars, often for 0.25% to 1.5%: about $2.60 to $16 on the $1,050 purchase, and again on the sale unless you keep the dollars (the full walk-through is in [[what-your-first-order-costs]]). The exchange rate can also move while you hold, so your gain in koruna differs: see [[currency-risk]].

The stop is not a guaranteed price either. After a [[gap]], a jump in price, for example overnight, the stop can sell well below $38.

## Step 6: What happened, and what do you write down?

The price passed $54 and kept rising. No order waited at $54, so the trade stayed open, as the rule said. Months later the price closed below its average, and the signal exit sold the shares at $64: a gain of $22 per share, $550 before costs and $545 after the $5 commission. That is 5.5 times the $100 risk before costs, against the planned 3 to 1.

Keep the plan and the result apart: a good result does not prove a good plan. Then check: did you follow the rule? If the rule said to sell at $54 and you held on, the extra gain came from breaking the plan, and next time that can turn into a loss.

Record each trade: the rule, the entry, the stop and how you set it, the size, the target, the exit and which one closed the trade, the costs, the result as a multiple of the planned risk (here, 5.5 before costs), and whether you followed the rule. Over many trades, these records give your [[win-rate-and-expectancy|win rate and expectancy]].

The sale also makes the gain realised, and that is where tax can apply. The rules differ by country. In some, such as the US and Czechia, they also depend on how long you held: see [[taxes-on-trading]]. A Czech trader counts the gain in CZK, so keep the exchange rates in your record too.

## Try it

Pick a stock you follow and plan one trade on paper, without buying:

1. Write the entry and exit rules in three lines.
2. Find its daily ATR and put the stop four ATRs below today's price.
3. Work out the shares for 1% of a $10,000 account.
4. Set a 3 to 1 target, then take $5 of costs off the possible gain and add $5 to the possible loss. What is the ratio now?

Before trading a rule, test it on past prices: see [[testing-a-trading-rule]].
