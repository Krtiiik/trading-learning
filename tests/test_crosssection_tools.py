"""The cross-sectional signals on the synthetic Store: each equals a plain loop and none looks ahead."""

import numpy as np
import pandas as pd
import pytest

from trading.experiments import crosssection_tools as tools
from trading.research.market import ResearchData
from trading.research.split import DEV_END


@pytest.fixture
def dev(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path)


def loop(values: np.ndarray, days: int, statistic) -> np.ndarray:
    """`statistic` of each coin's last `days` values at every bar; NaN unless all are finite."""
    out = np.full(values.shape, np.nan)
    for bar in range(days - 1, len(values)):
        for coin in range(values.shape[1]):
            window = values[bar - days + 1 : bar + 1, coin]
            if np.isfinite(window).all():
                out[bar, coin] = statistic(window)
    return out


def test_past_return_is_the_close_over_the_close_that_many_bars_earlier(dev):
    market = dev.market("1d")
    expected = loop(market.close, 22, lambda closes: closes[-1] / closes[0] - 1)

    signal = tools.past_return(market, 21).to_numpy()

    # Only the two ends matter to a return, so the loop is NaN in more cells; compare where it is not.
    known = np.isfinite(expected)
    assert known.sum() > 1000 and np.allclose(signal[known], expected[known])
    assert not np.isfinite(signal[:21]).any()


def test_volatility_is_the_standard_deviation_of_the_last_daily_returns(dev):
    market = dev.market("1d")
    returns = np.full(market.close.shape, np.nan)
    returns[1:] = market.close[1:] / market.close[:-1] - 1
    expected = loop(returns, 30, lambda window: window.std(ddof=1))

    signal = tools.volatility(market, 30).to_numpy()

    assert np.isfinite(expected).sum() > 1000
    assert np.allclose(signal, expected, equal_nan=True)


def test_log_mean_quote_volume_is_the_log_of_the_mean_of_the_last_bars(dev):
    market = dev.market("1d")
    expected = loop(market.quote_volume, 7, lambda window: np.log(window.mean()))

    signal = tools.log_mean_quote_volume(market, 7).to_numpy()

    assert np.isfinite(expected).sum() > 1000
    assert np.allclose(signal, expected, equal_nan=True)


@pytest.mark.parametrize(
    ("signal", "days"),
    [(tools.past_return, 21), (tools.volatility, 30), (tools.log_mean_quote_volume, 7)],
)
def test_removing_later_bars_leaves_earlier_rows_unchanged(dev, signal, days):
    cut = pd.Timestamp("2024-03-10")

    again = signal(dev.truncated(cut).market("1d"), days)

    pd.testing.assert_frame_equal(again, signal(dev.market("1d"), days).loc[:cut])
