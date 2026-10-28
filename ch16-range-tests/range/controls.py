"""Validate locked control-variable sheets for one range-walk session."""

from __future__ import annotations

from typing import Any

REQUIRED = (
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
)

ALLOWED_DISTANCE_METHODS = frozenset({"gps", "wheel", "paced"})


def validate_controls(doc: dict[str, Any]) -> list[str]:
    """Return error strings; empty means OK."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be an object"]

    for key in REQUIRED:
        if key not in doc:
            errors.append(f"missing field: {key}")

    if errors:
        return errors

    if not str(doc.get("session_id", "")).strip():
        errors.append("session_id must be non-empty")
    if not str(doc.get("date", "")).strip():
        errors.append("date must be non-empty")
    if not str(doc.get("region", "")).strip():
        errors.append("region must be non-empty")

    for key in ("sf", "bw_khz", "cr", "tx_dbm", "payload_bytes"):
        value = doc.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{key} must be a number")

    sf = doc.get("sf")
    if isinstance(sf, (int, float)) and not isinstance(sf, bool):
        if int(sf) < 7 or int(sf) > 12:
            errors.append("sf must be between 7 and 12")

    method = str(doc.get("distance_method", "")).strip().lower()
    if method not in ALLOWED_DISTANCE_METHODS:
        errors.append("distance_method must be gps, wheel, or paced")

    for key in ("antenna_fixed", "antenna_walking"):
        if not str(doc.get(key, "")).strip():
            errors.append(f"{key} must be non-empty")

    for key in ("height_fixed_m", "height_walking_m"):
        value = doc.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{key} must be a number")
        elif float(value) < 0:
            errors.append(f"{key} must be >= 0")

    return errors
