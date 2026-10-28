"""Sensor-log validation for Chapter 8.

Checks required fields for receive-only rtl_433 JSON / JSONL practice notes.
Does not talk to hardware and does not invent sensors.
"""

from __future__ import annotations

import json
from typing import Any, Mapping, Sequence

REQUIRED_META_FIELDS = (
    "access_date",
    "jurisdiction_note",
    "rtl433_version_or_build",
    "band_note",
    "privacy_ack",
)

REQUIRED_RECORD_FIELDS = (
    "time",
    "model",
    "id",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or not str(value).strip():
            missing.append(name)
    return missing


def validate_record(entry: Mapping[str, Any], index: int) -> list[str]:
    """Return problem labels for one decoded sensor record."""
    prefix = f"records[{index}]"
    problems = missing_fields(entry, REQUIRED_RECORD_FIELDS)
    if problems:
        return [f"{prefix}.{name}" for name in problems]
    return []


def validate_sensor_log(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a sensor-log document (meta + records)."""
    problems = missing_fields(doc, REQUIRED_META_FIELDS)
    if problems:
        return problems

    privacy = str(doc.get("privacy_ack", "")).strip().lower()
    if privacy not in {"yes", "true", "acknowledged"}:
        return ["privacy_ack"]

    records = doc.get("records")
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        return ["records"]
    if len(records) == 0:
        return ["records"]

    for index, entry in enumerate(records):
        if not isinstance(entry, Mapping):
            return [f"records[{index}]"]
        entry_problems = validate_record(entry, index)
        if entry_problems:
            return entry_problems

    return []


def load_jsonl_records(text: str) -> list[dict[str, Any]]:
    """Parse rtl_433-style JSON lines into a list of objects."""
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"line {line_no}: expected a JSON object")
        records.append(obj)
    return records
