#!/usr/bin/env python3
"""Plot relative signal strength vs frequency from a simple CSV.

CSV format (header required):
    frequency_mhz,relative_db

The dB column is relative (for example peak meter readings from an SDR
UI), not calibrated absolute power. This script does not talk to hardware.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_scan(path: Path) -> tuple[list[float], list[float]]:
    """Load frequency_mhz,relative_db pairs from CSV."""
    freqs: list[float] = []
    levels: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        required = {"frequency_mhz", "relative_db"}
        missing = required - {name.strip() for name in reader.fieldnames}
        if missing:
            raise ValueError(f"CSV missing columns: {sorted(missing)}")
        for row in reader:
            if not row.get("frequency_mhz") or not row.get("relative_db"):
                continue
            freqs.append(float(row["frequency_mhz"]))
            levels.append(float(row["relative_db"]))
    if not freqs:
        raise ValueError("CSV has no data rows")
    return freqs, levels


def summarize(freqs: list[float], levels: list[float]) -> dict[str, float]:
    """Return peak frequency and level plus span."""
    peak_index = max(range(len(levels)), key=lambda i: levels[i])
    return {
        "peak_frequency_mhz": freqs[peak_index],
        "peak_relative_db": levels[peak_index],
        "min_frequency_mhz": min(freqs),
        "max_frequency_mhz": max(freqs),
        "n_points": float(len(freqs)),
    }


def plot_scan(
    freqs: list[float],
    levels: list[float],
    out_path: Path,
    title: str,
) -> None:
    """Write a PNG using matplotlib (Agg backend)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(freqs, levels, color="#1a1a1a", linewidth=1.5)
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Relative level (dB)")
    ax.set_title(title)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plot relative FM/broadcast strength from CSV."
    )
    parser.add_argument("csv_path", type=Path, help="Input CSV path")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional PNG output path (requires matplotlib)",
    )
    parser.add_argument(
        "--title",
        default="Relative signal strength",
        help="Plot title",
    )
    args = parser.parse_args(argv)

    freqs, levels = load_scan(args.csv_path)
    stats = summarize(freqs, levels)
    print(
        "points={n_points:.0f} "
        "span={min_frequency_mhz:.3f}-{max_frequency_mhz:.3f} MHz "
        "peak={peak_frequency_mhz:.3f} MHz "
        "at {peak_relative_db:.1f} dB (relative)".format(**stats)
    )

    if args.out is not None:
        plot_scan(freqs, levels, args.out, args.title)
        print(f"wrote {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
