#!/usr/bin/env python3
"""Runnable lab notebook: airtime + first-order link budget.

Replace FIXTURE sensitivity with a number you copy from your module datasheet.
This script prints steps; it does not claim a field range.
"""

from __future__ import annotations

from lora.airtime import airtime_ms, compare_sf_airtime
from lora.link_budget import link_budget, mw_to_dbm
from lora.srd import duty_cycle_budget, srd_entry


def main() -> None:
    print("=== Step 1: SF7 vs SF12 airtime (10-byte payload, BW 125 kHz, CR 4/5) ===")
    cmp_ = compare_sf_airtime(7, 12, 125000.0, 10, cr=1)
    print(f"SF7:  {cmp_['a']['airtime_ms']:.3f} ms")
    print(f"SF12: {cmp_['b']['airtime_ms']:.3f} ms")
    print(f"ratio SF12/SF7: {cmp_['ratio_b_over_a']:.2f}x")

    print("\n=== Step 2: Duty-cycle planning under Annex 1 g1 (10% of 1 hour) ===")
    g1 = srd_entry("g1_433")
    air = airtime_ms(12, 125000.0, 10, cr=1)
    budget = duty_cycle_budget(air["airtime_ms"], float(g1["duty_cycle_percent"]))
    print(f"entry: {g1['label']} -- {g1['notes']}")
    print(f"SF12 airtime: {air['airtime_ms']:.3f} ms")
    print(f"max packets / hour at {g1['duty_cycle_percent']}%: {budget['max_packets']}")
    print("Not legal advice. Re-check https://docdb.cept.org/download/4863 and national footnotes.")

    print("\n=== Step 3: Recompute TX power as 10 mW e.r.p. planning (10 dBm) ===")
    tx_dbm = mw_to_dbm(10.0)
    print(f"10 mW -> {tx_dbm:.2f} dBm")

    print("\n=== Step 4: First-order link budget (FIXTURE sensitivity -- replace me) ===")
    # FIXTURE ONLY. Open your SX127x / SX126x / E22 datasheet and paste the
    # sensitivity for the SF/BW row you actually plan to use.
    sensitivity_dbm = -120.0
    source = "FIXTURE -- replace with datasheet title, revision, table/page"
    lb = link_budget(
        tx_power_dbm=tx_dbm,
        tx_antenna_gain_dbi=0.0,
        rx_antenna_gain_dbi=0.0,
        distance_m=1000.0,
        freq_mhz=433.0,
        sensitivity_dbm=sensitivity_dbm,
        other_losses_db=1.0,
        sensitivity_source=source,
    )
    print(f"FSPL:   {lb['fspl_db']:.2f} dB")
    print(f"Prx:    {lb['prx_dbm']:.2f} dBm")
    print(f"Sens:   {lb['sensitivity_dbm']:.2f} dBm ({lb['sensitivity_source']})")
    print(f"Margin: {lb['margin_db']:.2f} dB")
    print(lb["note"])


if __name__ == "__main__":
    main()
