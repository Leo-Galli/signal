#!/usr/bin/env python3
"""Validate a Chapter 18 four-week study calendar JSON document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from licence.calendar import total_planned_minutes, validate_calendar


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to calendar JSON")
    args = parser.parse_args(argv)

    doc = json.loads(args.path.read_text(encoding="utf-8"))
    problems = validate_calendar(doc)
    if problems:
        print(json.dumps({"ok": False, "problems": problems}))
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "weeks": 4,
                "planned_minutes": total_planned_minutes(doc),
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
