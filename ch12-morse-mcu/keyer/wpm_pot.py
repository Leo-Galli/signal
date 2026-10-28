"""Map ADC readings from a WPM potentiometer to clamped WPM."""

from __future__ import annotations

from .timing import clamp_wpm


def wpm_from_adc(adc_raw: int, adc_max: int = 4095) -> int:
    """Map 0..adc_max onto 5..40 WPM (matches firmware/src/timing.cpp)."""
    if adc_max <= 0:
        raise ValueError("adc_max must be positive")
    if adc_raw < 0:
        raise ValueError("adc_raw must be non-negative")
    raw = min(int(adc_raw), int(adc_max))
    mapped = 5 + (raw * 35) // int(adc_max)
    return clamp_wpm(mapped)
