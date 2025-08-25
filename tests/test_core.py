import os
import sys
import pytest

# Ensure the package root is on the path when tests run from the tests directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from musical_memory import MusicalMemory


def test_add_and_recall_notes():
    memory = MusicalMemory()
    memory.add_note("C")
    memory.add_note("D")
    assert memory.recall() == ["C", "D"]


def test_recall_returns_copy():
    memory = MusicalMemory()
    memory.add_note("E")
    returned = memory.recall()
    returned.append("F")
    assert memory.recall() == ["E"]


def test_add_note_validation():
    memory = MusicalMemory()
    with pytest.raises(ValueError):
        memory.add_note(1)  # type: ignore
    with pytest.raises(ValueError):
        memory.add_note("")


def test_clear_memory():
    memory = MusicalMemory()
    memory.add_note("G")
    memory.clear()
    assert memory.recall() == []
