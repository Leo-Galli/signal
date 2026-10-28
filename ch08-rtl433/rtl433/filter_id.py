"""Filter rtl_433 JSON records by device id.

Does not talk to hardware. Operates on dicts the reader already logged.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def normalize_id(value: Any) -> str:
    """Return a stable string form of a device id."""
    if value is None:
        return ""
    return str(value).strip()


def filter_by_device_id(
    records: Sequence[Mapping[str, Any]],
    device_id: Any,
) -> list[dict[str, Any]]:
    """Return copies of records whose id matches device_id."""
    want = normalize_id(device_id)
    if not want:
        raise ValueError("device_id must be non-empty")
    matched: list[dict[str, Any]] = []
    for entry in records:
        if normalize_id(entry.get("id")) == want:
            matched.append(dict(entry))
    return matched


def unique_ids(records: Sequence[Mapping[str, Any]]) -> list[str]:
    """Return sorted unique id strings seen in records."""
    seen: set[str] = set()
    for entry in records:
        value = normalize_id(entry.get("id"))
        if value:
            seen.add(value)
    return sorted(seen)
