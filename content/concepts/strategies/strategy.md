A strategy is a fixed set of rules for when to enter and exit trades: decided in advance and followed every time.

## What makes it a strategy

The rules are written down and precise enough that two people following them on the same chart get the same trades.

"Buy when the [[stock]] looks strong" is not a strategy: people read "strong" differently. "Buy on the first day the daily close is above the 100-day [[moving-average]]" is precise. The time to check and the order to use complete it (see [[entry-and-exit-rules]]).

## The parts

1. **What to trade**: which assets, on which [[timeframe]].
2. **When to enter**: the condition that opens a trade.
3. **When to exit**: the condition that closes it, at a gain or a loss, and a [[stop-loss]] as a safety net in a hard fall.
4. **How much**: [[position-sizing]], how many shares to buy.

## Example

A simple [[trend-following]] strategy:

- **What**: one stock, daily [[candle|candles]].
- **Enter**: buy on the first day the price closes above its 100-day average.
- **Exit**: sell on the first day it closes below.
- **Stop loss**: $4 below entry.
- **How much**: lose 1% of the account if the stop is hit.

On a $10,000 account, 1% is $100. The stock closes above its average at $42, and you buy. The stop goes at $38: $100 of risk at $4 per share allows 25 shares.

Months later it closes below the average at $64, and you sell: a gain of $22 per share, or $550 in total before [[fees-and-commissions|fees]] and the [[spread]].

Had it soon closed below the average, say at $41, you would sell for a $25 loss. The stop at $38 acts only on a sudden fall: you lose about $100, or more if the price [[gap|gaps]] past it.

## The main styles

- **Trend following**: ride a price while it keeps moving one way.
- [[mean-reversion|Mean reversion]]: bet that a price far from its usual level comes back.
- [[momentum|Momentum]]: buy the recent top risers among many assets, expecting them to stay ahead.
- [[breakout-trading|Breakout trading]]: enter when the price breaks past a [[support-and-resistance|support or resistance]] level.
- [[buy-and-hold|Buy and hold]]: buy and keep for years.
- [[rebalancing|Rebalancing]]: trade back to a target mix after prices shift it.

Buy and hold and rebalancing are long-term styles: their rules decide what to hold and when to trade back, not when to exit.

## Why fixed rules help

- **They can be tested** on past prices in a [[backtest]].
- **They remove in-the-moment emotion.** A rule decides before fear or hope can push you to sell winners early or hold losers too long.

## Watch out

- **Fitting the past is not proof.** Rules tuned until a backtest looks great may only fit chance moves in that data (overfitting) and fail later.
- **No strategy wins every trade.** What matters is how often it wins and its average result per trade: its [[win-rate-and-expectancy]].

Next, see [[entry-and-exit-rules]], then [[backtest]].
