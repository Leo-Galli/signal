#!/usr/bin/env python3
"""Validate checked-in GNU Radio Companion .grc files for Chapter 9."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gnuradio.grc_parse import summarize_grc, validate_file_source_grc, validate_live_grc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Chapter 9 .grc flowgraph file."
    )
    parser.add_argument("path", type=Path, help="Path to a .grc file")
    parser.add_argument(
        "--kind",
        choices=("live", "file"),
        default="live",
        help="Which required-block set to apply (default: live)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.kind == "live":
        problems = validate_live_grc(args.path)
    else:
        problems = validate_file_source_grc(args.path)

    if problems:
        print("invalid: " + ", ".join(problems), file=sys.stderr)
        return 1

    summary = summarize_grc(args.path)
    print(
        f"ok: {args.path} kind={args.kind} "
        f"block_ids={summary['block_id_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
