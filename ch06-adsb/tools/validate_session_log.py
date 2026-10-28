#!/usr/bin/env python3
"""Validate a Chapter 6 ADS-B session-log JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adsb.session import validate_session_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a receive-only ADS-B session-log JSON file."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to session-log JSON",
    )
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

    problems = validate_session_log(doc)
    if problems:
        print("invalid: " + ", ".join(problems), file=sys.stderr)
        return 1

    session_count = len(doc.get("sessions", []))
    print(f"ok: {args.path} sessions={session_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
