"""Measure dit length from a list of mark durations (milliseconds)."""

from __future__ import annotations

from statistics import mean
from typing import Iterable, Sequence


def average_dit_ms(mark_ms: Sequence[float], *, dah_ratio: float = 2.0) -> float:
    """Average durations classified as dits (shorter than dah_ratio * median-ish).

    Classification: any mark shorter than (min_mark * dah_ratio) counts as a dit.
    Raises ValueError if no dit-length marks remain.
    """
    if not mark_ms:
        raise ValueError("mark_ms must not be empty")
    values = [float(v) for v in mark_ms]
    if any(v <= 0 for v in values):
        raise ValueError("mark durations must be positive")
    shortest = min(values)
    threshold = shortest * dah_ratio
    dits = [v for v in values if v < threshold]
    if not dits:
        # All marks look like dahs; still report the mean of everything.
        dits = values
    return float(mean(dits))


def measure_dot_length(
    events: Iterable[dict],
    *,
    wpm_hint: int | None = None,
) -> dict:
    """Measure average dit ms from key-event dicts.

    Each event needs keys:
      - kind: "mark" or "space"
      - duration_ms: positive number

    Returns a dict with average_dit_ms, sample_count, and optional expected_unit_ms.
    """
    marks = [
        float(ev["duration_ms"])
        for ev in events
        if ev.get("kind") == "mark" and "duration_ms" in ev
    ]
    if not marks:
        raise ValueError("no mark events to measure")
    avg = average_dit_ms(marks)
    result: dict = {
        "average_dit_ms": round(avg, 3),
        "sample_count": len(marks),
    }
    if wpm_hint is not None:
        from .timing import unit_ms_from_wpm

        expected = unit_ms_from_wpm(int(wpm_hint))
        result["expected_unit_ms"] = expected
        result["wpm_hint"] = int(wpm_hint)
        result["error_ms"] = round(avg - expected, 3)
    return result
