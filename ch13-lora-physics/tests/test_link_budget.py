"""Link-budget tests -- sensitivity must be caller-supplied."""

from __future__ import annotations

import math
import unittest

from lora.link_budget import free_space_path_loss_db, link_budget, mw_to_dbm


class LinkBudgetTests(unittest.TestCase):
    def test_mw_to_dbm_10(self) -> None:
        self.assertAlmostEqual(mw_to_dbm(10.0), 10.0, places=6)

    def test_mw_to_dbm_1(self) -> None:
        self.assertAlmostEqual(mw_to_dbm(1.0), 0.0, places=6)

    def test_fspl_1km_433mhz(self) -> None:
        # 20*log10(1) + 20*log10(433) + 32.44 ~= 85.17 dB (km form)
        fspl = free_space_path_loss_db(1000.0, 433.0)
        expected = 20 * math.log10(1.0) + 20 * math.log10(433.0) + 32.44
        self.assertAlmostEqual(fspl, expected, places=1)

    def test_margin_requires_source(self) -> None:
        with self.assertRaises(ValueError):
            link_budget(
                tx_power_dbm=10.0,
                tx_antenna_gain_dbi=0.0,
                rx_antenna_gain_dbi=0.0,
                distance_m=100.0,
                freq_mhz=433.0,
                sensitivity_dbm=-120.0,
                sensitivity_source="  ",
            )

    def test_positive_margin_fixture(self) -> None:
        # Fixture arithmetic only -- not a datasheet claim.
        r = link_budget(
            tx_power_dbm=10.0,
            tx_antenna_gain_dbi=0.0,
            rx_antenna_gain_dbi=0.0,
            distance_m=100.0,
            freq_mhz=433.0,
            sensitivity_dbm=-120.0,
            other_losses_db=0.0,
            sensitivity_source="CI fixture sensitivity row",
        )
        self.assertGreater(r["margin_db"], 0.0)
        self.assertIn("Free-space", r["note"])


if __name__ == "__main__":
    unittest.main()
