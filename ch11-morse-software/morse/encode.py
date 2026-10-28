"""Text to Morse element sequences and on/off keying timelines."""

from __future__ import annotations

from typing import Iterable

from morse.alphabet import PROSIGNS, encode_symbol
from morse.timing import standard_gaps, unit_seconds


def tokenize_text(text: str, *, include_prosigns: bool = True) -> list[str]:
    """Split text into Morse symbols.

    Whitespace collapses to a single word break. Prosign tokens may be
    written as <AR>, <SK>, <BT>, <KN>, <AS>, or <SOS> (angle brackets).
    Other characters must be letters, digits or supported punctuation.
    """
    tokens: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            if tokens and tokens[-1] != " ":
                tokens.append(" ")
            i += 1
            continue
        if ch == "<" and include_prosigns:
            end = text.find(">", i + 1)
            if end < 0:
                raise ValueError("unclosed prosign bracket")
            name = text[i + 1 : end].strip().upper()
            if name not in PROSIGNS:
                raise ValueError(f"unknown prosign: {name!r}")
            tokens.append(name)
            i = end + 1
            continue
        tokens.append(ch.upper() if ch.isalpha() else ch)
        i += 1
    while tokens and tokens[0] == " ":
        tokens.pop(0)
    while tokens and tokens[-1] == " ":
        tokens.pop()
    return tokens


def text_to_elements(
    text: str,
    *,
    include_prosigns: bool = True,
) -> list[str]:
    """Return a flat list of dit/dah marks with gap markers.

    Marks are '.' or '-'. Inter-character gaps are ''. Word gaps are ' '.
    """
    tokens = tokenize_text(text, include_prosigns=include_prosigns)
    elements: list[str] = []
    for token in tokens:
        if token == " ":
            elements.append(" ")
            continue
        if elements and elements[-1] != " ":
            elements.append("")
        pattern = encode_symbol(token, include_prosigns=include_prosigns)
        elements.extend(list(pattern))
    return elements


def elements_to_on_off(
    elements: Iterable[str],
    *,
    wpm: float,
    timing_scale: float = 1.0,
) -> list[tuple[bool, float]]:
    """Expand element markers into (tone_on, duration_seconds) segments.

    timing_scale multiplies all durations (use 0.9 / 1.1 for +/- 10% fuzz).
    """
    if timing_scale <= 0:
        raise ValueError("timing_scale must be positive")
    unit = unit_seconds(wpm) * timing_scale
    gaps = standard_gaps()
    segments: list[tuple[bool, float]] = []
    marks_in_char = 0

    for item in elements:
        if item in (".", "-"):
            if marks_in_char > 0:
                segments.append((False, unit * gaps["intra_element"]))
            duration = unit * (1 if item == "." else 3)
            segments.append((True, duration))
            marks_in_char += 1
            continue
        if item == "":
            marks_in_char = 0
            if segments:
                segments.append((False, unit * gaps["inter_character"]))
            continue
        if item == " ":
            marks_in_char = 0
            if segments:
                segments.append((False, unit * gaps["inter_word"]))
            continue
        raise ValueError(f"unknown element token: {item!r}")

    return segments


def text_to_on_off(
    text: str,
    *,
    wpm: float,
    timing_scale: float = 1.0,
    include_prosigns: bool = True,
) -> list[tuple[bool, float]]:
    """Encode text straight to an on/off timeline."""
    elements = text_to_elements(text, include_prosigns=include_prosigns)
    return elements_to_on_off(elements, wpm=wpm, timing_scale=timing_scale)
