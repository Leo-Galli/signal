# ch18-licence-qso

Companion folder for **Your Licence and First QSO** (Signal, Chapter 18).

Book steps live in the manuscript. This folder holds a four-week study calendar
validator, practice quiz / Italy syllabus checklist scoring, first-QSO cheat
card checks, station-ID checklist validation, official-directory clubs list
checks, phonetics helper, worksheets and tests.

**Not legal advice.** Sample JSON is for CI and schema practice. Replace with
your own cited notes from official sources. A practice score is not a licence.

## Layout

| Path | Purpose |
| --- | --- |
| `licence/` | Calendar, quiz, cheat card, station ID, clubs, phonetics |
| `tools/` | CLIs for validate and score |
| `data/` | Sample documents for CI |
| `bom.md` | No radio parts required |
| `worksheets/` | Printable prompts |
| `tests/` | Unit + tool tests |

## Run tests

```bash
cd ch18-licence-qso
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/validate_calendar.py data/sample_calendar.json
python tools/score_quiz.py data/sample_quiz_us.json --responses data/sample_responses_us.json
python tools/score_quiz.py data/sample_quiz_it_checklist.json
python tools/validate_cheat_card.py data/sample_cheat_card.json
python tools/validate_station_id.py data/sample_station_id.json
python tools/validate_clubs.py data/sample_clubs.json
python tools/spell_callsign.py LG
```
