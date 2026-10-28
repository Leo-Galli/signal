#!/usr/bin/env python3
"""Measure decode accuracy on a fixed corpus of known phrases."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from morse.audio import synthesize_wav, write_wav
from morse.corpus import DEFAULT_CORPUS, score_accuracy, validate_corpus
from morse.decode import decode_wav_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="Optional corpus JSON (default: built-in phrases)",
    )
    parser.add_argument("--wpm", type=float, default=20.0)
    parser.add_argument(
        "--min-accuracy",
        type=float,
        default=1.0,
        help="Exit 1 if overall accuracy is below this (default 1.0)",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write per-phrase scores",
    )
    args = parser.parse_args(argv)

    if args.corpus is None:
        phrases = DEFAULT_CORPUS
    else:
        doc = json.loads(args.corpus.read_text(encoding="utf-8"))
        problems = validate_corpus(doc)
        if problems:
            print(f"invalid corpus fields: {problems}", file=sys.stderr)
            return 1
        phrases = doc["phrases"]

    rows = []
    total_matches = 0
    total_compared = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for phrase in phrases:
            phrase_id = phrase["id"]
            text = phrase["text"]
            wav_path = tmp_path / f"{phrase_id}.wav"
            pcm, rate = synthesize_wav(text, wpm=args.wpm)
            write_wav(wav_path, pcm, sample_rate=rate)
            decoded = decode_wav_file(wav_path, wpm_hint=args.wpm)
            score = score_accuracy(text, decoded)
            total_matches += int(score["matches"])
            total_compared += int(score["compared_len"])
            row = {
                "id": phrase_id,
                "expected": text,
                "decoded": decoded,
                "accuracy": score["accuracy"],
            }
            rows.append(row)
            print(
                f"{phrase_id}: accuracy={score['accuracy']:.3f} "
                f"decoded={decoded!r}"
            )

    overall = total_matches / total_compared if total_compared else 0.0
    print(f"overall_accuracy={overall:.3f} ({total_matches}/{total_compared})")

    if args.json_out is not None:
        payload = {
            "wpm": args.wpm,
            "overall_accuracy": overall,
            "phrases": rows,
        }
        args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if overall + 1e-12 < args.min_accuracy:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
