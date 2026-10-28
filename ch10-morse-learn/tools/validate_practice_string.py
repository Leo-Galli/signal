#!/usr/bin/env python3
"""Validate a Chapter 10 practice-string JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from morse.practice_string import (
    classify_practice_string,
    validate_practice_string_doc,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Morse practice-string JSON file."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to practice-string JSON",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        doc = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not isinstance(doc, dict):
        print("error: root must be a JSON object", file=sys.stderr)
        return 1

    problems = validate_practice_string_doc(doc)
    if problems:
        print("invalid: " + ", ".join(problems), file=sys.stderr)
        return 1

    kind = classify_practice_string(str(doc["practice_text"]))
    print(f"ok: {args.path} kind={kind}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
