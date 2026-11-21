A peak is a local high point of a price: the price rose to it, then turned and fell. A trough is a local low point: the price fell to it, then turned and rose. "Local" means highest or lowest only near that point on the [[price-chart]], not in all the history.

## Not every candle high is a peak

Each [[candle]] has a high, the highest price of one period (see [[ohlc]]). Most candle highs are not peaks, because a nearby candle, before or after, went higher.

## How traders spot them

Choose a number N, for example 2. Traders call a peak found this way a **swing high**, and a trough a **swing low**:

- **Swing high**: a candle whose high is above the highs of the N candles before it and the N candles after it.
- **Swing low**: a candle whose low is below the lows of the N candles on each side.

## Example

A [[stock]] on a weekly chart, with N = 2:

| Week | High | Low | Close |
|------|------|-----|-------|
| 1    | $46  | $45 | $46   |
| 2    | $47  | $45 | $46   |
| 3    | $48  | $46 | $47   |
| 4    | $47  | $45 | $46   |
| 5    | $46  | $44 | $45   |
| 6    | $49  | $46 | $48   |
| 7    | $51  | $48 | $50   |
| 8    | $53  | $50 | $52   |
| 9    | $52  | $49 | $50   |

- **Week 3 is a peak at $48.** Its high is above the highs of weeks 1, 2, 4 and 5.
- **Week 5 is a trough at $44.** Its low is below the lows of weeks 3, 4, 6 and 7.
- **Week 8 is not a peak yet.** Its $53 high is the highest so far, but only one candle has come after it.

## You know a peak only later

At the end of week 3, nobody knew that $48 was a peak. You knew it at the end of week 5, after the price had fallen away from it. Every peak and trough is confirmed late: with N = 2, two candles late.

## Trends

Higher highs and higher lows make an uptrend; lower highs and lower lows make a downtrend (see [[trend]]). The peak at $48 and the trough at $44 match the first high and low after $40 in the trend page's example. $53 becomes the example's next peak if week 10's high stays below it. When the peaks stop at about the same level, and the troughs too, the price moves sideways between them. Levels where several peaks or troughs line up are [[support-and-resistance|support and resistance]].

## Practical use

- **Stop below the last trough.** The trough is confirmed at the close of week 7, and you buy at that close, about $50. A common choice is a [[stop-loss]] a little below the trough, at $43.50. Below $44, the higher lows would break.
- **The last peak as a target.** If you buy after a dip, a common first target is the most recent peak above your buy price, because the last rise stopped there.

## Watch out

- **Peaks depend on the [[timeframe]] and on N.** A peak on an hourly chart can be a wiggle inside one daily candle. A bigger N finds fewer, larger turning points but confirms them later.
- **Small wiggles are not real turning points.** Ignore turns smaller than the price's usual move per candle, its [[volatility]].

Next, see [[support-and-resistance]], then [[breakout]].
