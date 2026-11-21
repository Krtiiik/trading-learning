Position sizing is choosing how many shares (or units) to buy in a trade. A common method starts from the loss you accept if your [[stop-loss]] is hit, and works back to the number of shares.

## Money put in, money at risk

Two amounts matter, and they are not the same:

- **Position size**: the money you put into the trade, the price times the number of shares.
- **Money at risk**: what you lose if the price falls to your stop and the stop sells there.

The stop is what makes the second amount much smaller than the first.

## The method

1. Choose the part of your account you accept to lose on one trade, for example 1%.
2. Choose the stop before you choose the size.
3. Divide:

**shares = (account × risk %) / (entry − stop)**

Round the result down to whole shares, so the risk stays at or below your limit.

## Example

You have a $10,000 account and risk 1%: $100. You buy a [[stock]] at $42 with a stop at $38, a risk of $4 per share. $100 / $4 = 25 shares. They cost $1,050, but the plan risks only about $100 of it.

Now say this stock usually swings more (it has higher [[volatility]]), so you put the stop at $34 instead. The risk is $8 per share: $100 / $8 = 12.5, rounded down to 12 shares. They cost $504 and risk $96. A wider stop gives fewer shares, and the money at risk stays about the same.

## Why a small fixed percentage

Every [[strategy]] has runs of losing trades. If you risk 1% of what the account holds at the time, each loss is a little smaller than the last. After 10 losses in a row, the account still holds about $9,044 (10,000 × 0.99¹⁰). Risking 10% each time instead would leave about $3,487. A small percentage keeps the account's fall from its high, its [[drawdown]], small. From $3,487 you need a gain of about 187% to get back to $10,000; from $9,044, only about 11%.

The 1% is only this site's example, not a recommendation; the choice is yours.

## When cash is the limit

A very tight stop gives a very large position. With a stop at $41.90, the risk is only $0.10 per share, and the formula says 1,000 shares: $42,000, more than the whole account. You can buy at most what your cash pays for, here 238 shares ($9,996). Then the account, not the percentage, limits the size. Borrowing to buy more is [[leverage]], which enlarges losses too.

## Watch out

- **The planned risk is not a guarantee.** If the stock closes at $40 and opens the next morning at $35, a [[gap]] past the stop, the stop sells around $35. The 25 shares lose about $7 each: about $175 instead of $100.
- **Costs come on top.** [[fees-and-commissions|Fees]] and the [[spread]] add to each loss.
- **Size does not fix a bad trade.** It controls how much a loss hurts, not how often you lose.

Next, see [[risk-reward]], then [[drawdown]].
