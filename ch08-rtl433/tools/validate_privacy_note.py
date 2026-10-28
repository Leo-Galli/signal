#!/usr/bin/env python3
"""Validate a Chapter 8 privacy-note JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rtl433.privacy import validate_privacy_note


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate an ISM sensor privacy-note JSON file."
    )
    parser.add_argument("path", type=Path, help="Path to privacy-note JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        raw = args.path.read_text(encoding="utf-8")
        doc = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not isinstance(doc, dict):
        print("error: root must be a JSON object", file=sys.stderr)
        return 1

    problems = validate_privacy_note(doc)
    if problems:
        print("invalid: " + ", ".join(problems), file=sys.stderr)
        return 1

    print(f"ok: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
