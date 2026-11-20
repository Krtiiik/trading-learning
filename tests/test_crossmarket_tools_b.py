"""The outside-world cross-market signals on the synthetic Store."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from trading.experiments import crossmarket_tools_b as tools
from trading.research.market import ResearchData
from trading.research.split import DEV_END


@pytest.fixture
def dev(crypto_root, tmp_path) -> ResearchData:
    return ResearchData(DEV_END, crypto_root, records=tmp_path)


def test_volume_growth_equals_a_plain_loop_over_the_members_with_both_bars(dev):
    # The synthetic coins trade the same amount every day, so give them volumes that move.
    noise = np.random.default_rng(5).lognormal(sigma=0.4, size=dev.market("1d").close.shape)
    market = replace(dev.market("1d"), quote_volume=dev.market("1d").quote_volume * noise)
    expected = np.full(len(market.index), np.nan)
    for bar in range(1, len(market.index)):
        now = prior = 0.0
        for coin in np.flatnonzero(market.member[bar]):
            today, yesterday = market.quote_volume[bar, coin], market.quote_volume[bar - 1, coin]
            if np.isfinite(today) and np.isfinite(yesterday):
                now, prior = now + today, prior + yesterday
        if prior > 0:
            expected[bar] = np.clip(np.log(now / prior), -0.5, 0.5)

    growth = tools.volume_growth(market, clip=0.5)

    assert growth.index.equals(market.index) and growth.name == tools.SIGNAL
    assert np.allclose(growth.to_numpy(), expected, equal_nan=True)
    assert np.isfinite(expected).sum() > 500 and (np.abs(expected) == 0.5).any()


def test_volume_growth_does_not_change_when_later_bars_are_removed(dev):
    cut = pd.Timestamp("2024-03-01")

    again = tools.volume_growth(dev.truncated(cut).market("1d"), clip=1.0)

    pd.testing.assert_series_equal(again, tools.volume_growth(dev.market("1d"), clip=1.0).loc[:cut])
