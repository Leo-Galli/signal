#!/usr/bin/env python3
"""Score a Chapter 18 practice quiz or Italy syllabus checklist JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from licence.quiz import score_quiz


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quiz", type=Path, help="Path to quiz JSON")
    parser.add_argument(
        "--responses",
        type=Path,
        default=None,
        help="Optional JSON map of item id -> chosen answer (US MCQ)",
    )
    args = parser.parse_args(argv)

    doc = json.loads(args.quiz.read_text(encoding="utf-8"))
    responses = None
    if args.responses is not None:
        responses = json.loads(args.responses.read_text(encoding="utf-8"))

    result = score_quiz(doc, responses)
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
