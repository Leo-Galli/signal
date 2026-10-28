import json
import unittest
from pathlib import Path

from range.limitation import validate_limitation

ROOT = Path(__file__).resolve().parents[1]


class TestLimitation(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_limitation.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_limitation(doc), [])

    def test_too_short(self) -> None:
        errors = validate_limitation({"limitation_note": "too short"})
        self.assertTrue(any("40 characters" in e for e in errors))

    def test_bans_brag_phrase(self) -> None:
        errors = validate_limitation(
            {
                "limitation_note": (
                    "This walk proves I got 20 km under every condition forever."
                )
            }
        )
        self.assertTrue(any("kilometer brags" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
