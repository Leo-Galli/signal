#!/usr/bin/env python3
"""Decode a mono Morse WAV file to text."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from morse.decode import decode_wav_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path, help="Input mono 16-bit WAV")
    parser.add_argument(
        "--wpm-hint",
        type=float,
        default=None,
        help="Optional WPM hint for unit length (else estimated)",
    )
    parser.add_argument(
        "--no-prosigns",
        action="store_true",
        help="Do not map patterns to <PROSIGN> tokens",
    )
    args = parser.parse_args(argv)

    try:
        text = decode_wav_file(
            args.wav,
            include_prosigns=not args.no_prosigns,
            wpm_hint=args.wpm_hint,
        )
    except (ValueError, OSError) as exc:
        print(f"decode failed: {exc}", file=sys.stderr)
        return 1

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
