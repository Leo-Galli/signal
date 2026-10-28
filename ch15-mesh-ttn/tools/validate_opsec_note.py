#!/usr/bin/env python3
"""Validate an operational-security worksheet JSON note."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = (
    "secrets_storage",
    "retention",
    "redaction",
    "not_committed",
    "checked_date",
)


def validate_opsec_note(note: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(note, dict):
        return ["note must be a JSON object"]
    for field in REQUIRED:
        if field not in note:
            errors.append(f"missing field: {field}")
    if errors:
        return errors
    if note.get("not_committed") is not True:
        errors.append("not_committed must be true")
    for field in ("secrets_storage", "retention", "redaction"):
        if len(str(note.get(field, "")).strip()) < 3:
            errors.append(f"{field} must be a short non-empty string")
    if len(str(note.get("checked_date", "")).strip()) < 8:
        errors.append("checked_date must look like YYYY-MM-DD")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    note = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_opsec_note(note)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
