"""Pass-prediction / capture-log validation for Chapter 7.

Checks required fields for receive-only weather-sat practice notes.
Does not talk to hardware and does not invent passes or imagery.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

REQUIRED_LOG_FIELDS = (
    "access_date",
    "jurisdiction_note",
    "tle_source_url",
    "decoder_or_tool",
    "passes",
)

REQUIRED_PASS_FIELDS = (
    "label",
    "satellite_name",
    "predicted_aos_utc",
    "predicted_los_utc",
    "max_elevation_deg",
    "antenna_position",
    "outcome",
)

ALLOWED_OUTCOMES = frozenset(
    {
        "predicted-only",
        "practice-wav-decoded",
        "live-capture-decoded",
        "live-attempt-failed",
        "skipped-no-active-apt",
    }
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def _bad_elevation(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return True
    return number < 0 or number > 90


def validate_pass(entry: Mapping[str, Any], index: int) -> list[str]:
    """Return problem labels for one pass entry."""
    prefix = f"passes[{index}]"
    problems = missing_fields(entry, REQUIRED_PASS_FIELDS)
    if problems:
        return [f"{prefix}.{name}" for name in problems]

    if _bad_elevation(entry.get("max_elevation_deg")):
        return [f"{prefix}.max_elevation_deg"]

    outcome = str(entry.get("outcome", "")).strip()
    if outcome not in ALLOWED_OUTCOMES:
        return [f"{prefix}.outcome"]

    return []


def validate_pass_log(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a weather-sat pass-log document."""
    problems = missing_fields(doc, REQUIRED_LOG_FIELDS)
    if problems:
        return problems

    passes = doc.get("passes")
    if not isinstance(passes, Sequence) or isinstance(passes, (str, bytes)):
        return ["passes"]
    if len(passes) == 0:
        return ["passes"]

    for index, entry in enumerate(passes):
        if not isinstance(entry, Mapping):
            return [f"passes[{index}]"]
        entry_problems = validate_pass(entry, index)
        if entry_problems:
            return entry_problems

    return []
