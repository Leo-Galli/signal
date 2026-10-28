#!/usr/bin/env python3
"""Filter rtl_433 JSONL or sensor-log JSON by device id."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rtl433.filter_id import filter_by_device_id, unique_ids
from rtl433.log import load_jsonl_records


def _load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{"):
        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            return load_jsonl_records(text)
        if isinstance(doc, dict) and "records" in doc:
            records = doc["records"]
            if not isinstance(records, list):
                raise ValueError("records must be a JSON array")
            return [dict(item) for item in records if isinstance(item, dict)]
        if isinstance(doc, dict):
            return [doc]
    return load_jsonl_records(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Filter rtl_433 records by device id."
    )
    parser.add_argument("path", type=Path, help="JSONL or sensor-log JSON path")
    parser.add_argument(
        "--id",
        required=True,
        dest="device_id",
        help="Device id to keep",
    )
    parser.add_argument(
        "--list-ids",
        action="store_true",
        help="Print unique ids and exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = _load_records(args.path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.list_ids:
        for device_id in unique_ids(records):
            print(device_id)
        return 0

    try:
        matched = filter_by_device_id(records, args.device_id)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for entry in matched:
        print(json.dumps(entry, separators=(",", ":")))
    print(f"# matched={len(matched)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
