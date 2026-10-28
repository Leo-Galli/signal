#!/usr/bin/env python3
"""Encode or decode a Chapter 14 beacon payload (hex)."""

from __future__ import annotations

import argparse
import binascii
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lora.packet import decode, encode  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("encode", help="encode seq/name/lat/lon to hex")
    enc.add_argument("--seq", type=int, required=True)
    enc.add_argument("--name", required=True)
    enc.add_argument("--lat", type=float, default=0.0)
    enc.add_argument("--lon", type=float, default=0.0)

    dec = sub.add_parser("decode", help="decode hex payload")
    dec.add_argument("hex", help="hex string of packet bytes")

    args = parser.parse_args()
    if args.cmd == "encode":
        raw = encode(args.seq, args.name, args.lat, args.lon)
        print(binascii.hexlify(raw).decode("ascii"))
        print(json.dumps({"bytes": len(raw), "hex": binascii.hexlify(raw).decode("ascii")}))
        return 0

    raw = binascii.unhexlify(args.hex)
    print(json.dumps(decode(raw), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
