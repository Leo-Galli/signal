"""Temperature series helpers from rtl_433 JSON records.

Looks for common Celsius fields used by many weather / thermometer protocols.
Does not invent readings and does not talk to hardware.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

TEMP_C_KEYS = (
    "temperature_C",
    "temperature_c",
    "temp_C",
    "temp_c",
)


def extract_celsius(entry: Mapping[str, Any]) -> float | None:
    """Return temperature in Celsius if a known field is present."""
    for key in TEMP_C_KEYS:
        if key not in entry or entry.get(key) is None:
            continue
        try:
            return float(entry[key])
        except (TypeError, ValueError):
            return None
    return None


def temperature_series(
    records: Sequence[Mapping[str, Any]],
) -> list[tuple[str, float]]:
    """Return (time, temp_C) pairs for records that carry Celsius."""
    series: list[tuple[str, float]] = []
    for entry in records:
        temp = extract_celsius(entry)
        if temp is None:
            continue
        time_label = str(entry.get("time", "")).strip() or "unknown"
        series.append((time_label, temp))
    return series


def summarize_series(series: Sequence[tuple[str, float]]) -> dict[str, float | int | str]:
    """Return min/max/mean and count for a temperature series."""
    if not series:
        raise ValueError("series is empty")
    values = [temp for _, temp in series]
    return {
        "count": len(values),
        "min_c": min(values),
        "max_c": max(values),
        "mean_c": sum(values) / len(values),
        "first_time": series[0][0],
        "last_time": series[-1][0],
    }


def format_summary(series: Sequence[tuple[str, float]]) -> str:
    """Return a one-line temperature summary."""
    stats = summarize_series(series)
    return (
        f"count={stats['count']} min_c={stats['min_c']:.2f} "
        f"max_c={stats['max_c']:.2f} mean_c={stats['mean_c']:.2f} "
        f"from={stats['first_time']} to={stats['last_time']}"
    )
