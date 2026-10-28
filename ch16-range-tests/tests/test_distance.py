import math
import unittest

from range.distance import haversine_m


class TestDistance(unittest.TestCase):
    def test_zero_span(self) -> None:
        self.assertEqual(haversine_m(45.0, 9.0, 45.0, 9.0), 0.0)

    def test_short_east_west(self) -> None:
        # Roughly 111 m per 0.001 deg latitude near equator; at mid-lat smaller.
        d = haversine_m(45.0, 9.0, 45.0, 9.001)
        self.assertGreater(d, 70.0)
        self.assertLess(d, 90.0)

    def test_rejects_bad_radius(self) -> None:
        with self.assertRaises(ValueError):
            haversine_m(0.0, 0.0, 0.0, 0.0, radius_m=0.0)

    def test_known_quarter_meridian_scale(self) -> None:
        # 1 degree latitude ~ 111 km
        d = haversine_m(0.0, 0.0, 1.0, 0.0)
        self.assertTrue(math.isclose(d, 111_194.9, rel_tol=0.01))


if __name__ == "__main__":
    unittest.main()
