#!/usr/bin/env python3
"""Validate a Chapter 4 station notes JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdr.station_notes import validate_station_notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate SDR station notes JSON.")
    parser.add_argument("path", type=Path, help="Path to station notes JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw = args.path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    problems = validate_station_notes(doc)
    if problems:
        print("INVALID: " + ", ".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
