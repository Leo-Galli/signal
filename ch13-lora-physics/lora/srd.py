"""EU / CEPT SRD planning helpers using BOOK_SPEC-locked ERC/REC 70-03 figures.

Not legal advice. National footnotes can differ. Re-check the live annex.
"""

from __future__ import annotations

from typing import Any

# Locked planning highlights from BOOK_SPEC Section 15 / ERC/REC 70-03 Annex 1.
# Keys are stable labels for worksheets -- not a complete annex reprint.
SRD_ENTRIES: dict[str, dict[str, Any]] = {
    "g1_433": {
        "label": "ERC/REC 70-03 Annex 1 g1",
        "band_mhz": "433.05-434.79",
        "erp_mw": 10.0,
        "duty_cycle_percent": 10.0,
        "duty_cycle_required": True,
        "notes": "10 mW e.r.p., duty cycle <= 10%. Re-check live annex + national footnotes.",
        "source_url": "https://docdb.cept.org/download/4863",
    },
    "g2_433": {
        "label": "ERC/REC 70-03 Annex 1 g2",
        "band_mhz": "433.05-434.79",
        "erp_mw": 1.0,
        "duty_cycle_percent": None,
        "duty_cycle_required": False,
        "notes": "1 mW e.r.p., no duty-cycle requirement under that entry. Re-check live annex.",
        "source_url": "https://docdb.cept.org/download/4863",
    },
    "h1_868_family": {
        "label": "ERC/REC 70-03 Annex 1 h1.x family (planning highlight)",
        "band_mhz": "863-870",
        "erp_mw": 25.0,
        "duty_cycle_percent": 0.1,
        "duty_cycle_required": True,
        "notes": (
            "Common non-specific SRD highlight: typically 25 mW e.r.p. with "
            "duty-cycle or LBT+AFA depending on sub-entry. Always read the "
            "current Annex 1 row and national footnotes before field use."
        ),
        "source_url": "https://docdb.cept.org/download/4863",
    },
}


def srd_entry(key: str) -> dict[str, Any]:
    """Return a copy of a locked SRD planning entry."""
    if key not in SRD_ENTRIES:
        known = ", ".join(sorted(SRD_ENTRIES))
        raise KeyError(f"unknown SRD entry {key!r}; known: {known}")
    return dict(SRD_ENTRIES[key])


def duty_cycle_budget(
    airtime_ms: float,
    duty_cycle_percent: float,
    window_s: float = 3600.0,
) -> dict[str, Any]:
    """Max packets in a window given airtime and a percent duty-cycle cap.

    Example: 10% of 3600 s = 360 s TX budget per hour.
    """
    if airtime_ms <= 0:
        raise ValueError("airtime_ms must be positive")
    if duty_cycle_percent <= 0 or duty_cycle_percent > 100:
        raise ValueError("duty_cycle_percent must be in (0, 100]")
    if window_s <= 0:
        raise ValueError("window_s must be positive")

    budget_s = window_s * (duty_cycle_percent / 100.0)
    airtime_s = airtime_ms / 1000.0
    max_packets = int(budget_s // airtime_s)
    return {
        "airtime_ms": airtime_ms,
        "duty_cycle_percent": duty_cycle_percent,
        "window_s": window_s,
        "tx_budget_s": budget_s,
        "max_packets": max_packets,
        "note": "Planning arithmetic only. Not legal advice.",
    }
