"""Indoor vs outdoor unique-aircraft comparison helpers.

Counts are reader-recorded integers from local decoder UIs.
This module does not invent aircraft or talk to hardware.
"""

from __future__ import annotations


def count_delta(indoor_count: int, outdoor_count: int) -> int:
    """Return outdoor minus indoor unique-aircraft counts."""
    return outdoor_count - indoor_count


def prefer_site(indoor_count: int, outdoor_count: int) -> str:
    """Return 'outdoor', 'indoor', or 'tie' from unique counts."""
    if indoor_count == outdoor_count:
        return "tie"
    if outdoor_count > indoor_count:
        return "outdoor"
    return "indoor"


def summarize_sites(
    indoor_count: int,
    outdoor_count: int,
    label_indoor: str = "indoor",
    label_outdoor: str = "outdoor",
) -> str:
    """Return a one-line summary of an indoor/outdoor comparison."""
    if indoor_count < 0 or outdoor_count < 0:
        raise ValueError("counts must be >= 0")
    delta = count_delta(indoor_count, outdoor_count)
    winner = prefer_site(indoor_count, outdoor_count)
    if winner == "tie":
        preferred = "tie"
    elif winner == "outdoor":
        preferred = label_outdoor
    else:
        preferred = label_indoor
    return (
        f"{label_indoor}={indoor_count} {label_outdoor}={outdoor_count} "
        f"delta={delta} preferred={preferred}"
    )
