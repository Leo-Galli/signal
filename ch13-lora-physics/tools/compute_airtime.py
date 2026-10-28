#!/usr/bin/env python3
"""Compute LoRa packet airtime (Semtech timing model)."""

from __future__ import annotations

import argparse
import json
import sys

from lora.airtime import airtime_ms


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sf", type=int, required=True, help="Spreading factor 6..12")
    parser.add_argument("--bw", type=float, required=True, help="Bandwidth in Hz (e.g. 125000)")
    parser.add_argument("--payload", type=int, required=True, help="Payload bytes")
    parser.add_argument("--cr", type=int, default=1, help="Coding rate 1..4 (default 1 = 4/5)")
    parser.add_argument("--preamble", type=float, default=8.0, help="Preamble symbols")
    parser.add_argument("--no-crc", action="store_true", help="Disable CRC in timing model")
    parser.add_argument("--implicit-header", action="store_true")
    parser.add_argument(
        "--ldr",
        choices=["auto", "on", "off"],
        default="auto",
        help="Low data rate optimize (default auto: on when SF>=11)",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args(argv)

    ldr: bool | None
    if args.ldr == "auto":
        ldr = None
    elif args.ldr == "on":
        ldr = True
    else:
        ldr = False

    try:
        result = airtime_ms(
            args.sf,
            args.bw,
            args.payload,
            cr=args.cr,
            preamble_symbols=args.preamble,
            crc_on=not args.no_crc,
            implicit_header=args.implicit_header,
            low_data_rate=ldr,
        )
    except ValueError as exc:
        print(f"airtime failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"SF{result['sf']} BW={result['bw_hz']:.0f} Hz CR=4/{4 + result['cr']} "
            f"PL={result['payload_bytes']} B -> {result['airtime_ms']:.3f} ms "
            f"(LDR={result['low_data_rate']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
