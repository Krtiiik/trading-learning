import pytest

from trading.data.universe import load_universe


def test_project_universe_lists_starter_etfs():
    symbols = load_universe()

    assert symbols[0] == "SPY"
    assert {"QQQ", "TLT", "GLD", "XLK"} <= set(symbols)


def test_symbols_are_uppercased_and_deduplicated(tmp_path):
    path = tmp_path / "universe.toml"
    path.write_text('[universe]\nsymbols = ["spy", " QQQ", "SPY"]\n')

    assert load_universe(path) == ["SPY", "QQQ"]


def test_file_without_symbols_is_rejected(tmp_path):
    path = tmp_path / "universe.toml"
    path.write_text("[other]\n")

    with pytest.raises(ValueError, match="no \\[universe\\] symbols"):
        load_universe(path)
