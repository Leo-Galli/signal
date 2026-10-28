#!/usr/bin/env python3
"""Print RF / quadrature / audio rates for a Chapter 9 flowgraph chain."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gnuradio.sample_rates import describe_chain, nyquist_ok


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute sample-rate chain values for a WBFM receive path."
    )
    parser.add_argument(
        "--rf-rate",
        type=float,
        required=True,
        help="RF sample rate in Hz (RTL-SDR samp_rate)",
    )
    parser.add_argument(
        "--channel-decim",
        type=int,
        required=True,
        help="Integer decimation from RF rate to quadrature / channel rate",
    )
    parser.add_argument(
        "--audio-decim",
        type=int,
        required=True,
        help="Integer audio decimation inside WBFM Receive",
    )
    parser.add_argument(
        "--fm-deviation-hz",
        type=float,
        default=75e3,
        help="Optional: check Nyquist headroom vs this baseband half-width (default 75e3)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        chain = describe_chain(args.rf_rate, args.channel_decim, args.audio_decim)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    quad = chain["quadrature_rate_hz"]
    ok = nyquist_ok(quad, args.fm_deviation_hz)
    print(
        f"rf_rate_hz={chain['rf_rate_hz']:.1f} "
        f"quadrature_rate_hz={quad:.1f} "
        f"audio_rate_hz={chain['audio_rate_hz']:.1f} "
        f"nyquist_vs_deviation_ok={ok}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
