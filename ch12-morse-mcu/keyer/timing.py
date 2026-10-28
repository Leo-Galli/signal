"""PARIS timing helpers matching the firmware unit model."""

from __future__ import annotations


def unit_seconds(wpm: float) -> float:
    """Return the PARIS unit (dit) length in seconds for a given WPM."""
    if wpm <= 0:
        raise ValueError("wpm must be positive")
    return 1.2 / float(wpm)


def unit_ms_from_wpm(wpm: int) -> int:
    """Return the PARIS unit length in milliseconds (integer, firmware style)."""
    if wpm < 5:
        wpm = 5
    return 1200 // int(wpm)


def clamp_wpm(value: int) -> int:
    """Clamp WPM into the firmware range 5..40."""
    if value < 5:
        return 5
    if value > 40:
        return 40
    return int(value)
