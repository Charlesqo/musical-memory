import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

@dataclass
class ScoreManager:
    """Manage game scores stored in a JSON file.

    The data layout is:
    {
        "high_score": int,
        "history": [int, ...]
    }
    """

    file_path: Path = field(default_factory=lambda: Path(__file__).with_name("scores.json"))
    high_score: int = 0
    history: List[int] = field(default_factory=list)

    def load(self) -> None:
        """Load score data from ``file_path``.

        If the file does not exist an empty structure is created so that the
        manager can be used immediately.
        """
        if self.file_path.exists():
            with self.file_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.high_score = data.get("high_score", 0)
            self.history = data.get("history", [])
        else:
            self.high_score = 0
            self.history = []

    def save(self) -> None:
        """Persist current score data to ``file_path``."""
        data = {"high_score": self.high_score, "history": self.history}
        with self.file_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    def record(self, score: int) -> bool:
        """Record ``score`` and update high score.

        Returns ``True`` if ``score`` is a new high score.
        """
        self.history.append(score)
        new_high = False
        if score > self.high_score:
            self.high_score = score
            new_high = True
        self.save()
        return new_high
