"""Morse timing helpers using the PARIS standard and Farnsworth spacing.

PARIS at N words per minute uses 50 units per word, so one unit (dot length)
is 1.2 / N seconds. Farnsworth keeps character-internal timing at a higher
character speed while stretching inter-character and inter-word gaps so the
overall (effective) rate is slower.
"""

from __future__ import annotations

from typing import Any, Mapping


def unit_seconds(wpm: float) -> float:
    """Return the PARIS unit (dot) length in seconds for a given WPM."""
    if wpm <= 0:
        raise ValueError("wpm must be positive")
    return 1.2 / wpm


def units_for_element(element: str) -> int:
    """Return PARIS units for a single Morse element symbol."""
    mapping = {
        ".": 1,
        "-": 3,
        " ": 1,  # intra-character element gap is handled separately
    }
    if element not in mapping:
        raise ValueError(f"unknown element: {element!r}")
    return mapping[element]


def farnsworth_gap_units(
    character_wpm: float,
    effective_wpm: float,
) -> tuple[float, float]:
    """Return (inter-character gap units, inter-word gap units) for Farnsworth.

    Character-internal timing uses character_wpm. Extra delay is placed in the
    gaps between characters and words so the overall rate matches effective_wpm.

    Uses the common ARRL / LCWO-style stretch: total extra delay per PARIS word
    is distributed across the standard 5 inter-character gaps and 1 inter-word
    gap of the word PARIS (4 letters + word space), keeping the same ratio as
    standard Morse (3-unit character gaps, 7-unit word gaps).
    """
    if character_wpm <= 0 or effective_wpm <= 0:
        raise ValueError("speeds must be positive")
    if effective_wpm > character_wpm:
        raise ValueError("effective_wpm cannot exceed character_wpm")

    # Standard PARIS word = 50 units at one speed.
    # Time for one word at effective speed, minus time if sent entirely at
    # character speed, is the delay that must live in the stretched gaps.
    t_char_unit = unit_seconds(character_wpm)
    t_word_effective = 60.0 / effective_wpm
    t_word_at_char = 50.0 * t_char_unit
    extra_seconds = t_word_effective - t_word_at_char
    if extra_seconds < -1e-9:
        raise ValueError("inconsistent Farnsworth speeds")
    if abs(extra_seconds) < 1e-12:
        return (3.0, 7.0)

    # PARIS has 4 inter-character gaps and 1 inter-word gap.
    # Keep the 3:7 ratio between character-gap and word-gap stretch units.
    # Total "gap weight" = 4*3 + 7 = 19 units of standard spacing already in
    # the 50; we instead solve for stretched gap lengths in character-speed units.
    # Standard approach: extra delay distributed proportional to 3 and 7.
    # 4 * ic + iw = extra_seconds / t_char_unit + (4*3 + 7)
    # with iw / ic = 7/3
    extra_units = extra_seconds / t_char_unit
    # Base standard gaps already counted inside the 50-unit PARIS figure, so
    # the stretched gaps replace the standard 3 and 7 -- total gap units become:
    # 4 * ic + iw = (4*3 + 7) + extra_units = 19 + extra_units
    total_gap_units = 19.0 + extra_units
    # iw = (7/3) * ic; 4*ic + (7/3)*ic = (12/3 + 7/3)*ic = (19/3)*ic
    ic = total_gap_units * 3.0 / 19.0
    iw = ic * 7.0 / 3.0
    return (ic, iw)


def timing_report(character_wpm: float, effective_wpm: float) -> dict[str, float]:
    """Return a dict of useful Farnsworth timing numbers for worksheets."""
    unit = unit_seconds(character_wpm)
    ic, iw = farnsworth_gap_units(character_wpm, effective_wpm)
    return {
        "character_wpm": float(character_wpm),
        "effective_wpm": float(effective_wpm),
        "dot_seconds": unit,
        "dash_seconds": 3.0 * unit,
        "intra_element_gap_seconds": unit,
        "inter_character_gap_units": ic,
        "inter_word_gap_units": iw,
        "inter_character_gap_seconds": ic * unit,
        "inter_word_gap_seconds": iw * unit,
    }


def validate_timing_params(doc: Mapping[str, Any]) -> list[str]:
    """Validate a timing JSON document used by the Farnsworth worksheet tool."""
    problems: list[str] = []
    for name in ("character_wpm", "effective_wpm"):
        if name not in doc:
            problems.append(name)
            continue
        try:
            value = float(doc[name])
        except (TypeError, ValueError):
            problems.append(name)
            continue
        if value <= 0:
            problems.append(name)
    if problems:
        return problems
    char_wpm = float(doc["character_wpm"])
    eff_wpm = float(doc["effective_wpm"])
    if eff_wpm > char_wpm:
        return ["effective_wpm"]
    return []
