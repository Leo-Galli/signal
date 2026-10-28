"""Jurisdiction worksheet validation for Chapter 3.

Checks required citation fields and the not-legal-advice acknowledgement.
Does not invent regulatory limits, fees, callsigns or exam content.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_JURISDICTION_FIELDS = (
    "country_or_admin",
    "path_chosen",
    "official_urls",
    "receive_notes",
    "srd_or_unlicensed_notes",
    "amateur_licence_notes",
    "project_bucket_example",
    "not_legal_advice_ack",
    "access_date",
)

ALLOWED_PATHS = frozenset({"italy_mimit", "us_fcc", "other"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...] | None = None) -> list[str]:
    """Return names of required fields that are missing or blank."""
    names = required if required is not None else REQUIRED_JURISDICTION_FIELDS
    missing: list[str] = []
    for name in names:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def _urls_invalid(value: Any) -> bool:
    if isinstance(value, str):
        parts = [p.strip() for p in value.replace(",", " ").split() if p.strip()]
    elif isinstance(value, (list, tuple)):
        parts = [str(p).strip() for p in value if str(p).strip()]
    else:
        return True
    if not parts:
        return True
    return any(not p.startswith("https://") for p in parts)


def validate_jurisdiction(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a jurisdiction worksheet document."""
    problems = missing_fields(doc, REQUIRED_JURISDICTION_FIELDS)
    if problems:
        return problems

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    if _urls_invalid(doc.get("official_urls")):
        return ["official_urls"]

    ack = str(doc.get("not_legal_advice_ack", "")).strip()
    if ack != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    access = str(doc.get("access_date", "")).strip()
    if len(access) != 10 or access[4] != "-" or access[7] != "-":
        return ["access_date"]
    year, month, day = access.split("-")
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return ["access_date"]

    return []
