"""Local clubs / resources list validation -- official directories only."""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_CLUBS_FIELDS = (
    "path_chosen",
    "resources",
    "not_legal_advice_ack",
    "access_date",
)

ALLOWED_PATHS = frozenset({"italy_mimit", "us_fcc", "other"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"

MIN_RESOURCES = 2

# Host fragments that are never "official directory" sources for this worksheet.
BLOCKED_HOST_FRAGMENTS = (
    "discord.com",
    "reddit.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "instagram.com",
)


def _iso_date_ok(value: Any) -> bool:
    text = str(value).strip() if value is not None else ""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    year, month, day = text.split("-")
    return year.isdigit() and month.isdigit() and day.isdigit()


def _url_blocked(url: str) -> bool:
    lower = url.lower()
    return any(fragment in lower for fragment in BLOCKED_HOST_FRAGMENTS)


def validate_clubs(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels; empty list means OK."""
    for name in REQUIRED_CLUBS_FIELDS:
        if name not in doc or doc.get(name) is None:
            return [name]

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    if str(doc.get("not_legal_advice_ack", "")).strip() != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    if not _iso_date_ok(doc.get("access_date")):
        return ["access_date"]

    resources = doc.get("resources")
    if not isinstance(resources, list) or len(resources) < MIN_RESOURCES:
        return ["resources"]

    for i, item in enumerate(resources):
        if not isinstance(item, dict):
            return [f"resources[{i}]"]
        if not str(item.get("name", "")).strip():
            return [f"resources[{i}].name"]
        url = str(item.get("url", "")).strip()
        if not url.startswith("https://"):
            return [f"resources[{i}].url"]
        if _url_blocked(url):
            return [f"resources[{i}].url"]
        if not str(item.get("why_official", "")).strip():
            return [f"resources[{i}].why_official"]

    return []
