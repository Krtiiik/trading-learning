"""The configured set of symbols to download."""

import tomllib
from pathlib import Path

from trading.data.storage import PROJECT_ROOT

DEFAULT_UNIVERSE_FILE = PROJECT_ROOT / "universe.toml"


def load_universe(path: Path | None = None) -> list[str]:
    """Symbols listed under `[universe] symbols` in a TOML file, uppercased, in file order."""
    path = Path(path) if path is not None else DEFAULT_UNIVERSE_FILE
    with path.open("rb") as file:
        config = tomllib.load(file)
    try:
        symbols = config["universe"]["symbols"]
    except KeyError as error:
        raise ValueError(f"{path} has no [universe] symbols list") from error
    return list(dict.fromkeys(symbol.strip().upper() for symbol in symbols))
