#!/usr/bin/env python3
"""Compare two relative antenna-position quality scores."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from listening.snr import summarize_comparison


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two unitless relative quality scores (B minus A)."
    )
    parser.add_argument(
        "--position-a",
        type=float,
        required=True,
        help="Relative score at antenna position A",
    )
    parser.add_argument(
        "--position-b",
        type=float,
        required=True,
        help="Relative score at antenna position B",
    )
    parser.add_argument(
        "--label-a",
        default="A",
        help="Label for position A (default A)",
    )
    parser.add_argument(
        "--label-b",
        default="B",
        help="Label for position B (default B)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(
        summarize_comparison(
            args.position_a,
            args.position_b,
            label_a=args.label_a,
            label_b=args.label_b,
        )
    )
    print(
        "Scores are reader-assigned relative ratings; "
        "this tool does not invent dB from the air."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
