"""Tests for wxsat.artifacts validation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from wxsat.artifacts import validate_artifact_rating

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_artifact_rating.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class ArtifactTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_artifact_rating(_sample()), [])

    def test_missing_notes(self) -> None:
        doc = _sample()
        del doc["notes"]
        self.assertEqual(validate_artifact_rating(doc), ["notes"])

    def test_bad_source(self) -> None:
        doc = _sample()
        doc["image_source"] = "fake-noaa-live"
        self.assertEqual(validate_artifact_rating(doc), ["image_source"])

    def test_bad_usable(self) -> None:
        doc = _sample()
        doc["overall_usable"] = "maybe"
        self.assertEqual(validate_artifact_rating(doc), ["overall_usable"])


if __name__ == "__main__":
    unittest.main()
