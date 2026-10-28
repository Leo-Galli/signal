"""Frequency, wavelength and power conversions for Chapter 1.

Uses the defined speed of light in vacuum (SI): 299_792_458 m/s.
dBm is power relative to 1 milliwatt: dBm = 10 * log10(P_mW).
"""

from __future__ import annotations

import math

# Exact SI definition of the speed of light in vacuum (m/s).
SPEED_OF_LIGHT_M_S = 299_792_458.0


def mhz_to_wavelength_m(frequency_mhz: float) -> float:
    """Return free-space wavelength in meters for a frequency in MHz."""
    if frequency_mhz <= 0:
        raise ValueError("frequency_mhz must be positive")
    frequency_hz = frequency_mhz * 1_000_000.0
    return SPEED_OF_LIGHT_M_S / frequency_hz


def wavelength_m_to_mhz(wavelength_m: float) -> float:
    """Return frequency in MHz for a free-space wavelength in meters."""
    if wavelength_m <= 0:
        raise ValueError("wavelength_m must be positive")
    frequency_hz = SPEED_OF_LIGHT_M_S / wavelength_m
    return frequency_hz / 1_000_000.0


def mw_to_dbm(power_mw: float) -> float:
    """Convert milliwatts to dBm. 0 dBm == 1 mW."""
    if power_mw <= 0:
        raise ValueError("power_mw must be positive")
    return 10.0 * math.log10(power_mw)


def dbm_to_mw(power_dbm: float) -> float:
    """Convert dBm to milliwatts."""
    return 10.0 ** (power_dbm / 10.0)
