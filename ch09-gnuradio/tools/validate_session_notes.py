#!/usr/bin/env python3
"""Validate Chapter 9 GNU Radio session-notes JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gnuradio.session_notes import validate_block_versions, validate_session_notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate GNU Radio session notes or block-versions JSON."
    )
    parser.add_argument("path", type=Path, help="Path to JSON file")
    parser.add_argument(
        "--kind",
        choices=("session", "blocks"),
        default="session",
        help="Document kind (default: session)",
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

    if args.kind == "session":
        problems = validate_session_notes(doc)
    else:
        problems = validate_block_versions(doc)

    if problems:
        print("invalid: " + ", ".join(problems), file=sys.stderr)
        return 1

    print(f"ok: {args.path} kind={args.kind}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
