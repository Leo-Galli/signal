"""Known region labels for worksheets (not a full channel-plan reprint)."""

from __future__ import annotations

from typing import Any

# Stable teaching labels commonly seen in Meshtastic / LoRaWAN docs.
# Details live in official regional-parameter documents -- do not invent plans.
REGION_LABELS: dict[str, dict[str, Any]] = {
    "EU868": {
        "label": "EU868",
        "family": "863-870 MHz class plans (EU)",
        "typical_context": "Europe LoRaWAN / Meshtastic region preset",
        "docs_hint": "Confirm LoRa Alliance EU868 regional parameters and national footnotes.",
    },
    "US915": {
        "label": "US915",
        "family": "902-928 MHz class plans (US)",
        "typical_context": "United States LoRaWAN / Meshtastic region preset",
        "docs_hint": "Confirm LoRa Alliance US915 regional parameters and FCC rules.",
    },
    "AU915": {
        "label": "AU915",
        "family": "915-928 MHz class plans (AU)",
        "typical_context": "Australia region preset",
        "docs_hint": "Confirm LoRa Alliance AU915 regional parameters and national rules.",
    },
    "AS923": {
        "label": "AS923",
        "family": "AS923 family",
        "typical_context": "Asia 923 MHz class plans",
        "docs_hint": "Confirm LoRa Alliance AS923 regional parameters for your country variant.",
    },
    "IN865": {
        "label": "IN865",
        "family": "865-867 MHz class plans (IN)",
        "typical_context": "India region preset",
        "docs_hint": "Confirm LoRa Alliance IN865 regional parameters and national rules.",
    },
}


REQUIRED_REGION_NOTE_FIELDS = (
    "region",
    "country_or_area",
    "path",
    "official_url",
    "checked_date",
    "not_legal_advice",
)


def normalize_region(region: str) -> str:
    """Uppercase and strip a region label."""
    if not isinstance(region, str) or not region.strip():
        raise ValueError("region must be a non-empty string")
    return region.strip().upper()


def known_region(region: str) -> dict[str, Any]:
    """Return a copy of a known region entry, or raise KeyError."""
    key = normalize_region(region)
    if key not in REGION_LABELS:
        known = ", ".join(sorted(REGION_LABELS))
        raise KeyError(f"unknown region {region!r}; known teaching labels: {known}")
    return dict(REGION_LABELS[key])


def validate_region_note(note: dict[str, Any]) -> list[str]:
    """Return a list of validation errors (empty means OK)."""
    errors: list[str] = []
    if not isinstance(note, dict):
        return ["note must be a JSON object"]

    for field in REQUIRED_REGION_NOTE_FIELDS:
        if field not in note:
            errors.append(f"missing field: {field}")

    if errors:
        return errors

    try:
        region = normalize_region(str(note["region"]))
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    if region not in REGION_LABELS:
        errors.append(
            f"region {note['region']!r} not in teaching labels "
            f"{', '.join(sorted(REGION_LABELS))}"
        )

    path = str(note.get("path", "")).strip().lower()
    if path not in {"meshtastic", "ttn", "p2p", "none"}:
        errors.append("path must be one of: meshtastic, ttn, p2p, none")

    url = str(note.get("official_url", ""))
    if not (url.startswith("https://") or url.startswith("http://")):
        errors.append("official_url must start with http:// or https://")

    if note.get("not_legal_advice") is not True:
        errors.append("not_legal_advice must be true")

    country = str(note.get("country_or_area", "")).strip()
    if len(country) < 2:
        errors.append("country_or_area must be at least 2 characters")

    date = str(note.get("checked_date", "")).strip()
    if len(date) < 8:
        errors.append("checked_date must look like YYYY-MM-DD")

    return errors
