#!/usr/bin/env python3
"""Validate a datasheet citation JSON for link-budget worksheets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = (
    "module_family",
    "datasheet_title",
    "datasheet_revision_or_date",
    "table_or_page",
    "sf",
    "bw_hz",
    "sensitivity_dbm",
    "access_note",
)


def validate(doc: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in doc:
            errors.append(f"missing field: {key}")
            continue
        if doc[key] is None or (isinstance(doc[key], str) and not str(doc[key]).strip()):
            errors.append(f"empty field: {key}")
    if "sensitivity_dbm" in doc and not isinstance(doc["sensitivity_dbm"], (int, float)):
        errors.append("sensitivity_dbm must be a number")
    if doc.get("fixture_only") is True:
        # Allowed for CI samples; worksheets must set fixture_only false for real work.
        pass
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON path")
    args = parser.parse_args(argv)

    try:
        doc = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"validate failed: {exc}", file=sys.stderr)
        return 1

    if not isinstance(doc, dict):
        print("validate failed: root must be an object", file=sys.stderr)
        return 1

    errors = validate(doc)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    fixture = doc.get("fixture_only", False)
    print(
        f"ok: {doc['module_family']} sens={doc['sensitivity_dbm']} dBm "
        f"from {doc['datasheet_title']} ({doc['table_or_page']})"
        + (" [FIXTURE ONLY]" if fixture else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
