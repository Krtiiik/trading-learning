Trend following is a [[strategy]] built on one idea: prices that have started moving in a direction often keep moving that way for a while. So you buy when a price is rising, and sell what you hold (or stay out) when it is falling.

You do not try to predict where the [[trend]] starts or ends. You wait until it is visible, ride it, and leave when your exit rule says it has turned.

## A simple version

Many trend-following strategies are built from a [[moving-average]], the average of the closing prices over a set number of recent days, recalculated every day:

- **Enter**: buy on the first day the price closes above its 100-day moving average.
- **Exit**: sell on the first day it closes below.

The 100 is the average's length: it looks back over the last 100 daily periods. A longer length gives fewer, later signals. A shorter one reacts sooner, but also gives more false signals.

Those are the [[entry-and-exit-rules]]. Adding a [[stop-loss]], an order that sells automatically if the price falls to a level you chose, helps limit how much a single trade can lose (in a fast drop it can sell lower: [[liquidity|slippage]]).

## What it feels like

Most trades are small losses: the price crosses the average, then turns back. A few trades catch a long trend and make large gains. The few big winners pay for the many small losers, so the [[win-rate-and-expectancy|win rate]] is often below 50%, and the strategy can still make money overall if the winners are big enough.

## Example

A [[stock]] drifts down to about $40 and stays below its 100-day average for months. Then it climbs, and on the first close above the average, at $42, you buy. It rises for half a year to $70. The dips along the way stay above the average, until it finally closes below it at $64. You sell: a gain of $22 per share before costs, even though you missed both the bottom and the top.

## Watch out

- **Sideways markets cost money.** When the price moves back and forth with no clear trend, it crosses the average again and again, and each false signal is a small loss. You need patience through those stretches. A [[backtest]], which runs the rules on past prices, can show how long such stretches lasted in the past and how much they cost.
- **On a winning trade, you always give some back.** The exit comes only after the trend has turned. In the example the price reached $70, but you sold at $64.

Next, see [[entry-and-exit-rules]], [[breakout-trading]], which feels much the same, [[momentum]], which compares many assets with each other, or [[mean-reversion]] for the opposite approach.
