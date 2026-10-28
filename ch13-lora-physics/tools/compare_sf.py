#!/usr/bin/env python3
"""Compare LoRa airtime for two spreading factors."""

from __future__ import annotations

import argparse
import json
import sys

from lora.airtime import compare_sf_airtime


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sf-a", type=int, default=7, help="First SF (default 7)")
    parser.add_argument("--sf-b", type=int, default=12, help="Second SF (default 12)")
    parser.add_argument("--bw", type=float, default=125000.0, help="Bandwidth Hz")
    parser.add_argument("--payload", type=int, default=10, help="Payload bytes")
    parser.add_argument("--cr", type=int, default=1, help="Coding rate 1..4")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = compare_sf_airtime(
            args.sf_a,
            args.sf_b,
            args.bw,
            args.payload,
            cr=args.cr,
        )
    except ValueError as exc:
        print(f"compare failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        a = result["a"]
        b = result["b"]
        print(
            f"SF{a['sf']}: {a['airtime_ms']:.3f} ms | "
            f"SF{b['sf']}: {b['airtime_ms']:.3f} ms | "
            f"ratio SF{b['sf']}/SF{a['sf']} = {result['ratio_b_over_a']:.2f}x"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
