Drawdown is how far your account has fallen from its highest value so far, its high. You measure it from that high, not from the money you started with.

Every [[strategy]] has losing streaks, even one that makes money on average (a positive [[win-rate-and-expectancy|expectancy]]). Drawdown shows what they cost.

## How to find it

**drawdown = (high − current value) / high**

The top part, high − current value, is the drawdown in money. Multiply the result by 100 to get a percentage. Each new high sets the drawdown back to zero.

## Example

A [[backtest]] of a [[trend-following]] strategy on a $10,000 account gives these values at the end of each trade, before costs:

- Trade 1 wins: $10,150, a new high.
- Trades 2 to 5 lose: $10,030. The drawdown is $120, or 1.18% of $10,150.
- Trade 6 wins: $10,580, a new high. The drawdown is zero again.
- Trades 7 to 9 lose: $10,480, a drawdown of $100 (0.95%).
- Trade 10 wins: $10,780, a new high.

The largest drawdown is the **maximum drawdown**: here $120 (1.18%). Inside a trade the account can fall further than these end-of-trade values show.

## Time under water

A drawdown also has a length: the time from a high until the account gets back to it. Traders say the account is "under water" during that time. In the example, the longest time under water was four trades (2 to 5); the account got back to its high at trade 6. Real strategies can stay under water for months or years. It is hard to keep following rules that seem not to work.

## Losses need bigger gains to recover

After a fall, the account is smaller, so the same percentage gain adds fewer dollars than the loss took away. You need a bigger percentage to get back:

**gain needed = X / (1 − X)**, where X is the drawdown as a decimal (0.5 for 50%).

A 50% fall needs a 100% gain: $10,000 falls to $5,000, and $5,000 must double.

| Drawdown | Gain needed to recover |
|---|---|
| 10% | 11% |
| 20% | 25% |
| 50% | 100% |
| 65.13% | 187% |
| 90% | 900% |

## Risk per trade sets the depth

The example in [[position-sizing]] has 10 losses in a row on a $10,000 account. If each loss takes the full 1% of the current balance, $9,044 is left: a drawdown of 9.56%, which needs a gain of about 11% to recover. Risking 10% leaves $3,487: a drawdown of 65.13%, which needs about 187%.

## Watch out

- **A backtest's maximum drawdown is not the worst you will see.** It is only the worst in that piece of the past. Expect a larger one in real trading.
- **You must be able to keep following the rules through it.** Before you start, ask if you could accept that fall and that time under water without giving up at its lowest point.
- **Do not raise your risk after losses to win the money back.** Traders call this [[trading-psychology|revenge trading]]. Bigger positions make the next losses bigger too, so the drawdown gets deeper faster.

Next, see [[diversification]], [[position-sizing]] to limit it, or try the lesson [[testing-a-trading-rule]].
