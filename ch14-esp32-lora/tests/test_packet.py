import binascii
import unittest

from lora.packet import crc16_ccitt, decode, encode


class TestPacket(unittest.TestCase):
    def test_roundtrip(self) -> None:
        raw = encode(1, "ping", 0.0, 0.0)
        got = decode(raw)
        self.assertEqual(got["seq"], 1)
        self.assertEqual(got["name"], "ping")
        self.assertEqual(got["lat"], 0.0)
        self.assertEqual(got["lon"], 0.0)

    def test_crc_changes_with_payload(self) -> None:
        a = encode(1, "ping", 0.0, 0.0)
        b = encode(2, "ping", 0.0, 0.0)
        self.assertNotEqual(a, b)
        self.assertNotEqual(crc16_ccitt(a[:-2]), crc16_ccitt(b[:-2]))

    def test_bad_crc_rejected(self) -> None:
        raw = bytearray(encode(1, "ping", 0.0, 0.0))
        raw[-1] ^= 0xFF
        with self.assertRaises(ValueError):
            decode(bytes(raw))

    def test_name_too_long(self) -> None:
        with self.assertRaises(ValueError):
            encode(1, "x" * 16, 0.0, 0.0)

    def test_stable_hex_prefix(self) -> None:
        raw = encode(1, "ping", 0.0, 0.0)
        hex_s = binascii.hexlify(raw).decode("ascii")
        # magic S1, seq=1 LE, name_len=4, "ping"
        self.assertTrue(hex_s.startswith("533101000470696e67"))
        self.assertEqual(len(raw), 19)


if __name__ == "__main__":
    unittest.main()
