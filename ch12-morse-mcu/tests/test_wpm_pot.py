import unittest

from keyer.wpm_pot import wpm_from_adc


class WpmPotTests(unittest.TestCase):
    def test_endpoints_esp32(self) -> None:
        self.assertEqual(wpm_from_adc(0, 4095), 5)
        self.assertEqual(wpm_from_adc(4095, 4095), 40)

    def test_mid_esp32(self) -> None:
        self.assertEqual(wpm_from_adc(2048, 4095), 22)

    def test_uno_scale(self) -> None:
        self.assertEqual(wpm_from_adc(0, 1023), 5)
        self.assertEqual(wpm_from_adc(1023, 1023), 40)

    def test_rejects_bad_max(self) -> None:
        with self.assertRaises(ValueError):
            wpm_from_adc(0, 0)


if __name__ == "__main__":
    unittest.main()
