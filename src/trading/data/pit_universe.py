"""The point-in-time universe: the most traded USDT spot pairs at each monthly reconstitution.

Membership for a month is decided from daily bars that closed before the month began, so it
never uses information from the future, and coins that were later delisted stay in the
history. The same ranking gives each coin its liquidity tier for the cost model.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

QUOTE = "USDT"
UNIVERSE_DATASET = "binance/universe"
UNIVERSE_FILE = "TOP.parquet"

_LEVERAGED_BASES = (
    "1INCH AAVE ADA BCH BNB BTC DOT EOS ETH FIL LINK LTC SUSHI SXP TRX UNI XLM XRP XTZ YFI"
).split()

_TOKENISED_STOCKS = (
    "AAOIB AAPLB ADBEB AGPUB ALABB AMATB AMCB AMDB AMZNB APPB ARMB ASMLB ASTSB AVGOB AXTIB BABAB "
    "BBB BEB BMNRB BNCB BOTB BRKBB BSPB CBRSB COHRB COINB CRCLB CRDOB CRMB CRWDB CRWVB CYPHB "
    "DELLB DJTB DRAMB EWYB FLNCB FWDIB GEVB GLWB GMEB GOOGLB GPROB GSB HIMSB HOODB HPEB IBMB "
    "INTCB INTWB IRENB JPMB KORUB KSTRB LITEB LLYB MDBB METAB MRNAB MRVLB MSFTB MSTRB MUB MUUB "
    "MVLLB NBISB NFLXB NOKB NVDAB ORCLB PDDB PENGB PLTRB PYPLB QCOMB QNTB QQQB RDDTB RKLBB SECZB "
    "SHAZB SKDDB SKHYB SKUUB SMCIB SMHB SNDKB SNXXB SOXLB SOXSB SPCXB SPYB SQQQB STXB TMFB TQQQB "
    "TSLAB TSMB USARB USDEB UVXYB VSTB WDCB WENB ZMB"
).split()

EXCLUDED_BASES: dict[str, str] = {
    **dict.fromkeys(
        "USDC BUSD TUSD PAX USDP DAI FDUSD UST USTC SUSD USDS USDSB USD1 XUSD USDE BFUSD RLUSD "
        "RWUSD AEUR EURI EUR GBP AUD BKRW".split(),
        "stablecoin or fiat",
    ),
    **dict.fromkeys("WBTC WBETH BETH BNSOL PAXG XAUT".split(), "wrapped or pegged token"),
    **dict.fromkeys(_TOKENISED_STOCKS, "tokenised stock"),
    **dict.fromkeys(
        "BULL BEAR ETHBULL ETHBEAR BNBBULL BNBBEAR EOSBULL EOSBEAR XRPBULL XRPBEAR".split(),
        "leveraged token",
    ),
    **{f"{base}{side}": "leveraged token" for base in _LEVERAGED_BASES for side in ("UP", "DOWN")},
}
"""Base assets that are never universe members, with the reason. A curated list: the names
alone do not tell (JUP is a coin, BTCUP a leveraged token), so new listings need a look."""


@dataclass(frozen=True)
class UniverseRules:
    size: int = 40
    """Members per reconstitution (fewer while fewer pairs qualify)."""
    lookback_days: int = 30
    """Days of trailing quote volume that rank the pairs; a pair needs a bar on every one."""
    min_daily_volatility: float = 0.005
    """Pairs whose daily returns moved less than this over the lookback are treated as pegged.
    A net under the curated list: it catches a stablecoin nobody has classified yet."""
    tier_one: tuple[str, ...] = ("BTCUSDT", "ETHUSDT")
    tier_two_count: int = 10
    """Liquidity tiers for slippage: BTC and ETH, then this many next by volume, then the rest."""


def base_asset(symbol: str) -> str:
    """`BTC` for `BTCUSDT`; the earlier coin of a reused symbol (`LUNAUSDT-2022`) gives `LUNA`."""
    return symbol.upper().split("-")[0].removesuffix(QUOTE)


def exclusion(symbol: str) -> str | None:
    """Why a pair can never be a universe member, or None when it can."""
    return EXCLUDED_BASES.get(base_asset(symbol))


def build_universe(
    quote_volume: pd.DataFrame, close: pd.DataFrame, rules: UniverseRules = UniverseRules()
) -> pd.DataFrame:
    """Members at every month start, from daily panels (index: UTC dates, columns: symbols).

    One row per reconstitution `date` and member: `symbol`, `rank` (1 = most traded),
    `quote_volume` over the lookback, and liquidity `tier`. The row dated D uses only bars
    labelled before D and applies to bars labelled D or later, until the next reconstitution.
    """
    days = pd.date_range(quote_volume.index.min(), quote_volume.index.max(), freq="D")
    quote_volume = quote_volume.reindex(days)
    close = close.reindex(days)
    window = rules.lookback_days
    traded = quote_volume.rolling(window, min_periods=window).sum()
    moved = close.pct_change(fill_method=None).rolling(window, min_periods=window - 1).std()
    allowed = [symbol for symbol in quote_volume.columns if exclusion(symbol) is None]
    score = traded[allowed].where(moved[allowed] >= rules.min_daily_volatility)

    rows = []
    for date in pd.date_range(days[0], days[-1] + pd.Timedelta(days=1), freq="MS"):
        eve = date - pd.Timedelta(days=1)
        if eve not in score.index:
            continue
        ranked = score.loc[eve].dropna().sort_values(ascending=False, kind="stable")
        ranked = ranked[ranked > 0].head(rules.size)
        others = [symbol for symbol in ranked.index if symbol not in rules.tier_one]
        tier_two = set(others[: rules.tier_two_count])
        for rank, (symbol, volume) in enumerate(ranked.items(), start=1):
            tier = 1 if symbol in rules.tier_one else 2 if symbol in tier_two else 3
            rows.append((date, symbol, rank, float(volume), tier))
    universe = pd.DataFrame(rows, columns=["date", "symbol", "rank", "quote_volume", "tier"])
    return universe.astype({"date": "datetime64[ns]", "rank": "int64", "tier": "int64"})


def membership_panel(
    universe: pd.DataFrame, index: pd.DatetimeIndex, symbols: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    """Membership (bool) and liquidity tier (int) for each bar label and symbol.

    A bar takes the last reconstitution dated at or before its label. Coins outside the
    universe, and bars before the first reconstitution, get tier 3 and no membership.
    """
    labels = index.tz_localize(None) if index.tz is not None else index
    dates = np.sort(universe["date"].unique())
    position = np.searchsorted(dates, labels.to_numpy(), side="right") - 1
    column = {symbol: number for number, symbol in enumerate(symbols)}
    member_by_date = np.zeros((len(dates), len(symbols)), dtype=bool)
    tier_by_date = np.full((len(dates), len(symbols)), 3, dtype="int64")
    date_number = np.searchsorted(dates, universe["date"].to_numpy())
    for date, symbol, tier in zip(date_number, universe["symbol"], universe["tier"]):
        if symbol in column:
            member_by_date[date, column[symbol]] = True
            tier_by_date[date, column[symbol]] = tier
    known = position >= 0
    member = np.where(known[:, None], member_by_date[np.maximum(position, 0)], False)
    tier = np.where(known[:, None], tier_by_date[np.maximum(position, 0)], 3)
    return member, tier
