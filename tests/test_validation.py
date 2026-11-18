import pandas as pd

from trading.data.validation import validate_daily

from conftest import make_bars


def checks(bars: pd.DataFrame) -> dict[str, list[str]]:
    return {
        issue.check: [date.strftime("%Y-%m-%d") for date in issue.dates]
        for issue in validate_daily(bars)
    }


def nyse_bars() -> pd.DataFrame:
    """Bars for every NYSE session from 2024-01-02 to 2024-01-12 (2024-01-01 was a holiday)."""
    return make_bars("2024-01-02", 9)


def test_clean_bars_pass_every_check():
    assert validate_daily(nyse_bars()) == []


def test_empty_bars_are_reported():
    assert checks(make_bars("2024-01-02", 0)) == {"empty": []}


def test_duplicate_dates_are_reported():
    bars = nyse_bars()
    bars = pd.concat([bars, bars.iloc[[3]]]).sort_index()

    assert checks(bars)["duplicates"] == ["2024-01-05"]


def test_non_positive_and_missing_prices_are_reported():
    bars = nyse_bars()
    bars.loc["2024-01-04", "low"] = 0.0
    bars.loc["2024-01-08", "adj_close"] = float("nan")

    assert checks(bars)["prices"] == ["2024-01-04", "2024-01-08"]


def test_close_outside_high_low_range_is_reported():
    bars = nyse_bars()
    bars.loc["2024-01-05", "close"] = bars.loc["2024-01-05", "high"] + 5

    assert checks(bars)["ohlc"] == ["2024-01-05"]


def test_missing_sessions_and_bars_on_holidays_are_reported():
    bars = nyse_bars().drop(pd.Timestamp("2024-01-05"))
    holiday = make_bars("2024-01-15", 1)  # Martin Luther King Jr. Day
    bars = pd.concat([bars, holiday, make_bars("2024-01-16", 1)])

    found = checks(bars)

    assert found["missing"] == ["2024-01-05"]
    assert found["extra"] == ["2024-01-15"]


def test_big_move_without_split_is_reported():
    bars = nyse_bars()
    bars.loc["2024-01-09":, ["open", "high", "low", "close"]] /= 2

    assert checks(bars)["jumps"] == ["2024-01-09"]


def test_big_move_on_split_day_is_reported_as_unadjusted_history():
    # Prices are split-adjusted, so a real split never moves the close. A jump on the
    # split day means the bars before it were stored before the split was applied.
    bars = nyse_bars()
    bars.loc["2024-01-09":, ["open", "high", "low", "close"]] /= 2
    bars.loc["2024-01-09", "splits"] = 2.0

    found = checks(bars)

    assert found["split"] == ["2024-01-09"]
    assert "jumps" not in found


def test_crypto_bars_are_checked_against_a_market_that_never_closes():
    from trading.data.validation import validate_crypto

    from conftest import make_klines

    bars = make_klines("2024-01-01", "2024-01-20").assign(splits=0.0)
    bars["adj_close"] = bars["close"]
    assert validate_crypto(bars) == []

    gappy = bars.drop(bars.index[[5, 6]])
    gappy.loc["2024-01-15":, ["open", "high", "low", "close", "adj_close"]] *= 0.001  # an unrecorded redenomination

    found = {issue.check: issue for issue in validate_crypto(gappy)}
    assert str(found["missing"]) == "missing: 2 1d bars missing inside the history [2024-01-06, 2024-01-07]"
    assert [date.strftime("%Y-%m-%d") for date in found["jumps"].dates] == ["2024-01-15"]
