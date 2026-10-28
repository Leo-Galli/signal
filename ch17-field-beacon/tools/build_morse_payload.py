#!/usr/bin/env python3
"""Build the Morse fallback string for the field beacon."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from beacon.morse_payload import build_morse_payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    text = build_morse_payload(args.name, args.lat, args.lon)
    if args.json:
        print(json.dumps({"morse_text": text, "chars": len(text)}))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
