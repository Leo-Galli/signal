"""First-order free-space link budget.

Sensitivity must be supplied by the caller from a cited datasheet row.
This module never invents module sensitivity or field range claims.
"""

from __future__ import annotations

import math
from typing import Any


def mw_to_dbm(power_mw: float) -> float:
    """Convert milliwatts to dBm. 1 mW = 0 dBm; 10 mW = 10 dBm."""
    if power_mw <= 0:
        raise ValueError("power_mw must be positive")
    return 10.0 * math.log10(power_mw)


def dbm_to_mw(power_dbm: float) -> float:
    """Convert dBm to milliwatts."""
    return 10.0 ** (power_dbm / 10.0)


def free_space_path_loss_db(distance_m: float, freq_mhz: float) -> float:
    """Free-space path loss (dB) for distance in meters and frequency in MHz.

    FSPL = 20*log10(d_m) + 20*log10(f_MHz) + 20*log10(4*pi/c) with c in m/us
    form equivalent to 20*log10(d_km) + 20*log10(f_MHz) + 32.44 when d is in km.
    """
    if distance_m <= 0:
        raise ValueError("distance_m must be positive")
    if freq_mhz <= 0:
        raise ValueError("freq_mhz must be positive")
    # 20*log10(4*pi / c) with c = 299.792458 m/us -> constant for MHz and meters
    # Equivalent: 20*log10(d_m) + 20*log10(f_Hz) - 147.55 with f_Hz = freq_mhz*1e6
    return (
        20.0 * math.log10(distance_m)
        + 20.0 * math.log10(freq_mhz)
        + 20.0 * math.log10(4.0 * math.pi / 299.792458)
    )


def link_budget(
    *,
    tx_power_dbm: float,
    tx_antenna_gain_dbi: float,
    rx_antenna_gain_dbi: float,
    distance_m: float,
    freq_mhz: float,
    sensitivity_dbm: float,
    other_losses_db: float = 0.0,
    sensitivity_source: str,
) -> dict[str, Any]:
    """First-order link budget.

    sensitivity_dbm: paste from the module datasheet row matching your SF/BW.
    sensitivity_source: short citation string (datasheet title + revision/page).
    other_losses_db: cables, connectors, mismatch -- measured or datasheet, not invented.
    """
    source = (sensitivity_source or "").strip()
    if not source:
        raise ValueError(
            "sensitivity_source is required -- cite the datasheet row you copied"
        )

    fspl = free_space_path_loss_db(distance_m, freq_mhz)
    prx = (
        tx_power_dbm
        + tx_antenna_gain_dbi
        + rx_antenna_gain_dbi
        - fspl
        - other_losses_db
    )
    margin = prx - sensitivity_dbm

    return {
        "tx_power_dbm": tx_power_dbm,
        "tx_antenna_gain_dbi": tx_antenna_gain_dbi,
        "rx_antenna_gain_dbi": rx_antenna_gain_dbi,
        "distance_m": distance_m,
        "freq_mhz": freq_mhz,
        "other_losses_db": other_losses_db,
        "fspl_db": fspl,
        "prx_dbm": prx,
        "sensitivity_dbm": sensitivity_dbm,
        "sensitivity_source": source,
        "margin_db": margin,
        "note": (
            "Free-space first-order model only. Not a field range claim. "
            "Replace sensitivity with your datasheet number."
        ),
    }
