"""Validate indoor RSSI-vs-distance session logs (reader-measured only)."""

from __future__ import annotations

from typing import Any


REQUIRED_TOP = (
    "session_id",
    "module",
    "sf",
    "bw_khz",
    "tx_dbm",
    "duty_cycle_percent",
    "points",
)

REQUIRED_POINT = ("distance_m", "rssi_dbm", "snr_db", "seq")


def validate_rssi_log(doc: dict[str, Any]) -> list[str]:
    """Return a list of error strings; empty means OK."""
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

    points = doc.get("points")
    if not isinstance(points, list) or len(points) == 0:
        errors.append("points must be a non-empty list")
        return errors

    for i, pt in enumerate(points):
        if not isinstance(pt, dict):
            errors.append(f"points[{i}] must be an object")
            continue
        for key in REQUIRED_POINT:
            if key not in pt:
                errors.append(f"points[{i}] missing {key}")
        if "distance_m" in pt and not isinstance(pt["distance_m"], (int, float)):
            errors.append(f"points[{i}].distance_m must be a number")
        if "rssi_dbm" in pt and not isinstance(pt["rssi_dbm"], (int, float)):
            errors.append(f"points[{i}].rssi_dbm must be a number")

    return errors
