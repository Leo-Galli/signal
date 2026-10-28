"""Practice-string helpers for callsign-shaped or initials drills.

Unlicensed readers use initials or a nonsense practice string. Licensed readers
may use their own callsign. This module only validates format -- it does not
claim a string is a real issued callsign.
"""

from __future__ import annotations

import re
from typing import Any, Mapping

# ITU-like amateur callsign shape for practice only (not a registry lookup).
CALLSIGN_SHAPED = re.compile(
    r"^[A-Z0-9]{1,3}[0-9][A-Z0-9]{1,4}(/[A-Z0-9]{1,4})?$"
)
INITIALS = re.compile(r"^[A-Z]{2,4}$")
# Practice tokens: letters/digits with optional separators for copy drills.
PRACTICE_TOKEN = re.compile(r"^[A-Z0-9]{2,12}$")


def normalize_practice_text(text: str) -> str:
    """Uppercase and strip; reject empty."""
    cleaned = text.strip().upper()
    if not cleaned:
        raise ValueError("practice text is empty")
    return cleaned


def classify_practice_string(text: str) -> str:
    """Return 'callsign_shaped', 'initials', or 'practice_token'."""
    cleaned = normalize_practice_text(text)
    if CALLSIGN_SHAPED.match(cleaned):
        return "callsign_shaped"
    if INITIALS.match(cleaned):
        return "initials"
    if PRACTICE_TOKEN.match(cleaned):
        return "practice_token"
    raise ValueError(
        "use initials (2-4 letters), a short practice token, "
        "or a callsign-shaped string"
    )


def validate_practice_string_doc(doc: Mapping[str, Any]) -> list[str]:
    """Validate a practice-string worksheet JSON document."""
    required = (
        "practice_text",
        "kind_expected",
        "licensed_or_unlicensed",
        "notes",
    )
    problems: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            problems.append(name)
    if problems:
        return problems

    status = str(doc["licensed_or_unlicensed"]).strip().lower()
    if status not in {"licensed", "unlicensed", "studying"}:
        return ["licensed_or_unlicensed"]

    kind_expected = str(doc["kind_expected"]).strip().lower()
    if kind_expected not in {"callsign_shaped", "initials", "practice_token"}:
        return ["kind_expected"]

    try:
        kind = classify_practice_string(str(doc["practice_text"]))
    except ValueError:
        return ["practice_text"]

    if kind != kind_expected:
        return ["kind_expected"]

    if status == "unlicensed" and kind == "callsign_shaped":
        # Unlicensed readers may still drill a callsign-shaped nonsense string,
        # but must say so in notes (minimum honesty check: notes mention practice).
        notes = str(doc["notes"]).lower()
        if "practice" not in notes and "not a callsign" not in notes:
            return ["notes"]

    if len(str(doc["notes"]).strip()) < 3:
        return ["notes"]

    return []
