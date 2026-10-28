#!/usr/bin/env python3
"""Compare indoor vs outdoor unique-aircraft counts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adsb.antenna import summarize_sites


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare unique-aircraft counts for two antenna sites."
    )
    parser.add_argument(
        "--indoor",
        type=int,
        required=True,
        help="Unique aircraft count at the indoor (or poorer sky-view) site",
    )
    parser.add_argument(
        "--outdoor",
        type=int,
        required=True,
        help="Unique aircraft count at the outdoor (or better sky-view) site",
    )
    parser.add_argument(
        "--label-indoor",
        default="indoor",
        help="Label for the indoor site",
    )
    parser.add_argument(
        "--label-outdoor",
        default="outdoor",
        help="Label for the outdoor site",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        print(
            summarize_sites(
                args.indoor,
                args.outdoor,
                args.label_indoor,
                args.label_outdoor,
            )
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
