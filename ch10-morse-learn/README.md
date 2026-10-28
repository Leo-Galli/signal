# ch10-morse-learn

Companion folder for **Learning Morse by Ear** (Signal, Chapter 10).

Book steps live in the manuscript. This folder holds practice-log validators,
Farnsworth timing helpers, Koch-order lookup, worksheets, BOM and tests.

## Open trainers (pick one)

| Trainer | Notes |
| --- | --- |
| Learn CW Online (LCWO) | https://lcwo.net/ -- browser Koch / Farnsworth practice |
| unixcw (`cwcp`) | Terminal Morse tutor on many Linux distros |
| aldo | Unix Morse code tutor (package name varies by distro) |
| ebook2cw | https://github.com/DJ1YFK/ebook2cw -- text to Morse audio (pair with any player) |

Install instructions change; follow each project's current README. The book does
not require RF transmit for Chapter 10.

## Layout

| Path | Purpose |
| --- | --- |
| `morse/timing.py` | PARIS unit + Farnsworth gap math |
| `morse/practice_log.py` | Seven-day practice-log validation |
| `morse/practice_string.py` | Initials / callsign-shaped practice strings |
| `morse/koch.py` | LCWO-style Koch character order |
| `tools/` | CLI wrappers |
| `data/` | Sample JSON (replace with yours) |
| `bom.md` | Parts list |
| `worksheets/` | 7-day plan, practice string, 1-minute copy, Farnsworth |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch10-morse-learn
python -m unittest discover -s tests -v
```

## Practice log

```bash
python tools/validate_practice_log.py data/sample_practice_log.json
```

## Farnsworth timing

```bash
python tools/farnsworth_timing.py --character-wpm 20 --effective-wpm 10
```

Receive-only practice framing for the chapter worksheets. Not legal advice.
Do not commit private callsign credentials or exam answers.
