#!/usr/bin/env python3
"""Max packets under a percent duty-cycle cap for a given airtime."""

from __future__ import annotations

import argparse
import json
import sys

from lora.airtime import airtime_ms
from lora.srd import duty_cycle_budget, srd_entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sf", type=int, default=12)
    parser.add_argument("--bw", type=float, default=125000.0)
    parser.add_argument("--payload", type=int, default=10)
    parser.add_argument("--cr", type=int, default=1)
    parser.add_argument(
        "--entry",
        choices=["g1_433", "g2_433", "h1_868_family", "custom"],
        default="g1_433",
        help="Locked SRD planning entry or custom percent",
    )
    parser.add_argument(
        "--duty-percent",
        type=float,
        help="Required when --entry custom",
    )
    parser.add_argument("--window-s", type=float, default=3600.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        air = airtime_ms(args.sf, args.bw, args.payload, cr=args.cr)
        if args.entry == "custom":
            if args.duty_percent is None:
                raise ValueError("--duty-percent required with --entry custom")
            duty = args.duty_percent
            entry_meta = {"label": "custom", "notes": "Caller-supplied percent"}
        else:
            entry_meta = srd_entry(args.entry)
            if not entry_meta["duty_cycle_required"]:
                print(
                    f"{entry_meta['label']}: no duty-cycle requirement under that "
                    "planning entry (still re-check the live annex).",
                    file=sys.stderr,
                )
                if args.json:
                    print(json.dumps({"entry": entry_meta, "airtime": air}, indent=2))
                return 0
            duty = float(entry_meta["duty_cycle_percent"])
        budget = duty_cycle_budget(air["airtime_ms"], duty, window_s=args.window_s)
    except (ValueError, KeyError) as exc:
        print(f"duty-cycle failed: {exc}", file=sys.stderr)
        return 1

    out = {"entry": entry_meta, "airtime": air, "budget": budget}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(
            f"airtime={air['airtime_ms']:.3f} ms | duty={duty}% / {args.window_s:.0f}s "
            f"| max_packets={budget['max_packets']} "
            f"| entry={entry_meta.get('label', args.entry)}"
        )
        print("Not legal advice. Re-check ERC/REC 70-03 live annex + national footnotes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
