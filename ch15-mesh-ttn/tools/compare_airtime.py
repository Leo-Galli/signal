#!/usr/bin/env python3
"""Compare mesh-text airtime vs LoRaWAN uplink payload airtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mesh.compare import compare_mesh_vs_uplink


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh-text", required=True, help="Teaching mesh text")
    parser.add_argument(
        "--uplink-bytes",
        type=int,
        required=True,
        help="LoRaWAN FRMPayload size in bytes",
    )
    parser.add_argument("--sf", type=int, default=7)
    parser.add_argument("--bw", type=float, default=125000.0, help="Bandwidth Hz")
    parser.add_argument("--cr", type=int, default=1, help="Coding rate 1..4 (4/(4+cr))")
    args = parser.parse_args(argv)

    result = compare_mesh_vs_uplink(
        args.mesh_text,
        args.uplink_bytes,
        sf=args.sf,
        bw_hz=args.bw,
        cr=args.cr,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
