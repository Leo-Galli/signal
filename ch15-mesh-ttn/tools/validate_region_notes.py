#!/usr/bin/env python3
"""Validate a region-settings JSON note."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mesh.regions import validate_region_note


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON region note path")
    args = parser.parse_args(argv)

    note = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_region_note(note)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "region": note["region"], "path": note["path"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
