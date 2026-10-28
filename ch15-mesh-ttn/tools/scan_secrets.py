#!/usr/bin/env python3
"""Scan a path for secret-shaped patterns before git add."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mesh.secrets_scan import scan_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        action="append",
        required=True,
        help="File or directory to scan (repeatable)",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Exit 0 even when findings exist (report only)",
    )
    args = parser.parse_args(argv)

    findings = scan_paths(args.path)
    print(json.dumps({"findings": findings, "count": len(findings)}, indent=2))
    if findings and not args.allow_empty:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
