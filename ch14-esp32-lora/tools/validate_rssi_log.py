#!/usr/bin/env python3
"""Validate an indoor RSSI-vs-distance JSON log."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lora.rssi_log import validate_rssi_log  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    doc = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_rssi_log(doc)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {len(doc['points'])} points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
