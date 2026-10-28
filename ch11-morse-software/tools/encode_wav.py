#!/usr/bin/env python3
"""Encode text to a mono Morse WAV file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from morse.audio import synthesize_wav, write_wav


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="Text to encode (use <AR> style for prosigns)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output WAV path",
    )
    parser.add_argument("--wpm", type=float, default=20.0, help="PARIS WPM (default 20)")
    parser.add_argument("--tone-hz", type=float, default=700.0, help="Tone frequency")
    parser.add_argument("--sample-rate", type=int, default=8000, help="Sample rate Hz")
    parser.add_argument(
        "--timing-scale",
        type=float,
        default=1.0,
        help="Multiply all element durations (0.9 / 1.1 for fuzz)",
    )
    parser.add_argument(
        "--no-prosigns",
        action="store_true",
        help="Reject <PROSIGN> tokens",
    )
    args = parser.parse_args(argv)

    try:
        pcm, rate = synthesize_wav(
            args.text,
            wpm=args.wpm,
            sample_rate=args.sample_rate,
            tone_hz=args.tone_hz,
            timing_scale=args.timing_scale,
            include_prosigns=not args.no_prosigns,
        )
        write_wav(args.output, pcm, sample_rate=rate)
    except (ValueError, KeyError) as exc:
        print(f"encode failed: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {args.output} ({len(pcm)} samples @ {rate} Hz, {args.wpm} WPM)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
