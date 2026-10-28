#!/usr/bin/env python3
"""Summarize and optionally plot temperature_C from rtl_433 records.

CSV/JSON/JSONL input. Does not talk to hardware.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rtl433.filter_id import filter_by_device_id
from rtl433.log import load_jsonl_records
from rtl433.temperature import format_summary, temperature_series


def _load_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        records: list[dict[str, Any]] = []
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                records.append(dict(row))
        return records

    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{"):
        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            return load_jsonl_records(text)
        if isinstance(doc, dict) and "records" in doc:
            records = doc["records"]
            if not isinstance(records, list):
                raise ValueError("records must be a JSON array")
            return [dict(item) for item in records if isinstance(item, dict)]
        if isinstance(doc, dict):
            return [doc]
    return load_jsonl_records(text)


def plot_series(
    series: list[tuple[str, float]],
    out_path: Path,
    title: str,
) -> None:
    """Write a PNG using matplotlib (Agg backend)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = list(range(len(series)))
    ys = [temp for _, temp in series]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, ys, color="#333333", linewidth=1.5)
    ax.set_xlabel("sample index")
    ax.set_ylabel("temperature_C")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize temperature_C from rtl_433 records."
    )
    parser.add_argument("path", type=Path, help="JSONL, sensor-log JSON, or CSV")
    parser.add_argument(
        "--id",
        dest="device_id",
        default="",
        help="Optional device id filter",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional PNG output path",
    )
    parser.add_argument(
        "--title",
        default="rtl_433 temperature",
        help="Plot title when --out is set",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = _load_records(args.path)
        if args.device_id:
            records = filter_by_device_id(records, args.device_id)
        series = temperature_series(records)
        if not series:
            print("error: no temperature_C samples found", file=sys.stderr)
            return 1
        print(format_summary(series))
        if args.out is not None:
            plot_series(series, args.out, args.title)
            print(f"wrote {args.out}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
