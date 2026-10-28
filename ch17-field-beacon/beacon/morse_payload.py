"""Morse fallback string builder mirroring firmware/src/morse_payload.cpp."""

from __future__ import annotations

MORSE_PAYLOAD_MAX = 96
NAME_MAX = 15


def format_coord(value: float, hemi_pos: str, hemi_neg: str) -> str:
    hemi = hemi_pos if value >= 0.0 else hemi_neg
    return f"{abs(value):.5f}{hemi}"


def build_morse_payload(name: str, lat: float, lon: float) -> str:
    """Return 'SOS <NAME> <lat> <lon>' for sidetone / legal CW practice."""
    cleaned = "".join(ch for ch in name.upper() if ch.isascii())
    cleaned = cleaned[:NAME_MAX]
    if not cleaned:
        cleaned = "NONAME"
    lat_s = format_coord(float(lat), "N", "S")
    lon_s = format_coord(float(lon), "E", "W")
    text = f"SOS {cleaned} {lat_s} {lon_s}"
    if len(text) > MORSE_PAYLOAD_MAX:
        raise ValueError("morse payload too long")
    return text
