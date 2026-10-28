"""First-order Doppler helpers for LEO weather-sat practice.

Uses the non-relativistic radial approximation:
delta_f = f0 * v_radial_mps / c
Positive v_radial means the transmitter is approaching the receiver
(frequency shifts upward). Does not invent orbital elements.
"""

from __future__ import annotations

SPEED_OF_LIGHT_MPS = 299_792_458.0


def doppler_shift_hz(carrier_hz: float, v_radial_mps: float) -> float:
    """Return frequency shift in Hz for a radial speed in m/s."""
    if carrier_hz <= 0:
        raise ValueError("carrier_hz must be positive")
    return carrier_hz * v_radial_mps / SPEED_OF_LIGHT_MPS


def observed_frequency_hz(carrier_hz: float, v_radial_mps: float) -> float:
    """Return observed frequency = carrier + Doppler shift."""
    return carrier_hz + doppler_shift_hz(carrier_hz, v_radial_mps)


def format_doppler(carrier_hz: float, v_radial_mps: float) -> str:
    """Return a one-line Doppler summary."""
    shift = doppler_shift_hz(carrier_hz, v_radial_mps)
    observed = carrier_hz + shift
    return (
        f"carrier_hz={carrier_hz:.1f} v_radial_mps={v_radial_mps:.1f} "
        f"delta_hz={shift:.2f} observed_hz={observed:.2f}"
    )
