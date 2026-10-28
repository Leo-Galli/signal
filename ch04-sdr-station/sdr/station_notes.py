"""Station notes validation for Chapter 4.

Checks required fields for a repeatable receive-only SDR setup.
Does not talk to hardware and does not invent measurements.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_STATION_FIELDS = (
    "software_name",
    "software_version",
    "device_name",
    "sample_rate_hz",
    "ppm_correction",
    "default_gain",
    "antenna_notes",
    "last_expected_mhz",
    "last_measured_mhz",
    "iq_recording_path",
    "iq_duration_s",
    "access_date",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...] | None = None) -> list[str]:
    """Return names of required fields that are missing or blank."""
    names = required if required is not None else REQUIRED_STATION_FIELDS
    missing: list[str] = []
    for name in names:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def _non_positive_number(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return True
    return number <= 0


def _not_number(value: Any) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return True
    return False


def validate_station_notes(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a station notes document."""
    problems = missing_fields(doc, REQUIRED_STATION_FIELDS)
    if problems:
        return problems

    if _non_positive_number(doc.get("sample_rate_hz")):
        return ["sample_rate_hz"]
    if _not_number(doc.get("ppm_correction")):
        return ["ppm_correction"]
    if _non_positive_number(doc.get("last_expected_mhz")):
        return ["last_expected_mhz"]
    if _non_positive_number(doc.get("last_measured_mhz")):
        return ["last_measured_mhz"]
    if _non_positive_number(doc.get("iq_duration_s")):
        return ["iq_duration_s"]

    return []
