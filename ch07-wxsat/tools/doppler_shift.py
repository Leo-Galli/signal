#!/usr/bin/env python3
"""Compute first-order Doppler shift for a carrier and radial speed."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wxsat.doppler import format_doppler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compute first-order Doppler shift. "
            "Positive v_radial_mps means the transmitter approaches."
        )
    )
    parser.add_argument(
        "--carrier-hz",
        type=float,
        required=True,
        help="Nominal carrier frequency in Hz (for example 137100000)",
    )
    parser.add_argument(
        "--v-radial-mps",
        type=float,
        required=True,
        help="Radial speed in meters per second (approaching is positive)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        print(format_doppler(args.carrier_hz, args.v_radial_mps))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
