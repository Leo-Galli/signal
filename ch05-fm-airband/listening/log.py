"""Listening-log validation for Chapter 5.

Checks required fields for receive-only FM / airband practice notes.
Does not talk to hardware and does not invent receptions.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

ALLOWED_MODES = frozenset({"WBFM", "AM", "NBFM"})

REQUIRED_LOG_FIELDS = (
    "access_date",
    "jurisdiction_note",
    "source_url_or_doc",
    "entries",
)

REQUIRED_ENTRY_FIELDS = (
    "time",
    "frequency_mhz",
    "mode",
    "gist",
    "antenna_position",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
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


def validate_entry(entry: Mapping[str, Any], index: int) -> list[str]:
    """Return problem labels for one log entry."""
    prefix = f"entries[{index}]"
    problems = missing_fields(entry, REQUIRED_ENTRY_FIELDS)
    if problems:
        return [f"{prefix}.{name}" for name in problems]

    if _non_positive_number(entry.get("frequency_mhz")):
        return [f"{prefix}.frequency_mhz"]

    mode = str(entry.get("mode", "")).strip().upper()
    if mode not in ALLOWED_MODES:
        return [f"{prefix}.mode"]

    return []


def validate_listen_log(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a listening-log document."""
    problems = missing_fields(doc, REQUIRED_LOG_FIELDS)
    if problems:
        return problems

    entries = doc.get("entries")
    if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
        return ["entries"]
    if len(entries) == 0:
        return ["entries"]

    partial = bool(doc.get("partial_session"))
    if not partial and len(entries) < 5:
        return ["entries_count"]

    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            return [f"entries[{index}]"]
        entry_problems = validate_entry(entry, index)
        if entry_problems:
            return entry_problems

    return []
