---
title: "Does this rule work? From idea to tested strategy"
summary: Turn a vague idea into exact rules, backtest them, and read the results without fooling yourself.
added: 2026-11-22
step: 4
builds_on: [strategy, entry-and-exit-rules, moving-average, trend-following, stop-loss, position-sizing, backtest, win-rate-and-expectancy, drawdown, fees-and-commissions]
---
This lesson takes one trading idea from a vague hunch to a tested [[strategy]]. Each step answers one question. The ten ideas listed above each have their own short page; this lesson links them instead of explaining them again. Here a trade means one position: a buy and the later sale that closes it.

## Step 1: Is the idea a rule yet?

"Buy when the [[stock]] looks strong" is not a rule: two people read "strong" differently, so they make different trades, and no test can decide what it means. Make every part exact (see [[entry-and-exit-rules]]):

- **What**: one stock, daily [[candle|candles]].
- **Enter**: on the first day the price closes above its 100-day [[moving-average]], buy.
- **Exit**: on the first day it closes below, sell.
- **Safety net**: a [[stop-loss]], an order that sells automatically if the price falls to a level you chose, $4 below entry (four times the stock's average daily move, as in [[planning-one-trade]]).
- **How much**: [[position-sizing]] so a hit stop loses 1% of the account. On $10,000 that is $100, and $100 / $4 = 25 shares.
- **When and how**: check the price a few minutes before the close, treat that price as the close, and buy or sell with a [[order-types|market order]] (it trades at once). Your price, and on a close call even the signal, can differ a little from the backtest, which uses the exact close.

This is the simple [[trend-following]] rule. Now two people with the same chart get the same trades, and a computer can too.

## Step 2: What would it have done?

Run the rules on past prices: a [[backtest]]. Go through the data one day at a time, using only what was known on that day, and write down each trade. Suppose the test finds 10 trades on a $10,000 account (the same example the backtest page uses):

| Trade | Result | Account |
|-------|--------|---------|
| 1 | +$150 | $10,150 |
| 2–5 | −$25, −$40, −$30, −$25 | $10,030 |
| 6 | +$550 | $10,580 |
| 7–9 | −$50, −$20, −$30 | $10,480 |
| 10 | +$300 | $10,780 |

Three wins make $1,000 and seven losses cost $220: +$780, or 7.8%, before costs. That total is only the start. The next two steps ask how it got there.

## Step 3: How often does it win, and how much per trade?

Read the [[win-rate-and-expectancy]]:

- **Win rate**: 3 of 10, or 30%.
- **Average win**: about $333. **Average loss**: about $31.
- **Expectancy**: $78 per trade before costs, the same as $780 / 10.

Losing 7 times in 10 feels bad, but it is normal for trend following: the few big wins pay for the many small losses. A rule is not good because it wins often. It is worth testing further only if its expectancy stays positive after costs. Note too that each loss was far smaller than the $100 the stop risked: the signal exit sold first.

## Step 4: How bad did it get on the way?

Now read the [[drawdown]], the fall from the account's high:

- **Maximum drawdown**: trades 2 to 5 took the account from $10,150 to $10,030, a fall of $120 (1.18%) before costs.
- **Time under water**: four trades passed before trade 6 made a new high.

These numbers are small, but they are only end-of-trade values from ten trades. Inside a trade the account can fall further, and real trading usually brings a deeper and longer drawdown than the test showed. Ask yourself: could you keep following the rules through four, or fourteen, losses in a row?

## Step 5: Is the test fooling you?

Check three things before you believe any result:

1. **Overfitting.** Did you try many lengths and stops (a 97-day average, a stop at $3.80) and keep the best? Then the rules may fit chance moves. Tune on the first years of data only, then run the rules unchanged, once, on the last years.
2. **Look-ahead bias.** Did the test use anything not known at the time? A rule that checks the day's close but buys at that day's open could never be traded.
3. **Missing costs.** Add the [[spread]], [[fees-and-commissions|fees]] and [[slippage]]. At $5 per round trip ($2.50 per order, as in [[planning-one-trade]]), the total falls to +$730, the expectancy to about $73 per trade, and the maximum drawdown grows to $140.

If your account is in CZK or EUR, the result in your own money differs from the dollar result, because the exchange rate moves too: see [[currency-risk]]. Your broker also takes a [[fees-and-commissions|currency conversion fee]] each way, often 0.25% to 1.5%. On a position of about $1,050 that is about $5 to $32 per round trip, large next to the $73 expectancy left after commission. [[what-your-first-order-costs]] adds up these costs for one order.

## Step 6: Does it work with real money?

A backtest is still not real trading. First, many [[broker|brokers]] offer a demo account where you trade with pretend money; this is called paper trading (see [[trading-journal]]). It checks that you can follow the rules on time, every day, but it hides real fills (the prices your orders actually trade at) and [[trading-psychology|real fear]].

Then trade the rules live, but small: risk much less per trade than the 1% the test used, for example 0.25%. On $10,000 that is $25, so 6 shares with the $4 stop. Write down every trade and compare it with what the backtest would have done on the same days. If your real fills are worse, or you skip signals, fix that before you raise the risk. The backtest had only ten trades, and your first live trades will be fewer still, so give it time; a short run of losses alone does not prove the rule is broken.

## Try it

Write down one trading idea you have and answer:

1. Can two people follow it and get the same trades? If not, which word is vague?
2. After costs, is the expectancy still positive?
3. Could you sit through a drawdown twice as deep and twice as long as the test's maximum?
4. Did you test it on years you did not use to tune it?

Once a rule passes these steps, see [[planning-one-trade]] to take one trade from entry to exit.
