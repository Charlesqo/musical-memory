"""Simple module for managing a sequence of musical notes."""

from typing import List


class MusicalMemory:
    """Store and recall a sequence of musical notes.

    Notes are represented as strings.
    """

    def __init__(self) -> None:
        self._sequence: List[str] = []

    def add_note(self, note: str) -> None:
        """Add a note to the memory.

        Args:
            note: A non-empty string representing a musical note.

        Raises:
            ValueError: If ``note`` is not a non-empty string.
        """
        if not isinstance(note, str) or not note:
            raise ValueError("note must be a non-empty string")
        self._sequence.append(note)

    def recall(self) -> List[str]:
        """Return a copy of the stored sequence."""
        return list(self._sequence)

    def clear(self) -> None:
        """Clear the stored sequence."""
        self._sequence.clear()
