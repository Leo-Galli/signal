"""SRD planning helper tests."""

from __future__ import annotations

import unittest

from lora.srd import duty_cycle_budget, srd_entry


class SrdTests(unittest.TestCase):
    def test_g1_figures(self) -> None:
        e = srd_entry("g1_433")
        self.assertEqual(e["erp_mw"], 10.0)
        self.assertEqual(e["duty_cycle_percent"], 10.0)

    def test_g2_no_duty(self) -> None:
        e = srd_entry("g2_433")
        self.assertEqual(e["erp_mw"], 1.0)
        self.assertFalse(e["duty_cycle_required"])

    def test_duty_budget_packets(self) -> None:
        # 1000 ms airtime, 10% of 3600 s => 360 s budget => 360 packets
        b = duty_cycle_budget(1000.0, 10.0, window_s=3600.0)
        self.assertEqual(b["max_packets"], 360)

    def test_unknown_entry(self) -> None:
        with self.assertRaises(KeyError):
            srd_entry("not_real")


if __name__ == "__main__":
    unittest.main()
