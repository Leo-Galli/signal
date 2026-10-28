#!/usr/bin/env python3
"""Print Koch characters through a lesson number."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from morse.koch import KOCH_ORDER, characters_through_lesson, lesson_for_character


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Koch lesson helper (LCWO-style order)."
    )
    parser.add_argument(
        "--lesson",
        type=int,
        help="1-based lesson index; print characters through that lesson",
    )
    parser.add_argument(
        "--char",
        dest="character",
        help="Look up which lesson introduces this character",
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="Print the full Koch order string",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list_all:
        print("".join(KOCH_ORDER))
        return 0
    if args.character is not None:
        try:
            lesson = lesson_for_character(args.character)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(f"char={args.character!r} lesson={lesson}")
        return 0
    if args.lesson is None:
        print("error: provide --lesson, --char, or --list-all", file=sys.stderr)
        return 1
    try:
        chars = characters_through_lesson(args.lesson)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"lesson={args.lesson} characters={''.join(chars)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
