RSI (relative strength index) is an [[indicator]] that compares the size of recent rises with the size of recent falls and gives a score from 0 to 100. Wilder introduced it in 1978. Apps draw it in a separate box (a panel) under the [[price-chart|chart]].

## How it is built

RSI looks at the change from each close to the next. It usually looks back over 14 periods, its length (see [[moving-average]]).

1. If a period (a day on a daily chart) closes above the one before, the rise is its gain. If it closes below, the fall is its loss, kept positive: a 30-cent fall is a loss of 30 cents. A rising day has a loss of 0, and a falling day a gain of 0.
2. Average the gains over the length, and average the losses.
3. Divide: RS (relative strength) = average gain / average loss.
4. Turn RS into a score: RSI = 100 − 100 / (1 + RS).

Most apps use Wilder's average for both, the same average that [[atr]] uses.

## Example

Over the last 14 days, a [[stock]] had an average gain of 60 cents and an average loss of 20 cents.

- RS = 60 / 20 = 3
- RSI = 100 − 100 / (1 + 3) = 100 − 25 = 75

Reverse the numbers, and RS = 20 / 60 = 1/3, so RSI = 100 − 100 / (1 + 1/3) = 100 − 75 = 25. When rises and falls are equally strong, RSI is 50.

## 70 and 30

- **Above 70: overbought.** Recent rises were unusually strong compared with falls.
- **Below 30: oversold.** Recent falls were unusually strong compared with rises.

In the [[mean-reversion]] example, a stock moves sideways between about $45 and $55, with an average near $50. It falls to a close of $46. Say its RSI is now 25: oversold. A mean-reversion trader reads this as a sign that the fall has gone far and the price may turn back toward $50.

## Strong trends

Overbought does not mean "about to fall". In a strong uptrend (see [[trend]]), most days rise, so the average gain stays much larger than the average loss. RSI can stay above 70 for weeks while the price keeps rising. A trader who sells each time RSI passes 70 leaves the trend early. In a strong downtrend, RSI can stay below 30 in the same way.

## Divergence

Traders watch for **divergence**: the price makes a higher [[peak-and-trough|peak]], but RSI makes a lower one. Some read it as an early sign of a turn, but often the trend continues.

## Watch out

- **RSI is not a rule by itself.** Use it inside [[entry-and-exit-rules]], with a [[stop-loss]], and check them with a [[backtest]].
- **Settings change the score.** A shorter length reaches the extremes more often; some use 80 and 20. Say which length and levels you use.
- **It lags.** RSI is built from past closes and reacts late.

Next, see [[mean-reversion]] for a strategy that buys oversold dips, or [[bollinger-bands]] to measure how far the price is from its average.
