#!/usr/bin/env python3
"""Validate a decode-log JSON captured from the MCU serial monitor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from keyer.decode_log import DecodeLogError, validate_decode_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to decode log JSON")
    args = parser.parse_args(argv)

    payload = json.loads(args.path.read_text(encoding="utf-8"))
    try:
        summary = validate_decode_log(payload)
    except DecodeLogError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2))
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
