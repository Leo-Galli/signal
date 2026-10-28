"""PARIS timing helpers for encode and decode."""

from __future__ import annotations


def unit_seconds(wpm: float) -> float:
    """Return the PARIS unit (dit) length in seconds for a given WPM."""
    if wpm <= 0:
        raise ValueError("wpm must be positive")
    return 1.2 / wpm


def standard_gaps() -> dict[str, int]:
    """Return standard Morse gap lengths in units."""
    return {
        "intra_element": 1,
        "inter_character": 3,
        "inter_word": 7,
    }
