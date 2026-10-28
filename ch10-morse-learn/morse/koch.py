"""Koch character introduction order used by many CW trainers.

Sequence matches the common Learn CW Online (LCWO) Koch lesson order for the
first 40 symbols (letters, digits and a few punctuation marks). Individual
trainers may differ slightly; treat this as a practice reference, not a rule.
"""

from __future__ import annotations

# LCWO-style Koch order (40 symbols), widely published for computer tutors.
KOCH_ORDER = tuple("KMURESNAPTLWI.JZ=FOY,VG5/Q92H380B?47C1D6X")


def characters_through_lesson(lesson: int) -> tuple[str, ...]:
    """Return the Koch characters introduced through a 1-based lesson index."""
    if lesson < 1 or lesson > len(KOCH_ORDER):
        raise ValueError(f"lesson must be 1..{len(KOCH_ORDER)}")
    return KOCH_ORDER[:lesson]


def lesson_for_character(char: str) -> int:
    """Return 1-based lesson index when a character is introduced."""
    symbol = char.upper() if len(char) == 1 and char.isalpha() else char
    try:
        return KOCH_ORDER.index(symbol) + 1
    except ValueError as exc:
        raise ValueError(f"character not in Koch order: {char!r}") from exc
