#!/usr/bin/env python3
"""Measure average dit length from a mark/space event JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from keyer.dot_timing import measure_dot_length


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON with an events array")
    parser.add_argument("--wpm-hint", type=int, default=None)
    args = parser.parse_args(argv)

    payload = json.loads(args.path.read_text(encoding="utf-8"))
    events = payload["events"] if isinstance(payload, dict) else payload
    wpm_hint = args.wpm_hint
    if wpm_hint is None and isinstance(payload, dict):
        wpm_hint = payload.get("wpm_hint")

    result = measure_dot_length(events, wpm_hint=wpm_hint)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
