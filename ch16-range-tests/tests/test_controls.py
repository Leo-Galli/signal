import json
import unittest
from pathlib import Path

from range.controls import validate_controls

ROOT = Path(__file__).resolve().parents[1]


class TestControls(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_controls.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_controls(doc), [])

    def test_missing_field(self) -> None:
        errors = validate_controls({"session_id": "x"})
        self.assertTrue(any("missing field" in e for e in errors))

    def test_bad_distance_method(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_controls.json").read_text(encoding="utf-8")
        )
        doc["distance_method"] = "guess"
        errors = validate_controls(doc)
        self.assertTrue(any("distance_method" in e for e in errors))

    def test_sf_bounds(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_controls.json").read_text(encoding="utf-8")
        )
        doc["sf"] = 6
        errors = validate_controls(doc)
        self.assertTrue(any("sf must be between" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
