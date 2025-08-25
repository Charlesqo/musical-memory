"""Musical Memory game entry point.

This module imports the CLI and allows starting the game either using
command line arguments or a configuration file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from . import cli


def _load_config(path: str) -> List[str]:
    """Load JSON configuration and convert it to CLI arguments.

    Parameters
    ----------
    path: str
        Path to a JSON file containing keys supported by ``cli.parse_args``.

    Returns
    -------
    List[str]
        A list of command line arguments for ``cli.main``.
    """
    data = json.loads(Path(path).read_text())
    args: List[str] = []
    if "levels" in data:
        args.extend(["--levels", str(data["levels"])])
    if "difficulty" in data:
        args.extend(["--difficulty", data["difficulty"]])
    if data.get("audio"):
        args.append("--audio")
    return args


def main(argv: List[str] | None = None) -> None:
    """Entrypoint that delegates to the CLI module.

    Parameters
    ----------
    argv: List[str] | None
        Optional list of arguments. Defaults to ``sys.argv[1:]`` when ``None``.
    """
    parser = argparse.ArgumentParser(description="Musical Memory entry")
    parser.add_argument("--config", help="path to JSON configuration file")
    parsed, remaining = parser.parse_known_args(argv)
    cli_args: List[str] = remaining
    if parsed.config:
        cli_args = _load_config(parsed.config) + cli_args
    cli.main(cli_args)


if __name__ == "__main__":
    main()
