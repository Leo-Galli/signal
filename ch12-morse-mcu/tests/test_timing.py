import unittest

from keyer.timing import clamp_wpm, unit_ms_from_wpm, unit_seconds


class TimingTests(unittest.TestCase):
    def test_unit_seconds_20_wpm(self) -> None:
        self.assertAlmostEqual(unit_seconds(20), 0.06)

    def test_unit_ms_matches_firmware_integer(self) -> None:
        self.assertEqual(unit_ms_from_wpm(20), 60)
        self.assertEqual(unit_ms_from_wpm(12), 100)
        self.assertEqual(unit_ms_from_wpm(5), 240)

    def test_unit_seconds_rejects_non_positive(self) -> None:
        with self.assertRaises(ValueError):
            unit_seconds(0)

    def test_clamp_wpm(self) -> None:
        self.assertEqual(clamp_wpm(1), 5)
        self.assertEqual(clamp_wpm(20), 20)
        self.assertEqual(clamp_wpm(99), 40)


if __name__ == "__main__":
    unittest.main()
