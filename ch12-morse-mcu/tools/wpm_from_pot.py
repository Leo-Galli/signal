#!/usr/bin/env python3
"""Map a potentiometer ADC reading to WPM (firmware-compatible)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from keyer.wpm_pot import wpm_from_adc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adc_raw", type=int, nargs="?", help="Raw ADC reading")
    parser.add_argument(
        "--adc-max",
        type=int,
        default=4095,
        help="ADC full scale (4095 ESP32, 1023 Uno)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional JSON file with adc_raw and optional adc_max",
    )
    args = parser.parse_args(argv)

    if args.json is not None:
        payload = json.loads(args.json.read_text(encoding="utf-8"))
        adc_raw = int(payload["adc_raw"])
        adc_max = int(payload.get("adc_max", args.adc_max))
    else:
        if args.adc_raw is None:
            parser.error("provide adc_raw or --json")
        adc_raw = args.adc_raw
        adc_max = args.adc_max

    wpm = wpm_from_adc(adc_raw, adc_max)
    print(json.dumps({"adc_raw": adc_raw, "adc_max": adc_max, "wpm": wpm}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
