import json
import unittest
from copy import deepcopy
from pathlib import Path

from range.results import validate_results

ROOT = Path(__file__).resolve().parents[1]


class TestResults(unittest.TestCase):
    def test_blank_template_ok(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "blank_results.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_results(doc), [])

    def test_fixture_ok(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_results_fixture.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_results(doc), [])

    def test_rejects_invented_ranges(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "blank_results.json").read_text(encoding="utf-8")
        )
        doc["invented_ranges"] = True
        errors = validate_results(doc)
        self.assertTrue(any("invented_ranges" in e for e in errors))

    def test_requires_five_points(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "blank_results.json").read_text(encoding="utf-8")
        )
        doc["points"] = doc["points"][:3]
        errors = validate_results(doc)
        self.assertTrue(any("exactly 5" in e for e in errors))

    def test_empty_limitation_rejected(self) -> None:
        doc = deepcopy(
            json.loads(
                (ROOT / "data" / "blank_results.json").read_text(encoding="utf-8")
            )
        )
        doc["limitation_note"] = "   "
        errors = validate_results(doc)
        self.assertTrue(any("limitation_note" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
