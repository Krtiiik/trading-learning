A moving average is the average price over the last few periods, recalculated every period. Drawn as a line over the [[price-chart|chart]], it smooths out small zigzags so the bigger picture is easier to see. It is the simplest and most widely used [[indicator]].

## How it is calculated

Take the [[ohlc|closing prices]] of the last N periods, add them up and divide by N. When a new period closes, drop the oldest price, add the newest and calculate again. The average "moves" along with the chart.

The N is called the **length** (apps often label it "period"). A 20-day moving average uses the last 20 daily closes.

This plain version is the **simple** moving average (SMA). A variant called the **exponential** moving average weighs recent prices more, so it lags a little less.

## Example

The last five daily closes are $10, $11, $12, $11 and $13. The 5-day moving average today is (10 + 11 + 12 + 11 + 13) / 5 = $11.40. Tomorrow the price closes at $14: drop the $10, add the $14, and the average becomes $12.20.

## Short versus long

- A **short** average (say 10 periods) follows the price closely and reacts fast, but it also reacts to noise.
- A **long** average (say 200 periods) is smooth and slow. It shows the long-term [[trend]] but turns late.

## What people use it for

- **Seeing the trend.** Price above a rising average usually means an uptrend; below a falling one, a downtrend.
- **Signals.** When the price, or a short average, crosses a long average, many traders read it as a change of direction. This is the core of many [[trend-following]] rules.

## Watch out

A moving average is built from past prices, so it always lags. In a market that moves sideways it crosses back and forth and gives many false signals.

Next, see [[trend-following]] for how traders build rules around moving averages, or [[bollinger-bands]] for bands built around an average.
