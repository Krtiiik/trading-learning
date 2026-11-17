"""Command line entry point: `uv run trading ...`."""

import argparse
import sys
from pathlib import Path

from trading.data.bars import GRANULARITIES
from trading.data.providers import Provider, ProviderError, YahooProvider
from trading.data.storage import BarStore
from trading.data.universe import load_universe
from trading.data.update import update_symbol
from trading.data.validation import validate_daily


def main(argv: list[str] | None = None, provider: Provider | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    return args.command(args, provider or YahooProvider())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trading", description=__doc__)
    commands = parser.add_subparsers(required=True, metavar="command")

    fetch = commands.add_parser(
        "fetch",
        help="download bars into the local store",
        description="Download bars for the universe (or the given symbols) and check them. "
        "Symbols already stored get only the bars since their last stored bar.",
    )
    fetch.add_argument("--symbols", nargs="+", metavar="SYMBOL", help="instead of the universe")
    fetch.add_argument(
        "--universe", type=Path, help="TOML file listing symbols (default: universe.toml)"
    )
    fetch.add_argument("--granularity", choices=GRANULARITIES, default="1d")
    fetch.add_argument(
        "--full", action="store_true", help="re-download the whole history of each symbol"
    )
    fetch.add_argument("--data-dir", type=Path, help="store root (default: data/)")
    fetch.set_defaults(command=_fetch)
    return parser


def _fetch(args: argparse.Namespace, provider: Provider) -> int:
    symbols = [symbol.upper() for symbol in args.symbols] if args.symbols else load_universe(
        args.universe
    )
    store = BarStore(args.data_dir)
    width = max(len(symbol) for symbol in symbols)
    failed: list[str] = []

    plural = "" if len(symbols) == 1 else "s"
    print(f"Fetching {args.granularity} bars for {len(symbols)} symbol{plural} into {store.root}")
    for symbol in symbols:
        try:
            result = update_symbol(provider, store, symbol, args.granularity, full=args.full)
        except ProviderError as error:
            failed.append(symbol)
            print(f"{symbol:<{width}}  FAILED  {error}", file=sys.stderr)
            continue

        reason = f" ({result.reason})" if result.reason else ""
        print(
            f"{symbol:<{width}}  {result.mode:<11}  {result.total_bars:>6} bars"
            f"  {result.new_bars:+d}{reason}"
        )
        for issue in validate_daily(store.read(symbol, args.granularity)):
            print(f"{'':<{width}}  warning: {issue}")

    if failed:
        print(f"Failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0
