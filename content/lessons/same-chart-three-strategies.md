---
title: "Same chart, three strategies"
summary: "Read one chart as a trend follower, a mean-reversion trader and a breakout trader, and see why each wins and loses in a different way."
added: 2026-11-22
step: 5
builds_on: [trend, peak-and-trough, support-and-resistance, breakout, volume, gap, moving-average, rsi, bollinger-bands, atr, trend-following, mean-reversion, breakout-trading, stop-loss, position-sizing, risk-reward, win-rate-and-expectancy, drawdown]
---
Three traders look at the same chart. The first follows trends, the second buys deep dips and expects the price to come back, and the third waits for a breakout. This lesson goes through their rules on one made-up chart and shows that each one wins on a different part of it. The eighteen ideas listed above each have their own short page; this lesson links them instead of explaining them again. Here a trade means one position: a buy and the later sale that closes it.

All three traders have a $10,000 account and risk 1%, $100, per trade. [[position-sizing|Position sizing]] turns that risk into a number of shares.

## Step 1: Is the price trending or in a trading range?

The chart is a daily chart of one [[stock]]. For months it moves sideways between about $45 and $55, with these [[peak-and-trough|peaks and troughs]]:

| Turning point | Price  |
|---------------|--------|
| Trough        | $45.20 |
| Peak          | $54.80 |
| Trough        | $44.70 |
| Peak          | $55.30 |
| Trough        | $45.40 |

Read them as the [[trend]] page does. In its uptrend, each high ($48, $53, $58) and each low ($40, $44, $49) is above the one before. Here the highs and lows are a mix: $55.30 is above $54.80, but $44.70 is below $45.20. There is no clear trend. The stock is in a trading range, the sideways area between [[support-and-resistance|support and resistance]]. The troughs make a support zone of $44.70 to $45.40, and the peaks a resistance zone of $54.80 to $55.30.

The indicators agree. The 100-day [[moving-average]] is flat at about $50, and the price crosses it again and again. The 20-day average, which the mean-reversion trader uses, is also $50. The stock has an [[atr]] of $1: it moves about $1 on an average day, gaps included.

Then the chart changes. One day the stock closes at $56, above the resistance zone, on about twice its usual [[volume]]. Over the next months it climbs to about $72. So the chart has two parts: a trading range, then an uptrend. Remember that you see the two parts only afterwards. On the day of each trade below, nobody knew which part came next.

## Step 2: What does the trend follower do?

The [[trend-following]] rule is the one from [[testing-a-trading-rule]]:

- **Enter**: buy on the first close above the 100-day average.
- **Exit**: sell on the first close below it.
- **[[stop-loss|Stop loss]]**: $4 (4 ATRs) below the entry, so $100 / $4 = 25 shares.

In the trading range, the price rises through the flat average and closes at $51: buy. It goes on to $55, turns, and a few days later closes at $49: sell. That is −$2 × 25 = −$50. The rule bought after the swing up had started and sold after the swing down had started, so it kept none of the swing's gain: it got in late and out late. Each crossing of the flat average costs about the same. None of these losses reaches the stop.

After the last trough at $45.40, the price again closes at $51, and the rule buys again. This time it does not come back. It breaks out at $56 and climbs to $72, and the average rises behind it. Months later the price closes below the average at $63: sell. That is +$12 × 25 = **+$300**. The two full swings in the trading range gave two such losses, $100 in all: the one win paid for them three times.

## Step 3: What does the mean-reversion trader do?

The [[mean-reversion]] rule:

- **Enter**: buy on a close 4 ATRs or more below the 20-day average.
- **Exit**: sell on the first close at or above the average.
- **Stop loss**: 4 ATRs below the buy price.

Two more indicators measure the same distance. The [[bollinger-bands|Bollinger bands]] use the standard deviation of the last 20 closes (how far they usually are from their average), here $2, so the lower band is $50 − 2 × $2 = $46 and the upper band $54. [[rsi]] scores recent rises against recent falls; below 30 is called oversold.

In the trading range, the stock falls to a close at $46. That is 4 ATRs below the $50 average, at the lower band, with an RSI of 25. All three say the same thing: the price is far below its usual level. Buy 25 shares with a stop at $42, $4 below. (The support-and-resistance page puts its stop at $43.50 instead, a little more than one ATR below the support zone: less room, less risk per share.) The price dips a little further, into the support zone, then turns up and closes back at about $50: sell, +$4 × 25 = **+$100**. In practice the win is often a little smaller, because the falling closes pull the average, and so the exit, down. In the trading range this can happen again at each trough.

