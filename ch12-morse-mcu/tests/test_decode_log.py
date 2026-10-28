import json
import unittest
from pathlib import Path

from keyer.decode_log import DecodeLogError, validate_decode_log

ROOT = Path(__file__).resolve().parents[1]


class DecodeLogTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        payload = json.loads(
            (ROOT / "data" / "sample_decode_log.json").read_text(encoding="utf-8")
        )
        summary = validate_decode_log(payload)
        self.assertEqual(summary["decoded_text"], "PARIS")
        self.assertTrue(summary["practice_only"])

    def test_requires_practice_only_true(self) -> None:
        payload = {
            "session_id": "x",
            "board": "esp32dev",
            "wpm": 20,
            "decoded_text": "HI",
            "practice_only": False,
        }
        with self.assertRaises(DecodeLogError):
            validate_decode_log(payload)

    def test_blank_text_rejected(self) -> None:
        payload = {
            "session_id": "x",
            "board": "esp32dev",
            "wpm": 20,
            "decoded_text": "   ",
            "practice_only": True,
        }
        with self.assertRaises(DecodeLogError):
            validate_decode_log(payload)


if __name__ == "__main__":
    unittest.main()
