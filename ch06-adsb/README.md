# ch06-adsb

Companion folder for **Planes on a Map: ADS-B** (Signal, Chapter 6).

Book steps live in the manuscript. This folder holds session-log validation, decode-rate math, indoor/outdoor count comparison, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `adsb/rate.py` | Messages-per-minute helpers |
| `adsb/antenna.py` | Indoor vs outdoor unique-count helpers |
| `adsb/session.py` | Required-field checks for session-log JSON |
| `tools/decode_rate.py` | CLI: messages per minute |
| `tools/compare_antenna_counts.py` | CLI: compare two site counts |
| `tools/validate_session_log.py` | CLI to validate session-log JSON |
| `data/sample_session_log.json` | Example log (replace with yours) |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Indoor/outdoor, line of sight, decode rate |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch06-adsb
python -m unittest discover -s tests -v
```

## Decode rate

```bash
python tools/decode_rate.py --messages 2400 --minutes 10
```

## Compare antenna sites

```bash
python tools/compare_antenna_counts.py --indoor 3 --outdoor 12 --label-indoor indoor-desk --label-outdoor balcony
```

## Validate session log

```bash
python tools/validate_session_log.py data/sample_session_log.json
```

Exit code 0 means required fields are present and counts parse. Replace the sample with your receive-only practice notes after the build. Do not commit feeder credentials, exact home coordinates or private tracks.
