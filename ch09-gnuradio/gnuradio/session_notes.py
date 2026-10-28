"""Session-notes validation for Chapter 9 GNU Radio labs.

Checks required fields for receive-only flowgraph practice notes.
Does not talk to hardware and does not invent audio measurements.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

REQUIRED_FIELDS = (
    "access_date",
    "gnuradio_version",
    "grc_version_or_build",
    "flowgraph_path",
    "sample_rate_hz",
    "center_freq_hz",
    "filter_cutoff_hz",
    "audio_rate_hz",
    "jurisdiction_note",
    "block_versions_note",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def validate_session_notes(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a GNU Radio session-notes document."""
    problems = missing_fields(doc, REQUIRED_FIELDS)
    if problems:
        return problems

    for numeric in ("sample_rate_hz", "center_freq_hz", "filter_cutoff_hz", "audio_rate_hz"):
        try:
            value = float(doc[numeric])
        except (TypeError, ValueError):
            return [numeric]
        if value <= 0:
            return [numeric]

    exercises = doc.get("exercises")
    if exercises is not None:
        if not isinstance(exercises, Mapping):
            return ["exercises"]
        for key in ("filter_bandwidth", "file_sink", "block_versions"):
            if key in exercises and not str(exercises.get(key, "")).strip():
                return [f"exercises.{key}"]

    return []


def validate_block_versions(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a block-versions JSON document."""
    required = ("gnuradio_version", "blocks")
    problems = missing_fields(doc, required)
    if problems:
        return problems
    blocks = doc.get("blocks")
    if not isinstance(blocks, Sequence) or isinstance(blocks, (str, bytes)):
        return ["blocks"]
    if len(blocks) == 0:
        return ["blocks"]
    for index, entry in enumerate(blocks):
        if not isinstance(entry, Mapping):
            return [f"blocks[{index}]"]
        for field in ("id", "label"):
            if not str(entry.get(field, "")).strip():
                return [f"blocks[{index}].{field}"]
    return []
