#!/usr/bin/env python3
"""First-order free-space link budget (sensitivity from YOUR datasheet)."""

from __future__ import annotations

import argparse
import json
import sys

from lora.link_budget import link_budget, mw_to_dbm


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    power = parser.add_mutually_exclusive_group(required=True)
    power.add_argument("--tx-dbm", type=float, help="Conducted / planned TX power dBm")
    power.add_argument("--tx-mw", type=float, help="TX power in mW (converted to dBm)")
    parser.add_argument("--tx-gain", type=float, default=0.0, help="TX antenna gain dBi")
    parser.add_argument("--rx-gain", type=float, default=0.0, help="RX antenna gain dBi")
    parser.add_argument("--distance-m", type=float, required=True, help="Link distance meters")
    parser.add_argument("--freq-mhz", type=float, required=True, help="Carrier MHz")
    parser.add_argument(
        "--sensitivity-dbm",
        type=float,
        required=True,
        help="Receiver sensitivity from datasheet (dBm), matching SF/BW",
    )
    parser.add_argument(
        "--sensitivity-source",
        required=True,
        help="Datasheet citation (title, revision, table/page)",
    )
    parser.add_argument("--other-losses-db", type=float, default=0.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        tx_dbm = args.tx_dbm if args.tx_dbm is not None else mw_to_dbm(args.tx_mw)
        result = link_budget(
            tx_power_dbm=tx_dbm,
            tx_antenna_gain_dbi=args.tx_gain,
            rx_antenna_gain_dbi=args.rx_gain,
            distance_m=args.distance_m,
            freq_mhz=args.freq_mhz,
            sensitivity_dbm=args.sensitivity_dbm,
            other_losses_db=args.other_losses_db,
            sensitivity_source=args.sensitivity_source,
        )
    except ValueError as exc:
        print(f"link budget failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"FSPL={result['fspl_db']:.2f} dB  Prx={result['prx_dbm']:.2f} dBm  "
            f"Sens={result['sensitivity_dbm']:.2f} dBm  "
            f"Margin={result['margin_db']:.2f} dB"
        )
        print(f"source: {result['sensitivity_source']}")
        print(result["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