In the uptrend after the breakout, the rule finds nothing to do. The price stays far above its 20-day average, so no close is 4 ATRs below it. RSI can stay above 70 for weeks, and the price stays near the upper band for weeks while the band rises with it. A trader who also used [[short-selling|short selling]] at each touch of the upper band would lose again and again.

The rule fails when the price breaks out downward instead, through support. Say the stock had closed below the support zone a few days after the buy at $46 and kept falling. The stop at $42 sells: −$100. After a [[gap]], a jump in price, for example overnight, it can sell well below $42 and lose more. Traders call this catching a falling knife.

## Step 4: What does the breakout trader do?

The [[breakout-trading]] rule:

- **Enter**: buy on a close above the resistance zone. A [[wick]] above the zone with a close back inside does not count: the close beyond the zone is the confirmation (see [[breakout]]).
- **Stop loss**: $54, 80 cents below the resistance zone. The risk is $2 per share, so $100 / $2 = 50 shares.
- **Target**: the trading range is about $10 high (from about $45 to about $55); added to $55, that gives $65. The target is an exit: a sell order waits there.

In the trading range, the breakout trader does nothing. The rises to $54.80 and $55.30 stopped inside the zone, with no close above it.

On the day of the $56 close, on twice the usual volume, the trader buys 50 shares. The close is 70 cents beyond the zone, more than half an ATR, so it also passes the stricter test on the breakout page. Later the price dips to about $55.20, a retest of the old resistance, and turns up again. It reaches $65, and the sell order closes the trade: +$9 × 50 = **+$450**.

The rule fails on a false breakout. If the price had closed back below $54.80 and fallen to the stop at $54, the trade would have lost $100. Many breakouts fail this way, so the stop is hit often.

## Step 5: Why does each win and lose differently?

| | Trend following | Mean reversion | Breakout trading |
|---|---|---|---|
| Wins in | a long trend | a trading range | the start of a trend |
| Loses in | a trading range | a new trend against it | a false breakout |
| A win here | +$300 | +$100 | +$450 |
| A loss here | −$50 | −$100, more after a gap | −$100 |
| Win rate | often low | often high | often low |

A [[gap]] can jump past any of the three stops; the gap loss below uses mean reversion because it buys while the price is falling.

All three risk the same $100 at the stop. What differs is how often they win and how big the wins are. [[win-rate-and-expectancy|Expectancy]] puts the two together: win rate × average win − loss rate × average loss.

- **Breakout trading**, winning 3 trades in 10: 0.3 × $450 − 0.7 × $100 = $135 − $70 = **+$65 per trade**. The [[risk-reward]] of 4.5 to 1 means it breaks even at about 1 win in 5.5, or 18%, before costs and if every win reaches the target.
- **Mean reversion**, winning 6 in 10: 0.6 × $100 − 0.4 × $100 = **+$20 per trade**. Now make one of the four losses a $300 gap loss. The average loss becomes $600 / 4 = $150, and 0.6 × $100 − 0.4 × $150 = **$0**. One bad loss took all the gain.

These are made-up rates, before costs. Costs take a few dollars from every trade, win or lose, so they hurt the small wins of mean reversion most.

The strategies also feel different. Trend following and breakout trading bring long runs of small losses and wait for a rare large win; many traders give up just before it comes. Mean reversion brings long runs of small wins, and then one loss that takes many of them back. The losing runs, and the one big loss, pull the account down from its high: its [[drawdown]].

No rule knows in advance which part of the chart comes next. Step 1 tells you only what the price has done so far. So pick one rule, test it on past prices with a [[backtest]], and expect to sit through the part of the chart where it loses.

## Try it

Open the daily chart of a stock you follow and answer:

1. Mark the last five peaks and troughs. Is the price in a trend or in a trading range?
2. Is the 100-day average rising, falling or flat? What would the trend follower do today?
3. How many ATRs is the last close from the 20-day average? Where are the Bollinger bands, and what is the RSI? Would the mean-reversion trader buy?
4. Where are the support and resistance zones? What close would the breakout trader buy on, where would the stop go, and how many shares give $100 of risk?
5. For each of the three traders, what would the price have to do next to make them lose?

To test one of these rules on past prices, see [[testing-a-trading-rule]]; to plan one trade from entry to exit, see [[planning-one-trade]]. To pick one and stick with it, see [[trading-journal]] and [[trading-psychology]].
