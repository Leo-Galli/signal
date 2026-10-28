"""Validate five-point range-walk results (blank cells allowed; no invented ranges)."""

from __future__ import annotations

from typing import Any

REQUIRED_TOP = (
    "session_id",
    "date",
    "region",
    "sf",
    "bw_khz",
    "cr",
    "tx_dbm",
    "payload_bytes",
    "antenna_fixed",
    "antenna_walking",
    "height_fixed_m",
    "height_walking_m",
    "distance_method",
    "points",
    "limitation_note",
)

POINT_KEYS = (
    "index",
    "time",
    "distance_m",
    "lat",
    "lon",
    "rssi_dbm",
    "snr_db",
    "decode_ok",
    "notes",
)

OPTIONAL_NUMERIC = ("distance_m", "lat", "lon", "rssi_dbm", "snr_db")


def _is_number_or_null(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def validate_results(doc: dict[str, Any]) -> list[str]:
    """Return error strings; empty means OK.

    Blank measurement cells are represented as null. Invented range claims are
    rejected via invented_ranges=true or a missing limitation note.
    """
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be an object"]

    for key in REQUIRED_TOP:
        if key not in doc:
            errors.append(f"missing top-level field: {key}")

    if errors:
        return errors

    if doc.get("invented_ranges") is True:
        errors.append("invented_ranges must not be true; log only your measurements")

    if not str(doc.get("session_id", "")).strip():
        errors.append("session_id must be non-empty")

    note = doc.get("limitation_note")
    if not isinstance(note, str) or not note.strip():
        errors.append("limitation_note must be a non-empty string")

    points = doc.get("points")
    if not isinstance(points, list):
        errors.append("points must be a list")
        return errors
    if len(points) != 5:
        errors.append("points must contain exactly 5 entries")

    seen: set[int] = set()
    for i, pt in enumerate(points):
        if not isinstance(pt, dict):
            errors.append(f"points[{i}] must be an object")
            continue
        for key in POINT_KEYS:
            if key not in pt:
                errors.append(f"points[{i}] missing {key}")

        idx = pt.get("index")
        if not isinstance(idx, int) or isinstance(idx, bool):
            errors.append(f"points[{i}].index must be an int")
        else:
            if idx < 1 or idx > 5:
                errors.append(f"points[{i}].index must be 1..5")
            if idx in seen:
                errors.append(f"duplicate points index: {idx}")
            seen.add(idx)

        for key in OPTIONAL_NUMERIC:
            if key in pt and not _is_number_or_null(pt.get(key)):
                errors.append(f"points[{i}].{key} must be a number or null")

        decode_ok = pt.get("decode_ok")
        if decode_ok is not None and not isinstance(decode_ok, bool):
            errors.append(f"points[{i}].decode_ok must be bool or null")

        if "time" in pt and pt["time"] is not None and not isinstance(pt["time"], str):
            errors.append(f"points[{i}].time must be a string or null")
        if "notes" in pt and pt["notes"] is not None and not isinstance(pt["notes"], str):
            errors.append(f"points[{i}].notes must be a string or null")

    if len(points) == 5 and seen and seen != {1, 2, 3, 4, 5}:
        errors.append("points indexes must be exactly 1..5")

    return errors
