A trading journal is a record of each trade you make: what you planned before you bought, what happened, and whether you followed your rules. Here a trade means one position: a buy and the later sale that closes it.

## What to record

**Before the entry**, write the plan:

- the [[entry-and-exit-rules|rule]] that gave the signal;
- the entry price and the number of shares;
- the [[stop-loss]] and how you set it;
- the money at risk if the stop is hit;
- the [[risk-reward|target]], and whether an order sells there or it is only a check, with no order waiting.

**After the exit**, write what happened:

- the fills, the prices your orders traded at;
- which exit closed the trade;
- the costs: the [[spread]], [[fees-and-commissions|fees]] and any currency conversion;
- the result in dollars and as a multiple of the planned risk, often called **R** ($200 on $100 of risk is 2 R);
- whether you followed the rules, yes or no;
- a short note: why you broke a rule, or what you felt.

Write the plan before you buy. A plan written afterwards bends to fit the result.

## Example

The trade from the lesson [[planning-one-trade]]:

| Field | Record |
|---|---|
| Rule | [[trend-following|Trend following]]: first close above the 100-day [[moving-average|average]] |
| Plan | Buy 25 shares at $42 on a $10,000 account ([[position-sizing]]: $100 / $4) |
| Stop | $38, four [[atr|ATRs]] ($1 each) below the entry |
| Risk | $100, 1% of the account |
| Target | $54 (3 to 1), only a check |
| Fills | Bought at $42, sold at $64 |
| Exit | Signal exit: a close below the average |
| Costs | $5 commission; spread about 25 cents, left out; conversion if your account is not in dollars |
| Result | +$550 before costs, +$545 after; 5.5 R before costs (5.45 R after) |
| Rules followed | Yes |
| Note | Wanted to sell at $54, held as the rule said |

## Start with paper trading

Many [[broker|brokers]] offer a demo account where you trade with pretend money: paper trading. Keep the journal there too. Paper trading checks that you can follow the rules on time, but it hides real fills and real fear. Then trade live with a small risk, as in [[testing-a-trading-rule]].

## How to review it

After 20 or 30 trades, take a first rough look at your [[win-rate-and-expectancy|win rate and expectancy]] from the journal and compare them with your [[backtest]]. The backtest example won 30% of trades, with an expectancy of $78 per trade before costs: 0.78 R on $100 of risk.

Fills clearly worse than the backtest's prices point to [[slippage]], or to a backtest that assumed prices you could not get. Losses bigger than the planned risk (more than 1 R) point to a moved stop, or to a [[gap]] past the stop; the fills and the note show which. Many broken rules point to [[trading-psychology]], not to the rule.

## Records for tax

Tax rules differ by country (see [[taxes-on-trading]]). Broker statements give the official prices and dates. A Czech trader counts gains in CZK, using the daily rate of the ČNB (the Czech National Bank) or the yearly unified rate, such as 21 CZK per dollar. Record the buy and sale dates: they set the rate, and shares and funds held over 3 years are tax-free in Czechia.

## Watch out

- **Do not skip the losers.** A journal of only good trades looks better than your trading.
- **One trade proves little.** A good result does not prove a good plan, and twenty trades is still a small sample.
- **Do not change the rules after a few losses.** Test any change first.

Next, see [[win-rate-and-expectancy]], then [[trading-psychology]].
