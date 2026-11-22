Position sizing is choosing how many shares (or units, such as coins or currency) to buy in a trade. A common method starts from the loss you accept if your [[stop-loss]] is hit, and works back to the number of shares.

## Size, value and risk

The number of shares you hold is your **position size**. Two amounts of money follow from it, and they are not the same:

- **Position value**: what those shares are worth (price × shares).
- **Money at risk**: what you lose if the price falls to your stop and the stop sells there.

The stop makes the money at risk much smaller than the position value.

## The method

1. Choose the part of your account you are willing to lose on one trade, for example 1%.
2. Choose the stop before you choose the size.
3. Divide:

**shares = (account × risk %) / (entry price − stop price)**

Round the result down to whole shares, so the risk stays at or below your limit.

## Example

You have a $10,000 account and risk 1%: $100. You buy a [[stock]] at $42 with a stop at $38, a risk of $4 per share. $100 / $4 = 25 shares. Their position value is $1,050; the risk is about $100.

Now say this stock swings more (higher [[volatility]]), so you put the stop at $34. The risk is $8 per share: $100 / $8 = 12.5, rounded down to 12 shares. Their position value is $504, and they risk $96. A wider stop gives fewer shares, and the money at risk stays about the same.

## Why a small fixed percentage

Every [[strategy]] has runs of losing trades. Risking 1% of the current balance makes each loss a little smaller than the last. After 10 losses in a row, the account still holds about $9,044 (10,000 × 0.99¹⁰). Risking 10% each time instead would leave about $3,487. A small percentage keeps the [[drawdown]] (the account's fall from its high) small.

The 1% is an example, not a recommendation.

## When cash is the limit

A very tight stop gives a very large position size. With a stop at $41.90, the risk is only 10 cents per share, and the formula says 1,000 shares: a position value of $42,000, more than the whole account. Your cash buys at most 238 shares (position value $9,996). Then the account, not the percentage, limits the size. Borrowing to buy more is [[leverage]], which enlarges losses too.

## Watch out

- **The planned risk is not a guarantee.** A [[gap]] (a jump in price, for example overnight) past the stop can make the loss bigger than planned.
- **Costs come on top.** [[fees-and-commissions|Fees]] and the [[spread]] (the gap between the best price buyers offer and the best price sellers want) add to each loss.
- **Size does not fix a bad trade.** It controls how much a loss hurts, not how often you lose.

Next, see [[risk-reward]], then [[drawdown]], or try the lesson [[planning-one-trade]].
