#!/usr/bin/env python3
"""Simulate the firmware software duty-cycle gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lora.duty_cycle import DutyCycleGate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--percent", type=float, default=10.0)
    parser.add_argument("--window-ms", type=int, default=3_600_000)
    parser.add_argument("--airtime-ms", type=int, required=True)
    parser.add_argument("--packets", type=int, default=1)
    parser.add_argument("--interval-ms", type=int, default=5000)
    args = parser.parse_args()

    gate = DutyCycleGate(args.percent, args.window_ms)
    now = 0
    sent = 0
    blocked = 0
    for i in range(args.packets):
        if gate.allow(now, args.airtime_ms):
            gate.record(now, args.airtime_ms)
            sent += 1
        else:
            blocked += 1
        now += args.interval_ms

    out = gate.snapshot(now)
    out["sent"] = sent
    out["blocked"] = blocked
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
