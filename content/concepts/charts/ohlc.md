OHLC stands for open, high, low and close. These four prices sum up what the price did during one period, such as one hour or one day. That period is the chart's [[timeframe]]. Each [[candle]] on a [[price-chart]] is drawn from them.

## The four prices come from the trades

During a period, a [[stock]] may trade thousands of times (each trade is a buyer and a seller agreeing on a price). OHLC keeps only four of those prices:

- **Open**: the price of the first trade in the period.
- **High**: the highest price of any trade.
- **Low**: the lowest price of any trade.
- **Close**: the price of the last trade in the period.

## Example

To keep it short, say a stock traded only six times between 10:00 and 11:00:

| Time  | Price  |
|-------|--------|
| 10:00 | $50.00 |
| 10:12 | $50.40 |
| 10:25 | $49.80 |
| 10:41 | $50.90 |
| 10:53 | $50.60 |
| 10:59 | $50.70 |

The hour's OHLC is: open $50.00, high $50.90, low $49.80, close $50.70. The close is above the open, so this hour went up, and its candle would usually be green.

## Longer periods from shorter ones

You can build a longer period from shorter ones without looking at the trades again:

| Hour        | Open   | High   | Low    | Close  |
|-------------|--------|--------|--------|--------|
| 10:00–11:00 | $50.00 | $50.90 | $49.80 | $50.70 |
| 11:00–12:00 | $50.70 | $51.20 | $50.30 | $50.40 |
| 12:00–13:00 | $50.40 | $50.60 | $49.50 | $49.90 |

For the three hours together:

- **Open** is the first hour's open: $50.00.
- **High** is the highest of the highs: $51.20.
- **Low** is the lowest of the lows: $49.50.
- **Close** is the last hour's close: $49.90.

A daily candle is built the same way from all the day's hours. For a stock, though, the daily OHLC often leaves out trades before and after the regular session, so it can differ a little from that day's hourly candles.

## Where you meet it

- A **line chart** uses only the close. See [[line-vs-candle-chart]].
- Price data you download usually comes as columns named Open, High, Low and Close, often with a fifth, [[volume]]. Together they are called OHLCV.
- Most [[indicator|indicators]], numbers calculated from past prices or volume such as a [[moving-average]], use the close. Some, such as [[atr]], also use the high and low to measure how far the price swings.

## Watch out

- **OHLC loses the order.** You do not know if the high came before the low, or how the price moved between them.
- **The close is not final until the period ends.** On the newest candle, the "close" is just the latest price, and it changes with every trade.
- **The close depends on the market's hours.** A stock's daily close is the price at the end of the [[exchange|exchange's]] regular session; on most big exchanges a closing auction sets it. See [[trading-hours]]. A [[cryptocurrency]] trades all day, every day, so each app picks a time to end its day, often midnight UTC (London winter time).
- **The next open can differ from the last close.** If news comes out overnight, the stock can open far from yesterday's close. That jump is a [[gap]].

Next, see [[candle]] for how the four prices are drawn, or try the lesson [[reading-your-first-candle-chart]].
