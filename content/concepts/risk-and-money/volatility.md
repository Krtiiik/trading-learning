Volatility is how much a price usually moves in a given time. A price with high volatility makes large jumps up and down; a price with low volatility moves in small steps. Traders give it as a percentage per day or per year.

## Size, not direction

Volatility tells you how big the moves are, not which way they go. Two prices can both end the year 10% higher: one climbs a little each week, the other often jumps 5% up or 4% down on the way. The second one is more volatile.

Volatility also differs between assets: many smaller [[cryptocurrency|cryptocurrencies]] often move more in a day than a [[stock|large stock]] in a week, and even Bitcoin swings more than a [[index|broad stock index]], about as much as the jumpiest large stocks.

## How traders measure it

- **Daily range**: the day's high minus its low (see [[ohlc]]). Its average over recent days is a rough measure.
- **[[atr]]** (average true range): the same average, but it also counts any jump ([[gap]]) from the previous close.
- **Standard deviation of daily changes**: a statistic of how far daily percentage changes usually spread from their average.

All these measure **historical volatility**: how much the price moved in the past. **Implied volatility** is the size of move that traders expect in the future, read from the prices of [[option|options]] (contracts giving the right to buy or sell at a set price; they cost more when traders expect bigger moves). The VIX shows the implied volatility of the S&P 500 index for the next 30 days, as a yearly percentage.

## Calm and wild periods

Large moves tend to come in groups, and calm days usually follow calm days. A market can stay quiet for months, then swing hard for weeks after bad news.

## Example

Two stocks both trade at $42. You risk 1% of a $10,000 account ($100) per trade.

- **Calm stock**: its ATR (average daily move, gaps included) is about $1 (about 2.4%). You put the [[stop-loss]] at $38, four daily moves below the $42 buy price, so normal wobbles seldom reach it.
- **Jumpy stock**: its ATR is about $2 (about 4.8%). A stop at $38 is only two daily moves away, so you put it four moves away, at $34.

[[position-sizing|Position sizing]] then gives 25 shares of the calm stock and 12 of the jumpy one, each risking about $100. The target (the price where you plan to sell) moves too: a [[risk-reward]] of 3 to 1 needs $54 for the calm stock but $66 for the jumpy one (three times the stop distance above $42).

## Watch out

- **Volatility changes.** A stop that fit a calm month can be too tight in a wild one, so measure again from time to time.
- **Past volatility does not limit the next move.** A gap can be many times larger than a normal day's move.
- **Do not chase volatility for fast gains.** Large moves bring large losses as easily as large gains.

Next, see [[atr]], then [[position-sizing]].
