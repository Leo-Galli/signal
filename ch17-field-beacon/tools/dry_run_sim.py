#!/usr/bin/env python3
"""Simulate dry-run vs live TX decisions without keying RF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from beacon.dry_run import dry_run_init, simulate_tx


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile-force", action="store_true", default=True)
    parser.add_argument("--no-compile-force", action="store_true")
    parser.add_argument("--would-key", action="store_true")
    args = parser.parse_args(argv)
    compile_force = not args.no_compile_force
    state = dry_run_init(compile_force=compile_force)
    result = simulate_tx(state, would_key_rf=args.would_key)
    result["blocked_tx_count"] = state.blocked_tx_count
    result["simulated_tx_count"] = state.simulated_tx_count
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
