MACD (moving average convergence divergence) is a momentum [[indicator]] built from two [[moving-average|moving averages]]: it shows if price moves get stronger or weaker. Gerald Appel created it in the late 1970s; the histogram was added in 1986. Apps draw it in a separate box (a panel) under the [[price-chart|chart]].

## The exponential moving average

MACD uses the **exponential moving average** (EMA), which weighs recent closes more: in a 12-day EMA the newest close counts for about 15%, against 1/12 (about 8%) in a 12-day simple moving average. So an EMA reacts sooner.

## Three parts

- **MACD line**: the 12-period EMA minus the 26-period EMA. The short average reacts faster, so the averages move apart (diverge) when the price speeds up and come together (converge) when it slows. Hence the name.
- **Signal line**: a 9-period EMA of the MACD line.
- **Histogram**: the MACD line minus the signal line, drawn as bars around zero. Bars are above zero (usually green) when the MACD line is higher, below zero (usually red) when lower.

The usual lengths are written "12, 26, 9".

## Example

In the [[trend]] example, a [[stock]] climbs from $40 to $58. On a day late in its rise from $44 to $53, its 12-day EMA is $52.40 and its 26-day EMA is $51.60.

| Part | Calculation | Value |
|------|-------------|-------|
| MACD line | 52.40 − 51.60 | 0.80 |
| Signal line | 9-day EMA of the MACD line | 0.60 |
| Histogram | 0.80 − 0.60 | 0.20 |

The MACD line is above zero: the short average is above the long one. It is also above its signal line, so the histogram is positive: the rise is still getting stronger. Late in a rise, the histogram often shrinks before the price turns. When the price dips toward $49, the MACD line drops toward its signal line and the histogram shrinks toward zero.

## Crossovers

- **Signal-line crossover**: the MACD line crosses above its signal line (the histogram turns positive). Many traders read it as a buy signal; a cross below, as a sell. These come sooner and more often than zero-line crossovers, so more are false.
- **Zero-line crossover**: the MACD line crosses zero, exactly when the 12-period EMA crosses the 26-period EMA. This common [[trend-following]] signal comes later.

Traders also watch for a different divergence: the price makes a higher [[peak-and-trough|peak]], but MACD makes a lower one. Some read it as an early sign of a turn, but often the trend continues (see [[rsi]]).

## No fixed limits

MACD has no upper or lower limit, unlike RSI (0 to 100), so it has no levels like RSI's 70 (overbought) and 30 (oversold).

## Watch out

- **It lags twice.** The MACD line comes from moving averages, and the signal line averages it again, so crossovers come late.
- **Sideways markets give false crossovers.** In a trading range (sideways between [[support-and-resistance|support and resistance]]), the lines cross back and forth near zero, each a possible small loss.
- **Values are in price units.** A MACD of 0.80 means 80 cents. A $400 stock has much larger values than a $53 stock, so you cannot compare MACD across stocks.

Next, see [[rsi]] for another momentum indicator, or [[trend-following]] for rules built on moving averages.
