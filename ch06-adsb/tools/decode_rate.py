#!/usr/bin/env python3
"""Compute ADS-B messages per minute from recorded counts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adsb.rate import format_rate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute messages per minute from a timed ADS-B session."
    )
    parser.add_argument(
        "--messages",
        type=int,
        required=True,
        help="Message or frame count you recorded",
    )
    parser.add_argument(
        "--minutes",
        type=float,
        required=True,
        help="Session duration in minutes",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        print(format_rate(args.messages, args.minutes))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
