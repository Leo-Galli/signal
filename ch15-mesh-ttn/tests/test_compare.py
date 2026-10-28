import unittest

from mesh.compare import compare_mesh_vs_uplink, mesh_payload_bytes


class TestCompare(unittest.TestCase):
    def test_mesh_bytes_utf8(self) -> None:
        self.assertEqual(mesh_payload_bytes("HELP BASE 1"), 11)

    def test_longer_mesh_when_text_bigger(self) -> None:
        got = compare_mesh_vs_uplink("HELP BASE 1 AND MORE TEXT", 4, sf=7, bw_hz=125_000.0)
        self.assertEqual(got["longer"], "mesh_text")
        self.assertGreater(got["ratio_mesh_over_uplink"], 1.0)

    def test_equal_when_same_size(self) -> None:
        text = "ABCDEFGHIJK"  # 11 bytes
        got = compare_mesh_vs_uplink(text, 11, sf=7, bw_hz=125_000.0)
        self.assertEqual(got["longer"], "equal")
        self.assertAlmostEqual(got["ratio_mesh_over_uplink"], 1.0)


if __name__ == "__main__":
    unittest.main()
