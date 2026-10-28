#!/usr/bin/env python3
"""Validate a Chapter 2 rail-verify JSON log.

Usage:
    python tools/validate_rail_log.py data/sample_rail_verify_log.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as a script from ch02-safety/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from safety.checklist import validate_rail_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a 5 V rail verify log")
    parser.add_argument("path", type=Path, help="Path to rail-verify JSON log")
    args = parser.parse_args(argv)

    raw = args.path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    if not isinstance(doc, dict):
        print("error: root JSON value must be an object", file=sys.stderr)
        return 1

    missing = validate_rail_log(doc)
    if missing:
        print("missing or blank fields: " + ", ".join(missing), file=sys.stderr)
        return 1

    print("rail verify log ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
