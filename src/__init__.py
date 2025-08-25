"""Utilities for the musical memory game.

This module exposes the primary interfaces used throughout the project so
that they can be easily imported for use in applications or tests.
"""

from .game import (
    NOTES,
    check_sequence,
    generate_level_sequence,
    generate_sequence,
    sequence_length,
)

__all__ = [
    "NOTES",
    "generate_sequence",
    "check_sequence",
    "sequence_length",
    "generate_level_sequence",
]
