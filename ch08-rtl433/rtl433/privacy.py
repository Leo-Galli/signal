"""Privacy-note validation for Chapter 8 ISM sensor logging.

Ensures the reader documented a short privacy stance before keeping logs.
Does not invent legal advice.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_PRIVACY_FIELDS = (
    "access_date",
    "retention_plan",
    "neighbor_note",
    "no_publish_ack",
    "purpose",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def validate_privacy_note(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a privacy-note document."""
    problems = missing_fields(doc, REQUIRED_PRIVACY_FIELDS)
    if problems:
        return problems

    ack = str(doc.get("no_publish_ack", "")).strip().lower()
    if ack not in {"yes", "true", "acknowledged"}:
        return ["no_publish_ack"]

    retention = str(doc.get("retention_plan", "")).strip()
    if len(retention) < 8:
        return ["retention_plan"]

    neighbor = str(doc.get("neighbor_note", "")).strip()
    if len(neighbor) < 8:
        return ["neighbor_note"]

    purpose = str(doc.get("purpose", "")).strip()
    if len(purpose) < 8:
        return ["purpose"]

    return []
