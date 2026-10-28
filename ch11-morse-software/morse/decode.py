"""Simple envelope Morse decoder for clean practice audio.

Designed for noise-free (or near noise-free) tones produced by this chapter's
encoder. It measures mark/space lengths in PARIS units and maps them back to
letters. It is not a contest-grade CW skimmer.
"""

from __future__ import annotations

from array import array
from pathlib import Path

from morse.alphabet import INTERNATIONAL_MORSE, PROSIGNS, PUNCTUATION
from morse.audio import read_wav
from morse.timing import unit_seconds


def _build_lookup(*, include_prosigns: bool) -> dict[str, str]:
    """Map dit/dah patterns to printable characters / <PROSIGN> tokens."""
    lookup: dict[str, str] = {}
    for char, pattern in INTERNATIONAL_MORSE.items():
        lookup[pattern] = char
    for char, pattern in PUNCTUATION.items():
        # Prefer letter alphabet over punctuation aliases when identical.
        lookup.setdefault(pattern, char)
    if include_prosigns:
        for name, pattern in PROSIGNS.items():
            lookup[pattern] = f"<{name}>"
    return lookup


def _smooth_abs_envelope(pcm: array, window: int) -> list[float]:
    """Rectify PCM and apply a short moving average to kill sine zero-crossings."""
    n = len(pcm)
    if n == 0:
        return []
    window = max(1, window)
    abs_vals = [abs(sample) for sample in pcm]
    # Prefix sums for O(n) moving average.
    prefix = [0.0]
    running = 0.0
    for value in abs_vals:
        running += value
        prefix.append(running)
    half = window // 2
    env: list[float] = []
    for i in range(n):
        left = max(0, i - half)
        right = min(n, i + half + 1)
        env.append((prefix[right] - prefix[left]) / (right - left))
    return env


def envelope_on_off(
    pcm: array,
    *,
    sample_rate: int,
    threshold_ratio: float = 0.25,
    smooth_ms: float = 5.0,
) -> list[tuple[bool, float]]:
    """Convert PCM to (tone_on, duration_seconds) via a smoothed envelope."""
    if not pcm:
        return []
    window = max(1, int(round(sample_rate * smooth_ms / 1000.0)))
    env = _smooth_abs_envelope(pcm, window)
    peak = max(env) if env else 0.0
    if peak == 0:
        return [(False, len(pcm) / sample_rate)]
    threshold = peak * threshold_ratio

    segments: list[tuple[bool, float]] = []
    current_on = env[0] >= threshold
    run = 1
    for value in env[1:]:
        on = value >= threshold
        if on == current_on:
            run += 1
            continue
        segments.append((current_on, run / sample_rate))
        current_on = on
        run = 1
    segments.append((current_on, run / sample_rate))

    # Drop micro-gaps shorter than ~0.3 unit at 40 WPM (~7.5 ms) by merging.
    min_keep = 0.0075
    merged: list[tuple[bool, float]] = []
    for on, dur in segments:
        if merged and dur < min_keep:
            prev_on, prev_dur = merged[-1]
            merged[-1] = (prev_on, prev_dur + dur)
            continue
        if merged and merged[-1][0] == on:
            prev_on, prev_dur = merged[-1]
            merged[-1] = (on, prev_dur + dur)
            continue
        merged.append((on, dur))
    return merged


def _estimate_unit(segments: list[tuple[bool, float]]) -> float:
    """Estimate dit length from the shortest tone-on mark."""
    ons = [dur for on, dur in segments if on and dur > 1e-4]
    if not ons:
        raise ValueError("no tone marks found")
    # Use a robust low percentile: median of the shortest half of marks.
    ons_sorted = sorted(ons)
    half = ons_sorted[: max(1, len(ons_sorted) // 2)]
    return sum(half) / len(half)


def segments_to_text(
    segments: list[tuple[bool, float]],
    *,
    unit: float | None = None,
    include_prosigns: bool = True,
    wpm_hint: float | None = None,
) -> str:
    """Decode an on/off timeline into text."""
    if not segments:
        return ""

    if unit is None:
        if wpm_hint is not None:
            unit = unit_seconds(wpm_hint)
        else:
            unit = _estimate_unit(segments)

    lookup = _build_lookup(include_prosigns=include_prosigns)
    # Thresholds in units (midpoints between 1/3 and 3/7).
    mark_dash_min = 2.0
    gap_char_min = 2.0
    gap_word_min = 5.0

    pattern = ""
    letters: list[str] = []

    def flush_char() -> None:
        nonlocal pattern
        if not pattern:
            return
        letters.append(lookup.get(pattern, "?"))
        pattern = ""

    for tone_on, duration in segments:
        units = duration / unit
        if tone_on:
            if units >= mark_dash_min:
                pattern += "-"
            else:
                pattern += "."
            continue
        # Silence
        if units < gap_char_min:
            # Intra-element gap -- continue building the character.
            continue
        if units < gap_word_min:
            flush_char()
            continue
        # Word gap
        flush_char()
        if letters and letters[-1] != " ":
            letters.append(" ")

    flush_char()
    while letters and letters[-1] == " ":
        letters.pop()
    return "".join(letters)


def decode_pcm(
    pcm: array,
    *,
    sample_rate: int,
    include_prosigns: bool = True,
    wpm_hint: float | None = None,
) -> str:
    """Decode mono PCM Morse audio to text."""
    segments = envelope_on_off(pcm, sample_rate=sample_rate)
    return segments_to_text(
        segments,
        include_prosigns=include_prosigns,
        wpm_hint=wpm_hint,
    )


def decode_wav_file(
    path: Path | str,
    *,
    include_prosigns: bool = True,
    wpm_hint: float | None = None,
) -> str:
    """Decode a mono 16-bit WAV file to text."""
    pcm, sample_rate = read_wav(path)
    return decode_pcm(
        pcm,
        sample_rate=sample_rate,
        include_prosigns=include_prosigns,
        wpm_hint=wpm_hint,
    )
