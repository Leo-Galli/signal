#!/usr/bin/env python3
"""Validate a Chapter 18 first-QSO cheat card JSON document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from licence.cheat_card import validate_cheat_card


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to cheat-card JSON")
    args = parser.parse_args(argv)

    doc = json.loads(args.path.read_text(encoding="utf-8"))
    problems = validate_cheat_card(doc)
    if problems:
        print(json.dumps({"ok": False, "problems": problems}))
        return 1
    print(json.dumps({"ok": True, "script_lines": len(doc["script_lines"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
