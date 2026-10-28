"""ADS-B session-log validation for Chapter 6.

Checks required fields for receive-only 1090 MHz practice notes.
Does not talk to hardware and does not invent aircraft.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

REQUIRED_LOG_FIELDS = (
    "access_date",
    "jurisdiction_note",
    "decoder_name",
    "map_ui",
    "sessions",
)

REQUIRED_SESSION_FIELDS = (
    "label",
    "antenna_position",
    "duration_minutes",
    "unique_aircraft",
    "start_time",
    "end_time",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def _bad_non_negative_int(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, int):
        return value < 0
    try:
        number = float(value)
    except (TypeError, ValueError):
        return True
    if number < 0 or number != int(number):
        return True
    return False


def _bad_positive_number(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return True
    return number <= 0


def validate_session(entry: Mapping[str, Any], index: int) -> list[str]:
    """Return problem labels for one session entry."""
    prefix = f"sessions[{index}]"
    problems = missing_fields(entry, REQUIRED_SESSION_FIELDS)
    if problems:
        return [f"{prefix}.{name}" for name in problems]

    if _bad_positive_number(entry.get("duration_minutes")):
        return [f"{prefix}.duration_minutes"]

    if _bad_non_negative_int(entry.get("unique_aircraft")):
        return [f"{prefix}.unique_aircraft"]

    if "message_count" in entry and entry.get("message_count") is not None:
        if _bad_non_negative_int(entry.get("message_count")):
            return [f"{prefix}.message_count"]

    return []


def validate_session_log(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for an ADS-B session-log document."""
    problems = missing_fields(doc, REQUIRED_LOG_FIELDS)
    if problems:
        return problems

    sessions = doc.get("sessions")
    if not isinstance(sessions, Sequence) or isinstance(sessions, (str, bytes)):
        return ["sessions"]
    if len(sessions) == 0:
        return ["sessions"]

    for index, entry in enumerate(sessions):
        if not isinstance(entry, Mapping):
            return [f"sessions[{index}]"]
        entry_problems = validate_session(entry, index)
        if entry_problems:
            return entry_problems

    return []
