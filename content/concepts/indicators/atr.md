ATR (average true range) is an [[indicator]] that shows how far the price usually moves in one period, such as one day. It is a common measure of [[volatility]], drawn in a separate box (a panel) under the [[price-chart|chart]].

## True range

The plain range of a period is its high minus its low (see [[ohlc]]). This misses a [[gap]]: a jump from the previous close to the new open. The **true range** counts it. It is the largest of three numbers:

- high − low
- the distance from the high to the previous close
- the distance from the low to the previous close

To find a distance, subtract the smaller price from the larger one.

## Example: a gap day

On Monday a [[stock]] closes at $40. On Tuesday, after bad news, it opens at $35. Tuesday's high is $36 and its low is $34.50.

- High − low: $36 − $34.50 = $1.50
- High to previous close: $40 − $36 = $4
- Low to previous close: $40 − $34.50 = $5.50

The true range is $5.50. The plain range, $1.50, makes the day look calm, but at its low the price was $5.50 below Monday's close.

## From true range to ATR

ATR is the average true range over usually 14 periods, its length (see [[moving-average]]). Most apps use the average of ATR's inventor, J. Welles Wilder, which is like an exponential moving average. Each period, the new ATR is (13 × the last ATR + the new true range) / 14, so the newest period counts for only 1/14.

Say the ATR was $1 before the gap day. The $5.50 true range lifts it only to about $1.32. It then falls slowly. Some apps use a simple average, so apps can show slightly different values.

## Price units, not percent

ATR is in the price's own units (dollars for a US stock), not percent. An ATR of $1 on a $42 stock is about 2.4% a day; an ATR of $4 on a $400 stock is only 1%, so that stock is calmer. To compare two assets, divide ATR by the price.

ATR also changes with the [[timeframe]]. An hourly chart gives a much smaller ATR than a daily chart, so say which timeframe you mean.

## Stops and size

Traders often put the [[stop-loss]] a fixed number of ATRs below the buy price (2 or 3 is common), so that normal wobbles seldom reach it. This example uses four, a wider stop that gives the trade more room.

Take a $10,000 account that risks 1% ($100) per trade and buys at $42:

- **Calm stock**, ATR $1: stop at $38, $4 away. [[position-sizing|Position sizing]] gives 25 shares.
- **Jumpy stock**, ATR $2: stop at $34, $8 away. That gives 12 shares.

The stop follows the volatility, and the size follows the stop.

## Watch out

- **ATR shows size, not direction.** A high ATR can come in a rise or a fall.
- **ATR looks back.** It does not limit the next move. One gap can be several ATRs.

Next, see [[position-sizing]], then [[bollinger-bands]].
