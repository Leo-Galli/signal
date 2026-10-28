import unittest

from mesh.airtime import airtime_ms, symbol_time_s


class TestAirtime(unittest.TestCase):
    def test_symbol_time_sf7(self) -> None:
        self.assertAlmostEqual(symbol_time_s(7, 125_000.0), 0.001024)

    def test_airtime_positive(self) -> None:
        got = airtime_ms(7, 125_000.0, 12)
        self.assertGreater(got["airtime_ms"], 0)
        self.assertEqual(got["payload_bytes"], 12)

    def test_sf12_longer_than_sf7(self) -> None:
        a = airtime_ms(7, 125_000.0, 20)
        b = airtime_ms(12, 125_000.0, 20)
        self.assertGreater(b["airtime_ms"], a["airtime_ms"])


if __name__ == "__main__":
    unittest.main()
