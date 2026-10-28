"""Field checklist and 5 V rail-verify log validation for Chapter 2.

These helpers check that required safety fields are present and non-empty.
They do not invent fuse ratings, diode drops or RF exposure numbers.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_CHECKLIST_FIELDS = (
    "power_source",
    "polarity_marked",
    "fuse_value",
    "antenna_inspected",
    "stop_condition",
)

REQUIRED_RAIL_LOG_FIELDS = (
    "fuse_continuity",
    "diode_orientation",
    "measured_rail_volts",
    "reverse_hold_pass",
    "notes",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...] | None = None) -> list[str]:
    """Return names of required fields that are missing or blank."""
    names = required if required is not None else REQUIRED_CHECKLIST_FIELDS
    missing: list[str] = []
    for name in names:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def validate_checklist(doc: Mapping[str, Any]) -> list[str]:
    """Return missing field names for a field checklist document."""
    return missing_fields(doc, REQUIRED_CHECKLIST_FIELDS)


def validate_rail_log(doc: Mapping[str, Any]) -> list[str]:
    """Return missing field names for a 5 V rail verify log."""
    return missing_fields(doc, REQUIRED_RAIL_LOG_FIELDS)
