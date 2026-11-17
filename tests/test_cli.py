from trading.cli import main
from trading.data.storage import BarStore

from conftest import FakeProvider, make_bars


def test_fetch_downloads_given_symbols_and_reports_them(tmp_path, capsys):
    provider = FakeProvider({"SPY": make_bars("2024-01-02", 9), "QQQ": make_bars("2024-01-02", 9)})

    code = main(["fetch", "--symbols", "spy", "qqq", "--data-dir", str(tmp_path)], provider)

    assert code == 0
    assert BarStore(tmp_path).symbols("1d") == ["QQQ", "SPY"]
    output = capsys.readouterr().out
    assert "SPY  full" in output
    assert "nothing stored yet" in output


def test_fetch_defaults_to_universe_file(tmp_path, capsys):
    universe = tmp_path / "universe.toml"
    universe.write_text('[universe]\nsymbols = ["GLD"]\n')
    provider = FakeProvider({"GLD": make_bars("2024-01-02", 9)})

    code = main(
        ["fetch", "--universe", str(universe), "--data-dir", str(tmp_path / "data")], provider
    )

    assert code == 0
    assert [request[0] for request in provider.requests] == ["GLD"]


def test_fetch_prints_validation_warnings(tmp_path, capsys):
    gappy = make_bars("2024-01-02", 9).drop(make_bars("2024-01-05", 1).index)
    provider = FakeProvider({"SPY": gappy})

    main(["fetch", "--symbols", "SPY", "--data-dir", str(tmp_path)], provider)

    assert "warning: missing: 1 NYSE sessions without a bar [2024-01-05]" in capsys.readouterr().out


def test_fetch_continues_past_failures_and_exits_nonzero(tmp_path, capsys):
    provider = FakeProvider({"SPY": make_bars("2024-01-02", 9)})

    code = main(["fetch", "--symbols", "NOPE", "SPY", "--data-dir", str(tmp_path)], provider)

    assert code == 1
    assert BarStore(tmp_path).symbols("1d") == ["SPY"]
    assert "Failed: NOPE" in capsys.readouterr().err


def test_full_flag_redownloads(tmp_path, capsys):
    provider = FakeProvider({"SPY": make_bars("2024-01-02", 9)})
    args = ["fetch", "--symbols", "SPY", "--data-dir", str(tmp_path)]
    main(args, provider)

    main([*args, "--full"], provider)

    assert provider.requests[-1] == ("SPY", None, None)
