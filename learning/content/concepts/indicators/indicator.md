An indicator is a number calculated from past prices or [[volume]], drawn as a line or bars on or under the [[price-chart]]. It sums up one thing about the recent price, such as its direction or how much it swings. It is recalculated for each period: each bar or candle on the chart, such as one day.

## Example

A 3-day [[moving-average]] of the close (the last price of each day) is one of the simplest indicators. Average each set of three days in a row:

| Day | Close | 3-day average |
|-----|-------|---------------|
| Mon | $10   |               |
| Tue | $11   |               |
| Wed | $12   | $11.00        |
| Thu | $11   | $11.33        |
| Fri | $13   | $12.00        |

Wednesday's value is (10 + 11 + 12) / 3 = $11.00. On Thursday, drop Monday's $10 and add Thursday's $11. The first two days have no value, because there are not yet three closes to average. Join the values and you get a line over the price.

## On the price or under it

- An **overlay** is drawn on top of the price, on the same price axis, because its values are price levels. A moving average and [[bollinger-bands|Bollinger bands]] are overlays.
- A **panel** is a separate box under the chart, with its own scale. It is used when the number is not a price level: a score, such as the [[rsi|RSI]]'s 0 to 100, or the size of a move, such as the [[atr|ATR]].

Volume bars under the [[candle|candles]] are not really an indicator (they are the raw volume, though many apps list them with the indicators), but they usually sit in a panel the same way.

## Settings

An indicator's main setting is its **length** (also called its period): how many bars it looks back over. The example uses 3. A short length follows the price closely and reacts fast; a long length is smoother and slower, so always say which length you mean.

## The main families

- **Trend**: shows the price's [[trend]]; the moving average is the basic one.
- **Momentum**: shows how strong recent moves were. See RSI and [[macd|MACD]].
- **Volatility**: shows the price's [[volatility]], how much it swings. See Bollinger bands and ATR.
- **Volume**: shows how much was traded. [[volume-profile|Volume profile]], for example, shows it at each price, drawn sideways.

## Watch out

- **It lags.** It adds no new information to the data it is built from (the past prices on the chart) and reacts only after the price has moved. In the example, Friday's jump to $13 lifts the average only to $12.
- **It is not a signal by itself.** An indicator is a tool inside a [[strategy]], a fixed set of rules for when to enter and exit trades. "RSI is high" means nothing until a rule says what to do, and a [[backtest]] shows if that rule worked.
- **More is not better.** RSI and MACD both measure momentum, so a chart with both often shows the same idea twice.

Next, see [[moving-average]] for the most common indicator in detail.
