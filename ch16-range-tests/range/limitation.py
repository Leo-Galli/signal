"""Validate the required honest limitation paragraph for a range walk."""

from __future__ import annotations

from typing import Any

BANNED_FRAGMENTS = (
    "i got 20 km",
    "i got 20km",
    "guaranteed km",
    "guaranteed kilometers",
)


def validate_limitation(doc: dict[str, Any]) -> list[str]:
    """Return error strings; empty means OK.

    Requires a short paragraph. Rejects a few brag phrases that skip method.
    Does not try to NLP-police every claim -- honesty is still on the reader.
    """
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be an object"]

    if "limitation_note" not in doc:
        return ["missing field: limitation_note"]

    note = doc.get("limitation_note")
    if not isinstance(note, str):
        return ["limitation_note must be a string"]

    text = note.strip()
    if len(text) < 40:
        errors.append("limitation_note must be at least 40 characters")

    lower = text.lower()
    for fragment in BANNED_FRAGMENTS:
        if fragment in lower:
            errors.append(
                "limitation_note must not use empty kilometer brags; "
                "point at your own table instead"
            )
            break

    if doc.get("invented_ranges") is True:
        errors.append("invented_ranges must not be true")

    return errors
