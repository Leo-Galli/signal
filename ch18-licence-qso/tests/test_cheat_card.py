"""Tests for licence.cheat_card and phonetics."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from licence.cheat_card import validate_cheat_card
from licence.phonetics import spell_callsign

DATA = Path(__file__).resolve().parents[1] / "data"


class CheatCardTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((DATA / "sample_cheat_card.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_cheat_card(doc), [])

    def test_rejects_short_script(self) -> None:
        doc = json.loads((DATA / "sample_cheat_card.json").read_text(encoding="utf-8"))
        doc["script_lines"] = ["only one line"]
        self.assertEqual(validate_cheat_card(doc), ["script_lines"])

    def test_rejects_missing_listen_ack(self) -> None:
        doc = json.loads((DATA / "sample_cheat_card.json").read_text(encoding="utf-8"))
        doc["listen_first_ack"] = "maybe"
        self.assertEqual(validate_cheat_card(doc), ["listen_first_ack"])

    def test_spell_callsign(self) -> None:
        words = spell_callsign("K1AB")
        self.assertEqual(words, ["Kilo", "One", "Alfa", "Bravo"])


if __name__ == "__main__":
    unittest.main()
