"""Sample-rate chain helpers for a minimal FM receive flowgraph.

A typical WBFM path is:

  RF sample rate (RTL-SDR) -> optional decimation / LPF ->
  quadrature rate into WBFM Receive -> audio rate out to Audio Sink.

These helpers check arithmetic consistency. They do not open hardware.
"""

from __future__ import annotations


def audio_rate_hz(quadrature_rate_hz: float, audio_decimation: int) -> float:
    """Return audio sample rate from WBFM quadrature rate and decimation."""
    if quadrature_rate_hz <= 0:
        raise ValueError("quadrature_rate_hz must be positive")
    if audio_decimation < 1:
        raise ValueError("audio_decimation must be >= 1")
    return quadrature_rate_hz / float(audio_decimation)


def decimation_ok(input_rate_hz: float, output_rate_hz: float, decimation: int) -> bool:
    """Return True if input_rate / decimation matches output_rate within 1e-6 relative."""
    if input_rate_hz <= 0 or output_rate_hz <= 0:
        raise ValueError("rates must be positive")
    if decimation < 1:
        raise ValueError("decimation must be >= 1")
    expected = input_rate_hz / float(decimation)
    if expected == 0:
        return False
    return abs(expected - output_rate_hz) / expected <= 1e-6


def nyquist_ok(sample_rate_hz: float, highest_freq_hz: float) -> bool:
    """Return True if sample_rate is strictly above 2 * highest_freq (Nyquist)."""
    if sample_rate_hz <= 0 or highest_freq_hz < 0:
        raise ValueError("invalid rate or frequency")
    return sample_rate_hz > (2.0 * highest_freq_hz)


def throttle_period_s(sample_rate_hz: float) -> float:
    """Return seconds per sample for a Throttle block at sample_rate_hz."""
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    return 1.0 / sample_rate_hz


def describe_chain(
    rf_rate_hz: float,
    channel_decimation: int,
    audio_decimation: int,
) -> dict[str, float]:
    """Return named rates for RF -> channel -> audio given two integer decimations."""
    if rf_rate_hz <= 0:
        raise ValueError("rf_rate_hz must be positive")
    if channel_decimation < 1 or audio_decimation < 1:
        raise ValueError("decimation must be >= 1")
    quad = rf_rate_hz / float(channel_decimation)
    audio = audio_rate_hz(quad, audio_decimation)
    return {
        "rf_rate_hz": float(rf_rate_hz),
        "quadrature_rate_hz": float(quad),
        "audio_rate_hz": float(audio),
    }
