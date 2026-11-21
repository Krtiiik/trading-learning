Bollinger bands are an [[indicator]] made of three lines on the [[price-chart|chart]]: a [[moving-average]] in the middle (the middle band), one band above it and one band below it. The bands widen when the price swings more and narrow when it is calm.

## Standard deviation

Each band is a number of **standard deviations** from the average. A standard deviation measures how far the closes usually are from their average: small when they stay near it, large when they swing far. Your app calculates it.

Bollinger bands use the standard deviation of the closing prices themselves, in dollars. The [[volatility]] page lists another one, of daily percentage changes. Both grow when the price swings more.

## The usual setting

| Line | Usual setting |
|------|---------------|
| Middle band | simple moving average of the last 20 closes (a length of 20) |
| Upper band | middle band + 2 standard deviations of the same 20 closes |
| Lower band | middle band − 2 standard deviations |

Most closes stay inside the bands, often about 9 in 10. Some books say 95%, but that number assumes the closes scatter at random in a neat bell shape. Real prices follow trends and sometimes jump, so the share is often lower. Count the closes inside the bands on your own chart.

## Example

A [[stock]] has moved sideways between about $45 and $55 for months. Its 20-day average is $50, and the standard deviation of the last 20 closes is $2. The upper band is $50 + 2 × $2 = $54, and the lower band is $50 − 2 × $2 = $46.

In the [[mean-reversion]] example, a trader buys this stock on a close at $46, 4 [[atr|ATRs]] (average daily moves of $1) below the average. That buy is at the lower band, and the exit at the average is the middle band.

## Width follows volatility

A bigger standard deviation means wider bands. If our stock's standard deviation rose from $2 to $3, the bands would move out to $44 and $56.

A **squeeze** is a time when the bands are much narrower than usual. It often comes before a bigger move, but it does not show the direction: the price can [[breakout|break out]] up or down.

## A touch is not a signal

A close at a band shows that the price is far from its average, not that it will turn back. In a sideways market, it often does. In a strong [[trend]], the price can stay near one band for weeks while the band moves with it: the upper band in a rise, the lower band in a fall. Traders call this **walking the band**. A trader who buys at each touch of the lower band in a downtrend loses again and again.

## Watch out

- **The bands look back.** They lag like the moving average and do not limit the next move: a [[gap]] can jump far past a band.
- **A band is not a rule by itself.** Use it inside clear [[entry-and-exit-rules]], with a [[stop-loss]], and test them with a [[backtest]].
- **Settings change the bands.** Always say which length and how many standard deviations you use.

Next, see [[mean-reversion]] for a strategy that buys far below the average, or [[atr]] for another measure of volatility.
