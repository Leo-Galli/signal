"""Station identification checklist validation for Chapter 18."""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_STATION_ID_FIELDS = (
    "path_chosen",
    "official_url",
    "access_date",
    "id_rules_summary",
    "checklist",
    "not_legal_advice_ack",
)

ALLOWED_PATHS = frozenset({"italy_mimit", "us_fcc", "other"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"

MIN_CHECKLIST_ITEMS = 3


def _iso_date_ok(value: Any) -> bool:
    text = str(value).strip() if value is not None else ""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    year, month, day = text.split("-")
    return year.isdigit() and month.isdigit() and day.isdigit()


def validate_station_id(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels; empty list means OK."""
    for name in REQUIRED_STATION_ID_FIELDS:
        if name not in doc or doc.get(name) is None:
            return [name]

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    url = str(doc.get("official_url", "")).strip()
    if not url.startswith("https://"):
        return ["official_url"]

    if not _iso_date_ok(doc.get("access_date")):
        return ["access_date"]

    if not str(doc.get("id_rules_summary", "")).strip():
        return ["id_rules_summary"]

    if str(doc.get("not_legal_advice_ack", "")).strip() != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    checklist = doc.get("checklist")
    if not isinstance(checklist, list) or len(checklist) < MIN_CHECKLIST_ITEMS:
        return ["checklist"]

    for i, item in enumerate(checklist):
        if not isinstance(item, dict):
            return [f"checklist[{i}]"]
        if not str(item.get("step", "")).strip():
            return [f"checklist[{i}].step"]
        checked = item.get("checked")
        if checked is not None and not isinstance(checked, bool):
            return [f"checklist[{i}].checked"]

    return []
