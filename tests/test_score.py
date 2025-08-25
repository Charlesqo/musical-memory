from pathlib import Path
from src.score import ScoreManager


def test_record_updates_high_score(tmp_path: Path) -> None:
    file_path = tmp_path / "scores.json"
    manager = ScoreManager(file_path)
    manager.load()
    assert manager.high_score == 0

    assert manager.record(10) is True
    assert manager.high_score == 10

    # Lower score should not update high score
    assert manager.record(5) is False
    assert manager.high_score == 10

    # History should record all scores
    assert manager.history == [10, 5]
