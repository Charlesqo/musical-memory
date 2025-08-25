"""Command-line interface for the Musical Memory game.

This module provides a CLI for playing the game, as well as experimental
GUI and web modes that can be expanded in the future.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .score import ScoreManager
from .profile import ProfileManager

# Optional colour support ----------------------------------------------------
try:  # pragma: no cover - optional dependency
    from colorama import Fore, Style, init as colorama_init

    colorama_init()

    def _colour(text: str, colour: str) -> str:
        return f"{colour}{text}{Style.RESET_ALL}" if sys.stdout.isatty() else text

except Exception:  # pragma: no cover - colour is optional
    class _DummyFore:
        CYAN = YELLOW = RED = GREEN = MAGENTA = ""

    Fore = _DummyFore()  # type: ignore

    def _colour(text: str, colour: str) -> str:
        return text


# Support running as module or script ----------------------------------------
try:  # pragma: no cover - import resolution
    from .game import generate_next_note, play_sequence, check_sequence
except ImportError:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    from game import generate_next_note, play_sequence, check_sequence


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    """Parse command-line options for the game.

    Parameters
    ----------
    argv:
        Optional list of argument strings. When ``None`` the arguments are
        taken from :data:`sys.argv`.
    """
    parser = argparse.ArgumentParser(description="Musical memory game")
    parser.add_argument("--levels", type=int, default=5, help="number of levels to play")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="easy",
        help="difficulty determines available notes",
    )
    parser.add_argument(
        "--tempo",
        type=float,
        default=0.5,
        help="delay between notes in seconds",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=1,
        help="how many new notes are added each level",
    )
    parser.add_argument(
        "--user",
        default="player",
        help="profile name for saving progress",
    )
    parser.add_argument(
        "--import-data",
        type=Path,
        help="import profile data from file before playing",
    )
    parser.add_argument(
        "--export-data",
        type=Path,
        help="export profile data to file after playing",
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="play tones using simpleaudio if available",
    )
    parser.add_argument(
        "--mode",
        choices=["cli", "gui", "web"],
        default="cli",
        help="choose interaction mode",
    )
    return parser.parse_args(argv)


def _run_cli(args: argparse.Namespace) -> None:
    """Run the interactive command-line version of the game."""

    print(_colour("Welcome to Musical Memory!", Fore.CYAN))

    manager = ScoreManager()
    manager.load()
    profiles = ProfileManager()
    profiles.load()
    if args.import_data:
        profiles.import_data(args.import_data)

    while True:
        sequence: List[int] = []
        score = 0
        for level in range(1, args.levels + 1):
            for _ in range(args.step):
                sequence.append(generate_next_note(args.difficulty))
            print(_colour(f"Level {level}. Listen to the sequence:", Fore.YELLOW))
            play_sequence(sequence, use_audio=args.audio, delay=args.tempo)
            guess = input("Repeat the sequence separated by spaces: ").strip()
            try:
                user_sequence = [int(x) for x in guess.split()]
            except ValueError:
                print(
                    _colour(
                        f"Invalid input, numbers only. Game over. Provided: {guess}",
                        Fore.RED,
                    )
                )
                break
            if check_sequence(sequence, user_sequence):
                print(_colour("Correct!\n", Fore.GREEN))
                score = level
            else:
                print(
                    _colour(
                        f"Wrong sequence. Game over. Expected {' '.join(map(str, sequence))}",
                        Fore.RED,
                    )
                )
                break
        else:
            print(_colour("Congratulations! You completed all levels.", Fore.CYAN))
            score = args.levels

        is_high = manager.save_score(score)
        if is_high:
            print(_colour(f"New high score: {manager.high_score}!", Fore.MAGENTA))
        else:
            print(
                _colour(
                    f"Your score: {score}. High score: {manager.high_score}.", Fore.MAGENTA
                )
            )

        profiles.record_score(args.user, score)
        profile = profiles.get_profile(args.user)
        profile.settings.update(
            {"difficulty": args.difficulty, "tempo": args.tempo, "step": args.step}
        )
        profiles.save()
        lb = profiles.leaderboard()
        print(_colour("Leaderboard:", Fore.CYAN))
        for name, hs in lb:
            print(f"  {name}: {hs}")

        if args.export_data:
            profiles.export_data(args.export_data)

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print(_colour("Thanks for playing!", Fore.CYAN))
            break


def _run_gui(args: argparse.Namespace) -> None:  # pragma: no cover - manual mode
    """Run a very small experimental Tk GUI."""

    import tkinter as tk

    root = tk.Tk()
    root.title("Musical Memory")
    tk.Label(root, text="GUI mode is under construction").pack(padx=20, pady=20)
    root.mainloop()


def _run_web(args: argparse.Namespace) -> None:  # pragma: no cover - manual mode
    """Start a minimal HTTP server announcing the web mode."""

    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: D401 - small handler
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Musical Memory web mode is under construction</h1></body></html>"
            )

    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("Serving on http://127.0.0.1:8000 - press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv: List[str] | None = None) -> None:
    """Entry point choosing between CLI, GUI and web modes."""

    args = parse_args(argv)
    if args.mode == "cli":
        _run_cli(args)
    elif args.mode == "gui":
        _run_gui(args)
    else:
        _run_web(args)


if __name__ == "__main__":
    main()
