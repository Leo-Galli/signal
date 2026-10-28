"""Semtech LoRa packet airtime (AN1200.13 style).

Formulas follow the public Semtech LoRa modem design guide timing model.
Sensitivity and range are NOT computed here -- see link_budget.py and paste
datasheet numbers yourself.
"""

from __future__ import annotations

import math
from typing import Any


def symbol_time_s(sf: int, bw_hz: float) -> float:
    """LoRa symbol duration T_sym = 2^SF / BW."""
    if sf < 6 or sf > 12:
        raise ValueError(f"sf must be 6..12, got {sf}")
    if bw_hz <= 0:
        raise ValueError("bw_hz must be positive")
    return (2**sf) / float(bw_hz)


def _payload_symbol_count(
    payload_bytes: int,
    sf: int,
    cr: int,
    *,
    crc_on: bool = True,
    implicit_header: bool = False,
    low_data_rate: bool = False,
) -> int:
    """Number of payload symbols (Semtech payloadSymbNb)."""
    if payload_bytes < 0:
        raise ValueError("payload_bytes must be >= 0")
    if cr < 1 or cr > 4:
        raise ValueError("cr must be 1..4 (coding rate 4/(4+cr))")

    pl = payload_bytes
    crc = 1 if crc_on else 0
    h = 1 if implicit_header else 0
    de = 1 if low_data_rate else 0

    numerator = 8 * pl - 4 * sf + 28 + 16 * crc - 20 * h
    denominator = 4 * (sf - 2 * de)
    if denominator <= 0:
        raise ValueError("invalid SF / low_data_rate combination")

    n = math.ceil(numerator / denominator)
    if n < 0:
        n = 0
    return 8 + n * (cr + 4)


def airtime_ms(
    sf: int,
    bw_hz: float,
    payload_bytes: int,
    *,
    cr: int = 1,
    preamble_symbols: float = 8.0,
    crc_on: bool = True,
    implicit_header: bool = False,
    low_data_rate: bool | None = None,
) -> dict[str, Any]:
    """Return airtime breakdown in milliseconds.

    If low_data_rate is None, enable LDR optimize when SF >= 11 (common
    Semtech default for narrow BW / high SF). Pass True/False to override.
    """
    if low_data_rate is None:
        low_data_rate = sf >= 11

    t_sym = symbol_time_s(sf, bw_hz)
    t_preamble = (preamble_symbols + 4.25) * t_sym
    n_payload = _payload_symbol_count(
        payload_bytes,
        sf,
        cr,
        crc_on=crc_on,
        implicit_header=implicit_header,
        low_data_rate=low_data_rate,
    )
    t_payload = n_payload * t_sym
    t_packet = t_preamble + t_payload

    return {
        "sf": sf,
        "bw_hz": float(bw_hz),
        "cr": cr,
        "payload_bytes": payload_bytes,
        "preamble_symbols": float(preamble_symbols),
        "crc_on": crc_on,
        "implicit_header": implicit_header,
        "low_data_rate": low_data_rate,
        "symbol_time_ms": t_sym * 1000.0,
        "preamble_ms": t_preamble * 1000.0,
        "payload_symbols": n_payload,
        "payload_ms": t_payload * 1000.0,
        "airtime_ms": t_packet * 1000.0,
    }


def compare_sf_airtime(
    sf_a: int,
    sf_b: int,
    bw_hz: float,
    payload_bytes: int,
    **kwargs: Any,
) -> dict[str, Any]:
    """Compare airtime for two spreading factors with identical other settings."""
    a = airtime_ms(sf_a, bw_hz, payload_bytes, **kwargs)
    # low_data_rate None should re-evaluate per SF
    b_kwargs = dict(kwargs)
    if "low_data_rate" not in b_kwargs:
        b_kwargs["low_data_rate"] = None
    b = airtime_ms(sf_b, bw_hz, payload_bytes, **b_kwargs)
    ratio = b["airtime_ms"] / a["airtime_ms"] if a["airtime_ms"] else float("inf")
    return {
        "a": a,
        "b": b,
        "ratio_b_over_a": ratio,
    }
