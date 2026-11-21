The win rate is the share of trades that end in a gain. Expectancy is the average result per trade, wins and losses together. Here a trade means one buy and the later sale that closes it.

The win rate tells you how often a [[strategy]] wins. Expectancy tells you whether it made money on the trades you measured.

## The parts

- **Win rate**: winning trades / all trades.
- **Average win**: the total of the gains / the number of winning trades.
- **Average loss**: the total of the losses / the number of losing trades.
- **Loss rate**: losing trades / all trades (1 − the win rate when no trade breaks even).

**Expectancy = win rate × average win − loss rate × average loss**

Write the average loss as a positive amount; the minus sign in the formula takes it away. A positive expectancy means the strategy made money on average; a negative one means it lost.

## Example

A [[backtest]] of a [[trend-following]] strategy finds 10 trades:

| | Trades | Total | Average |
|---|---|---|---|
| Wins | 3 | +$1,000 | +$333.33 |
| Losses | 7 | $220 | $31.43 |

- **Win rate**: 3 of 10, or 30%.
- **Average win**: $1,000 / 3, about $333.
- **Average loss**: $220 / 7, about $31.
- **Expectancy**: 0.30 × $333.33 − 0.70 × $31.43 = $100 − $22 = **$78 per trade** before costs. That equals the $780 total / 10 trades.

The strategy loses 7 times in 10 and still makes money, because the average win is more than ten times the average loss.

Each trade risked about $100, the loss if its [[stop-loss]] was hit. The losers were all sold earlier, on a close below the 100-day [[moving-average]], so the average loss was only about $31. [[risk-reward|Risk/reward]] compares the possible gain with the possible loss before a trade; average win and average loss show what actually happened.

## A high win rate alone means nothing

Now take a strategy that wins 90% of the time, but each win is $10 and each loss is $150:

0.90 × $10 − 0.10 × $150 = $9 − $15 = **−$6 per trade**.

It wins nine trades in ten and loses money anyway: one loss takes away more than nine wins bring. Always look at the win rate and the average sizes together.

## Costs come off every trade

The [[spread]] (the gap between the price buyers offer and the price sellers want) and [[fees-and-commissions|fees]] make each win smaller and each loss bigger. At $5 per round trip (buying, then selling), the $78 expectancy becomes about $73. A strategy with a small expectancy can turn negative after costs.

## Watch out

- **Ten trades is few.** One more big win or loss would change these numbers a lot. Expectancy from a few trades is a rough guess, not a measurement.
- **Positive expectancy still has losing streaks.** In the backtest behind this example, trades 2 to 5 were four losses in a row. Such runs pull the account down from its high, its [[drawdown]]. A small risk per trade, set with [[position-sizing]], helps you survive them.
- **The past is not a promise.** An expectancy from past trades shows how the rules did then, not what they will do next.

Next, see [[risk-reward]], then [[drawdown]].
