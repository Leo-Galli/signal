#!/usr/bin/env python3
"""Encode a practice APT-like WAV and decode it to a grayscale PNG."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wxsat.apt_practice import DEFAULT_LINES, encode_decode_roundtrip


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Write a practice APT-like WAV and decode it to a grayscale PNG. "
            "Not a live NOAA APT capture."
        )
    )
    parser.add_argument(
        "--wav",
        type=Path,
        default=ROOT / "data" / "practice_apt.wav",
        help="Output WAV path",
    )
    parser.add_argument(
        "--png",
        type=Path,
        default=ROOT / "data" / "practice_apt.png",
        help="Output PNG path",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=DEFAULT_LINES,
        help="Number of practice image lines",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        wav_path, png_path = encode_decode_roundtrip(
            args.wav,
            args.png,
            lines=args.lines,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wav={wav_path}")
    print(f"png={png_path}")
    print("note=practice pattern only -- not a satellite image")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
