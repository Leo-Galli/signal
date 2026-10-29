"""Tests for licence.clubs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from licence.clubs import validate_clubs

DATA = Path(__file__).resolve().parents[1] / "data"


class ClubsTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((DATA / "sample_clubs.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_clubs(doc), [])

    def test_rejects_discord(self) -> None:
        doc = json.loads((DATA / "sample_clubs.json").read_text(encoding="utf-8"))
        doc["resources"][0]["url"] = "https://discord.com/invite/example"
        self.assertEqual(validate_clubs(doc), ["resources[0].url"])

    def test_rejects_too_few(self) -> None:
        doc = json.loads((DATA / "sample_clubs.json").read_text(encoding="utf-8"))
        doc["resources"] = doc["resources"][:1]
        self.assertEqual(validate_clubs(doc), ["resources"])


if __name__ == "__main__":
    unittest.main()
