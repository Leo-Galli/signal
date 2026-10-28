#!/usr/bin/env python3
"""Print Farnsworth timing numbers or validate a timing JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from morse.timing import timing_report, validate_timing_params


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Farnsworth / PARIS timing helper for Morse practice."
    )
    parser.add_argument(
        "--character-wpm",
        type=float,
        help="Character speed in words per minute (PARIS)",
    )
    parser.add_argument(
        "--effective-wpm",
        type=float,
        help="Overall / Farnsworth effective speed in WPM",
    )
    parser.add_argument(
        "--json",
        type=Path,
        dest="json_path",
        help="Optional timing JSON to validate (character_wpm, effective_wpm)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.json_path is not None:
        try:
            doc = json.loads(args.json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if not isinstance(doc, dict):
            print("error: root must be a JSON object", file=sys.stderr)
            return 1
        problems = validate_timing_params(doc)
        if problems:
            print("invalid: " + ", ".join(problems), file=sys.stderr)
            return 1
        char_wpm = float(doc["character_wpm"])
        eff_wpm = float(doc["effective_wpm"])
    else:
        if args.character_wpm is None or args.effective_wpm is None:
            print(
                "error: provide --character-wpm and --effective-wpm, or --json",
                file=sys.stderr,
            )
            return 1
        char_wpm = args.character_wpm
        eff_wpm = args.effective_wpm
        problems = validate_timing_params(
            {"character_wpm": char_wpm, "effective_wpm": eff_wpm}
        )
        if problems:
            print("invalid: " + ", ".join(problems), file=sys.stderr)
            return 1

    try:
        report = timing_report(char_wpm, eff_wpm)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"character_wpm={report['character_wpm']}")
    print(f"effective_wpm={report['effective_wpm']}")
    print(f"dot_seconds={report['dot_seconds']:.6f}")
    print(f"dash_seconds={report['dash_seconds']:.6f}")
    print(
        "inter_character_gap_seconds="
        f"{report['inter_character_gap_seconds']:.6f}"
    )
    print(f"inter_word_gap_seconds={report['inter_word_gap_seconds']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
