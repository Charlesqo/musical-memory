import builtins
from typing import List

from src import cli


def _make_dummy_manager():
    class DummyManager:
        instances: List["DummyManager"] = []

        def __init__(self):
            self.saved: List[int] = []
            self.high_score = 0
            DummyManager.instances.append(self)

        def load(self) -> None:
            pass

        def save_score(self, score: int) -> bool:
            self.saved.append(score)
            if score > self.high_score:
                self.high_score = score
            return True

    return DummyManager


def test_cli_invalid_input(monkeypatch, capsys):
    Dummy = _make_dummy_manager()
    # save_score should indicate not a new high score to exercise the other branch
    def save_score(self, score: int) -> bool:
        self.saved.append(score)
        if score > self.high_score:
            self.high_score = score
        return False
    Dummy.save_score = save_score  # type: ignore

    monkeypatch.setattr(cli, "ScoreManager", Dummy)
    monkeypatch.setattr(cli, "generate_next_note", lambda diff: 1)
    monkeypatch.setattr(cli, "play_sequence", lambda seq, use_audio=False: None)

    inputs = iter(["not numbers", "n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    cli.main(["--levels", "2"])
    out = capsys.readouterr().out
    assert "Invalid input, numbers only. Game over." in out
    assert Dummy.instances[0].saved == [0]


def test_cli_level_progress_and_score_update(monkeypatch, capsys):
    Dummy = _make_dummy_manager()
    monkeypatch.setattr(cli, "ScoreManager", Dummy)

    notes = iter([1, 2])
    monkeypatch.setattr(cli, "generate_next_note", lambda diff: next(notes))
    monkeypatch.setattr(cli, "play_sequence", lambda seq, use_audio=False: None)

    inputs = iter(["1", "1 2", "n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    cli.main(["--levels", "2"])
    out = capsys.readouterr().out
    assert "Level 2. Listen to the sequence:" in out
    assert "Congratulations! You completed all levels." in out
    assert "New high score: 2!" in out
    assert Dummy.instances[0].saved == [2]
