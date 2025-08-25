import argparse
from typing import List

# Support running as module or script
try:  # pragma: no cover - import resolution
    from .game import generate_next_note, play_sequence, check_sequence
except ImportError:  # pragma: no cover
    from pathlib import Path
    import sys

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
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    print("Welcome to Musical Memory!")

    while True:
        sequence: List[int] = []
        for level in range(1, args.levels + 1):
            sequence.append(generate_next_note(args.difficulty))
            print(f"Level {level}. Listen to the sequence:")
            play_sequence(sequence, use_audio=args.audio)
            guess = input("Repeat the sequence separated by spaces: ").strip()
            try:
                user_sequence = [int(x) for x in guess.split()]
            except ValueError:
                print("Invalid input, numbers only. Game over.")
                break
            if check_sequence(sequence, user_sequence):
                print("Correct!\n")
            else:
                print("Wrong sequence. Game over.")
                break
        else:
            print("Congratulations! You completed all levels.")
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
