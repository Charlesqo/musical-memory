import pytest
from src import game


def test_generate_sequence_negative_length():
    with pytest.raises(ValueError):
        game.generate_sequence(-1)


def test_generate_level_sequence_length_increments(monkeypatch):
    monkeypatch.setattr(game.random, "choice", lambda seq: seq[0])
    seq1 = game.generate_level_sequence(1, base_length=2, step=2, notes=[1])
    seq3 = game.generate_level_sequence(3, base_length=2, step=2, notes=[1])
    assert len(seq1) == 2
    assert len(seq3) == 6  # 2 + (3-1)*2


def test_play_sequence_uses_mocked_audio(monkeypatch):
    calls = []

    def fake_play(freq):
        calls.append(freq)

    monkeypatch.setattr(game, "_play_tone", fake_play)
    # avoid actual sleeping if fallback is used
    monkeypatch.setattr(game.time, "sleep", lambda *_: None)
    sequence = [1, 2]
    game.play_sequence(sequence, use_audio=True, delay=0)
    expected = [game._freq_of(1), game._freq_of(2)]
    assert calls == expected


def test_check_sequence():
    assert game.check_sequence([1, 2], [1, 2])
    assert not game.check_sequence([1, 2], [2, 1])
