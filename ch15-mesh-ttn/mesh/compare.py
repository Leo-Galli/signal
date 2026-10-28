"""Compare airtime: mesh-style UTF-8 text vs compact LoRaWAN uplink bytes."""

from __future__ import annotations

from typing import Any

from mesh.airtime import airtime_ms


def mesh_payload_bytes(text: str) -> int:
    """UTF-8 byte length of a mesh-style teaching text (no protocol framing)."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return len(text.encode("utf-8"))


def compare_mesh_vs_uplink(
    mesh_text: str,
    uplink_bytes: int,
    *,
    sf: int = 7,
    bw_hz: float = 125_000.0,
    cr: int = 1,
) -> dict[str, Any]:
    """Airtime for mesh text bytes vs a LoRaWAN-sized uplink payload.

    Framing beyond the raw payload is ignored on purpose: this is a first-order
    teaching compare under identical modem settings, not a full stack simulator.
    """
    if uplink_bytes < 0:
        raise ValueError("uplink_bytes must be >= 0")

    mesh_n = mesh_payload_bytes(mesh_text)
    mesh = airtime_ms(sf, bw_hz, mesh_n, cr=cr)
    uplink = airtime_ms(sf, bw_hz, uplink_bytes, cr=cr)

    mesh_air = mesh["airtime_ms"]
    up_air = uplink["airtime_ms"]
    if up_air <= 0:
        ratio = float("inf")
    else:
        ratio = mesh_air / up_air

    longer = "mesh_text" if mesh_air > up_air else "uplink"
    if abs(mesh_air - up_air) < 1e-9:
        longer = "equal"

    return {
        "sf": sf,
        "bw_hz": float(bw_hz),
        "cr": cr,
        "mesh_text": mesh_text,
        "mesh_payload_bytes": mesh_n,
        "mesh": mesh,
        "uplink_bytes": uplink_bytes,
        "uplink": uplink,
        "ratio_mesh_over_uplink": ratio,
        "longer": longer,
        "note": (
            "Payload-only Semtech airtime compare. Not a full Meshtastic or "
            "LoRaWAN frame simulator. Not legal advice."
        ),
    }
