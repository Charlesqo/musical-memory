# Developer Guide

This document provides a quick overview for contributors.

## Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Checks

Run the test suite with:

```bash
pytest
```

The repository uses *pre-commit* for formatting and linting. After making
changes run it on the touched files:

```bash
pre-commit run --files <file1> <file2>
```

## Project Structure

- `src/cli.py` – command line interface and experimental GUI/web modes.
- `src/game.py` – game logic and sequence generation utilities.
- `src/score.py` – score storage abstraction.
- `src/main.py` – entrypoint that parses configuration then delegates to the CLI.
- `musical_memory/core.py` – stand‑alone class for managing note sequences.

## Extending the Game

- Add new interaction modes by expanding functions in `src/cli.py`.
- Introduce alternative note pools or difficulty rules in `src/game.py`.
- Replace the `ScoreManager` in `src/score.py` to store scores elsewhere.

