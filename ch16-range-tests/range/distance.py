"""Great-circle distance helpers for optional GPS waypoints."""

from __future__ import annotations

import math


def haversine_m(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    *,
    radius_m: float = 6_371_000.0,
) -> float:
    """Return approximate surface distance in meters between two WGS84 points.

    Teaching helper only. Phone GPS error often dominates short parking-lot walks.
    """
    for name, value in (
        ("lat1_deg", lat1_deg),
        ("lon1_deg", lon1_deg),
        ("lat2_deg", lat2_deg),
        ("lon2_deg", lon2_deg),
    ):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{name} must be a number")
    if radius_m <= 0:
        raise ValueError("radius_m must be > 0")

    phi1 = math.radians(float(lat1_deg))
    phi2 = math.radians(float(lat2_deg))
    d_phi = math.radians(float(lat2_deg) - float(lat1_deg))
    d_lambda = math.radians(float(lon2_deg) - float(lon1_deg))

    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0 - a)))
    return radius_m * c
