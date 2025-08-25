import random
from typing import Iterable, List, Sequence

# Default notes available in the game. They can be overridden when calling
# the generation functions if a different set of notes is desired.
NOTES: Sequence[str] = ("C", "D", "E", "F", "G", "A", "B")

def generate_sequence(length: int, notes: Sequence[str] = NOTES) -> List[str]:
    """Generate a random sequence of musical notes.

    Args:
        length: Number of notes to generate.
        notes: Collection of possible notes.

    Returns:
        List of randomly chosen notes.
    """
    notes_list = list(notes)
    if length < 0:
        raise ValueError("length must be non-negative")
    return [random.choice(notes_list) for _ in range(length)]


def sequence_length(level: int, base_length: int = 3, step: int = 1) -> int:
    """Determine the sequence length for a given level.

    The sequence grows with each level to make the game progressively more
    challenging.

    Args:
        level: Current level (starting from 1).
        base_length: Sequence length for level 1.
        step: How much the sequence length increases per level.

    Returns:
        Calculated sequence length for the level.
    """
    if level < 1:
        raise ValueError("level must be at least 1")
    return base_length + (level - 1) * step


def generate_level_sequence(level: int, base_length: int = 3, step: int = 1,
                             notes: Sequence[str] = NOTES) -> List[str]:
    """Generate a sequence for the specified level.

    The length of the sequence is derived from :func:`sequence_length` so that
    it increases with each level.

    Args:
        level: The current level of the game (1-indexed).
        base_length: Starting sequence length at level 1.
        step: Additional notes added per level.
        notes: Collection of notes to choose from.

    Returns:
        Randomly generated sequence for the level.
    """
    length = sequence_length(level, base_length=base_length, step=step)
    return generate_sequence(length, notes)


def check_sequence(user_input: Iterable[str], expected: Iterable[str]) -> bool:
    """Check whether the player's input matches the expected sequence.

    Args:
        user_input: Sequence of notes provided by the player.
        expected: The correct sequence of notes.

    Returns:
        ``True`` if the input matches the expected sequence exactly, otherwise
        ``False``.
    """
    return list(user_input) == list(expected)
