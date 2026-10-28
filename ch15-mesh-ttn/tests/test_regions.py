import json
import unittest
from pathlib import Path

from mesh.regions import known_region, normalize_region, validate_region_note

ROOT = Path(__file__).resolve().parents[1]


class TestRegions(unittest.TestCase):
    def test_normalize(self) -> None:
        self.assertEqual(normalize_region(" eu868 "), "EU868")

    def test_known_eu868(self) -> None:
        got = known_region("EU868")
        self.assertEqual(got["label"], "EU868")

    def test_sample_note_ok(self) -> None:
        note = json.loads((ROOT / "data" / "sample_region_notes.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_region_note(note), [])

    def test_missing_field(self) -> None:
        errors = validate_region_note({"region": "EU868"})
        self.assertTrue(any("missing field" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
