"""PPM frequency-error helpers for Chapter 4.

ppm = ((f_measured - f_expected) / f_expected) * 1_000_000

suggested_correction_ppm negates the error so applying it recenters
the display onto the expected frequency in the common "subtract error"
convention. If a host program uses the opposite sign, flip once and
document the convention in station notes.
"""

from __future__ import annotations


def frequency_error_ppm(expected_hz: float, measured_hz: float) -> float:
    """Return signed frequency error in parts per million."""
    if expected_hz == 0:
        raise ValueError("expected_hz must be non-zero")
    return ((measured_hz - expected_hz) / expected_hz) * 1_000_000.0


def suggested_correction_ppm(expected_hz: float, measured_hz: float) -> float:
    """Return PPM correction that cancels frequency_error_ppm."""
    return -frequency_error_ppm(expected_hz, measured_hz)


def mhz_to_hz(frequency_mhz: float) -> float:
    """Convert megahertz to hertz."""
    return frequency_mhz * 1_000_000.0
