#!/usr/bin/env python3
"""Compute PPM frequency error from expected vs measured MHz."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdr.ppm import frequency_error_ppm, mhz_to_hz, suggested_correction_ppm


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute PPM error and suggested correction from MHz values."
    )
    parser.add_argument(
        "--expected-mhz",
        type=float,
        required=True,
        help="Published or trusted frequency in MHz",
    )
    parser.add_argument(
        "--measured-mhz",
        type=float,
        required=True,
        help="Peak frequency read from the SDR display in MHz",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    expected_hz = mhz_to_hz(args.expected_mhz)
    measured_hz = mhz_to_hz(args.measured_mhz)
    error = frequency_error_ppm(expected_hz, measured_hz)
    correction = suggested_correction_ppm(expected_hz, measured_hz)
    print(f"expected_mhz={args.expected_mhz}")
    print(f"measured_mhz={args.measured_mhz}")
    print(f"frequency_error_ppm={error:.6f}")
    print(f"suggested_correction_ppm={correction:.6f}")
    print(
        "Apply suggested_correction_ppm in host software; "
        "flip the sign once if your UI uses the opposite convention."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
