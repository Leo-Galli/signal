#!/usr/bin/env python3
"""Encode at nominal WPM and at +/- timing_scale, then decode each WAV.

Exercise 2 helper: show whether the decoder still recovers the phrase when
element timing is stretched or compressed by about 10 percent.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from morse.audio import synthesize_wav, write_wav
from morse.corpus import score_accuracy
from morse.decode import decode_wav_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="Phrase to encode")
    parser.add_argument("--wpm", type=float, default=20.0)
    parser.add_argument(
        "--scales",
        default="0.9,1.0,1.1",
        help="Comma-separated timing scales (default 0.9,1.0,1.1)",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write results JSON",
    )
    args = parser.parse_args(argv)

    try:
        scales = [float(part.strip()) for part in args.scales.split(",") if part.strip()]
    except ValueError:
        print("bad --scales", file=sys.stderr)
        return 1
    if not scales:
        print("no scales", file=sys.stderr)
        return 1

    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for scale in scales:
            wav_path = tmp_path / f"scale_{scale:.3f}.wav"
            pcm, rate = synthesize_wav(args.text, wpm=args.wpm, timing_scale=scale)
            write_wav(wav_path, pcm, sample_rate=rate)
            decoded = decode_wav_file(wav_path, wpm_hint=args.wpm / scale)
            # Hint uses effective unit: slower scale stretches time so unit
            # estimate from wpm alone would be wrong; divide by scale.
            score = score_accuracy(args.text, decoded)
            row = {
                "timing_scale": scale,
                "decoded": decoded,
                "accuracy": score["accuracy"],
                "matches": score["matches"],
                "compared_len": score["compared_len"],
            }
            results.append(row)
            print(
                f"scale={scale:.3f} accuracy={score['accuracy']:.3f} "
                f"decoded={decoded!r}"
            )

    if args.json_out is not None:
        args.json_out.write_text(
            json.dumps({"text": args.text, "wpm": args.wpm, "results": results}, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
