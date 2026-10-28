"""Airtime formula tests (Semtech timing model)."""

from __future__ import annotations

import unittest

from lora.airtime import airtime_ms, compare_sf_airtime, symbol_time_s


class AirtimeTests(unittest.TestCase):
    def test_symbol_time_sf7_125k(self) -> None:
        self.assertAlmostEqual(symbol_time_s(7, 125000.0), 0.001024, places=9)

    def test_sf7_10byte_reference(self) -> None:
        # Classic reference: SF7, BW125k, CR4/5, 10 B, preamble 8, CRC on, explicit, no LDR
        r = airtime_ms(7, 125000.0, 10, cr=1, low_data_rate=False)
        self.assertAlmostEqual(r["airtime_ms"], 41.216, places=3)

    def test_sf12_longer_than_sf7(self) -> None:
        cmp_ = compare_sf_airtime(7, 12, 125000.0, 10, cr=1)
        self.assertGreater(cmp_["b"]["airtime_ms"], cmp_["a"]["airtime_ms"])
        self.assertGreater(cmp_["ratio_b_over_a"], 10.0)

    def test_sf12_10byte_with_ldr(self) -> None:
        r = airtime_ms(12, 125000.0, 10, cr=1, low_data_rate=True)
        self.assertAlmostEqual(r["airtime_ms"], 991.232, places=3)

    def test_invalid_sf(self) -> None:
        with self.assertRaises(ValueError):
            symbol_time_s(5, 125000.0)


if __name__ == "__main__":
    unittest.main()
