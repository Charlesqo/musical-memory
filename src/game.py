from pathlib import Path
from .score import ScoreManager


def end_game(score: int, file_path: Path | None = None) -> str:
    """Handle end-of-game logic by updating and reporting the high score."""
    manager = ScoreManager(file_path or ScoreManager().file_path)
    manager.load()
    is_new = manager.record(score)
    message = (
        f"New high score: {manager.high_score}!" if is_new else
        f"Your score: {score}. High score: {manager.high_score}."
    )
    print(message)
    return message


if __name__ == "__main__":
    import random
    # Simulate a game score for demonstration purposes.
    demo_score = random.randint(0, 100)
    end_game(demo_score)
