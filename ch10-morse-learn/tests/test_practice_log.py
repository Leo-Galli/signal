"""Tests for practice-log validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from morse.practice_log import validate_practice_log

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_practice_log.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class PracticeLogTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_practice_log(_sample()), [])

    def test_missing_meta(self) -> None:
        doc = _sample()
        del doc["trainer_name"]
        self.assertEqual(validate_practice_log(doc), ["trainer_name"])

    def test_bad_ack(self) -> None:
        doc = _sample()
        doc["receive_only_ack"] = "nope"
        self.assertEqual(validate_practice_log(doc), ["receive_only_ack"])

    def test_wrong_day_count(self) -> None:
        doc = _sample()
        doc["days"] = doc["days"][:6]
        self.assertEqual(validate_practice_log(doc), ["days"])

    def test_effective_above_character(self) -> None:
        doc = _sample()
        doc["days"] = copy.deepcopy(doc["days"])
        doc["days"][0]["effective_wpm"] = 40
        doc["days"][0]["character_wpm"] = 20
        self.assertEqual(
            validate_practice_log(doc),
            ["days[0].effective_wpm"],
        )

    def test_accuracy_out_of_range(self) -> None:
        doc = _sample()
        doc["days"] = copy.deepcopy(doc["days"])
        doc["days"][2]["accuracy_percent"] = 140
        self.assertEqual(
            validate_practice_log(doc),
            ["days[2].accuracy_percent"],
        )


if __name__ == "__main__":
    unittest.main()
