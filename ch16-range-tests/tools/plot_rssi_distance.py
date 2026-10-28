#!/usr/bin/env python3
"""Plot RSSI vs distance from a results JSON file (no invented points)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from range.plot_rssi import plot_rssi_distance, rssi_distance_series


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Results JSON")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("rssi_vs_distance.png"),
        help="Output PNG path",
    )
    parser.add_argument(
        "--title",
        default="RSSI vs distance (reader measurements)",
        help="Plot title",
    )
    args = parser.parse_args(argv)

    doc = json.loads(args.path.read_text(encoding="utf-8"))
    series, skipped = rssi_distance_series(doc)
    print(
        json.dumps(
            {
                "points_plotted": len(series),
                "points_skipped_blank": skipped,
                "series": [{"distance_m": d, "rssi_dbm": r} for d, r in series],
            },
            indent=2,
        )
    )
    if len(series) < 2:
        print(
            "ERROR: need at least two points with both distance_m and rssi_dbm",
            file=sys.stderr,
        )
        return 1
    plot_rssi_distance(series, str(args.out), title=args.title)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
