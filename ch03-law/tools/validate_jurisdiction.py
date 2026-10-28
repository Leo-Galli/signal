#!/usr/bin/env python3
"""Validate a Chapter 3 jurisdiction worksheet JSON document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from law.jurisdiction import validate_jurisdiction


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to jurisdiction JSON")
    args = parser.parse_args(argv)

    doc = json.loads(args.path.read_text(encoding="utf-8"))
    problems = validate_jurisdiction(doc)
    if problems:
        print("INVALID:", ", ".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
