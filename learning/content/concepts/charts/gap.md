A gap is a jump in price from the close of one period to the open of the next (see [[ohlc]]): the new period's first trade is far from the last one.

- **Gap up**: the new period opens above the last close.
- **Gap down**: the new period opens below the last close.

## How it looks on a chart

A big gap shows as empty space between two [[candle|candles]]. If the price never comes back during the new period, the two candles do not overlap: in a gap down, the new candle's high (the top of its [[wick]]) stays below the old candle's low. If the price moves back, the space closes, but the period still opened with a gap.

## Why gaps happen

Most gaps come from news while the market is closed, such as a company's earnings (its quarterly profit) reported after the close. Traders change their prices before the next open.

## Which markets gap

- **Stocks** gap often, because the regular session of an [[exchange]] closes every night and at weekends (see [[trading-hours]]).
- **[[forex-pair|Forex pairs]]** trade around the clock on weekdays, so they gap mainly at weekends.
- **[[cryptocurrency|Cryptocurrencies]]** trade all day, every day, so they seldom gap.

## Example

You bought 25 shares of a [[stock]] at $42, with a [[stop-loss]] at $38. On Monday the stock closes at $40; its low that day is $39.20. After the close, the company reports bad earnings.

On Tuesday the stock opens at $35, a gap down of $5. Both days also traded inside that range, so the empty space is smaller: from Tuesday's high, $36, to Monday's low, $39.20.

Your stop at $38 sells at the first price after the jump, around $35. You lose about $7 per share, not the planned $4: about $175 instead of $100.

## What a gap does to stop orders

A stop order waits until the price reaches or passes its stop price, then becomes a market order (see [[order-types]]). At most brokers, a plain stop works only in the regular session, so after a gap it triggers at the first price after the jump.

## Filling the gap

When the price comes back to its level before the gap (usually the old close), traders say the gap is **filled**. Others count it filled once the price crosses the empty space: in the example, at $39.20, not $40. Some fill the same day, some never. A big gap after news can start a new [[trend]].

## Watch out

- **A stop does not guarantee its price.** The example lost nearly twice the plan.
- **A stop-limit can miss completely.** It becomes a limit order, which sells only at your price or better. After a gap past that price, it does not sell, and you still hold the falling stock.
- **Small gaps are common.** Most stocks open slightly away from the last close almost daily. They matter mainly when your stop is close to the price.

Next, see [[stop-loss]], then [[trading-hours]].
