"""Image-artifact rating helpers for Chapter 7 worksheets.

Validates a structured artifact checklist the reader fills after
looking at a decoded grayscale practice image or a live decode.
Does not invent scores for real satellite passes.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_FIELDS = (
    "access_date",
    "image_source",
    "sync_quality",
    "noise_level",
    "slant_or_skew",
    "overall_usable",
    "notes",
)

ALLOWED_SYNC = frozenset({"clean", "intermittent", "lost", "n/a"})
ALLOWED_NOISE = frozenset({"low", "medium", "high", "n/a"})
ALLOWED_SLANT = frozenset({"none", "mild", "severe", "n/a"})
ALLOWED_USABLE = frozenset({"yes", "partial", "no"})
ALLOWED_SOURCES = frozenset(
    {
        "companion-practice-wav",
        "live-meteor-lrpt",
        "live-other",
        "archived-public-sample",
    }
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def validate_artifact_rating(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for an artifact-rating document."""
    problems = missing_fields(doc, REQUIRED_FIELDS)
    if problems:
        return problems

    checks = (
        ("image_source", ALLOWED_SOURCES),
        ("sync_quality", ALLOWED_SYNC),
        ("noise_level", ALLOWED_NOISE),
        ("slant_or_skew", ALLOWED_SLANT),
        ("overall_usable", ALLOWED_USABLE),
    )
    for field, allowed in checks:
        value = str(doc.get(field, "")).strip()
        if value not in allowed:
            return [field]
    return []
