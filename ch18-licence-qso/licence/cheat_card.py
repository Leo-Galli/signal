"""First-QSO cheat card validation for Chapter 18."""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_CHEAT_CARD_FIELDS = (
    "callsign_or_practice",
    "path_chosen",
    "listen_first_ack",
    "phonetic_name",
    "script_lines",
    "band_or_frequency_note",
    "not_legal_advice_ack",
)

ALLOWED_PATHS = frozenset({"italy_mimit", "us_fcc", "other", "practice_only"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"

LISTEN_FIRST_ACK = "I will listen before transmitting"

MIN_SCRIPT_LINES = 4


def validate_cheat_card(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels; empty list means OK."""
    problems: list[str] = []
    for name in REQUIRED_CHEAT_CARD_FIELDS:
        value = doc.get(name, "")
        if value is None or (isinstance(value, str) and not value.strip()):
            if name != "script_lines":
                problems.append(name)
    if problems:
        return problems

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    if str(doc.get("listen_first_ack", "")).strip() != LISTEN_FIRST_ACK:
        return ["listen_first_ack"]

    if str(doc.get("not_legal_advice_ack", "")).strip() != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    lines = doc.get("script_lines")
    if not isinstance(lines, list) or len(lines) < MIN_SCRIPT_LINES:
        return ["script_lines"]
    for i, line in enumerate(lines):
        if not isinstance(line, str) or not line.strip():
            return [f"script_lines[{i}]"]

    practice = str(doc.get("callsign_or_practice", "")).strip().upper()
    if path == "practice_only" and practice in {"", "TBD", "MYCALL"}:
        return ["callsign_or_practice"]

    return []
