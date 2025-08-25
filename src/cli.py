import argparse
import sys
from pathlib import Path
from typing import List

from .score import ScoreManager

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
    parser = argparse.ArgumentParser(description="Musical memory game")
    parser.add_argument("--levels", type=int, default=5, help="number of levels to play")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="easy",
        help="difficulty determines available notes",
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
    print(_colour("Welcome to Musical Memory!", Fore.CYAN))

    manager = ScoreManager()
    manager.load()

    while True:
        sequence: List[int] = []
        score = 0
        for level in range(1, args.levels + 1):
            sequence.append(generate_next_note(args.difficulty))
            print(_colour(f"Level {level}. Listen to the sequence:", Fore.YELLOW))
            play_sequence(sequence, use_audio=args.audio)
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

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print(_colour("Thanks for playing!", Fore.CYAN))
            break


def _run_gui(args: argparse.Namespace) -> None:  # pragma: no cover - manual mode
    import tkinter as tk

    root = tk.Tk()
    root.title("Musical Memory")
    tk.Label(root, text="GUI mode is under construction").pack(padx=20, pady=20)
    root.mainloop()


def _run_web(args: argparse.Namespace) -> None:  # pragma: no cover - manual mode
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
    args = parse_args(argv)
    if args.mode == "cli":
        _run_cli(args)
    elif args.mode == "gui":
        _run_gui(args)
    else:
        _run_web(args)


if __name__ == "__main__":
    main()
