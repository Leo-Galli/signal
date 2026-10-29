#!/usr/bin/env python3
"""Print ITU phonetic spelling for a practice callsign or initials."""

from __future__ import annotations

import argparse
import json
import sys

from licence.phonetics import spell_callsign


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="Callsign or practice string")
    args = parser.parse_args(argv)

    words = spell_callsign(args.text)
    print(json.dumps({"input": args.text, "phonetics": words}))
    return 0 if words else 1


if __name__ == "__main__":
    sys.exit(main())
