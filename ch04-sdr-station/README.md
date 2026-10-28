# ch04-sdr-station

Companion folder for **Your First SDR Station** (Signal, Chapter 4).

Book steps live in the manuscript. This folder holds PPM calibration helpers, station-notes validation, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `sdr/ppm.py` | Frequency error and suggested PPM correction |
| `sdr/station_notes.py` | Required-field checks for station notes JSON |
| `tools/calibrate_ppm.py` | CLI: expected vs measured MHz to ppm |
| `tools/validate_station_notes.py` | CLI to validate station notes JSON |
| `data/sample_station_notes.json` | Example notes (replace with yours) |
| `data/sample_ppm_cal.json` | Example ppm calibration numbers |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Gain settings, signal ID, station notes template |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch04-sdr-station
python -m unittest discover -s tests -v
```

## Calibrate PPM

```bash
python tools/calibrate_ppm.py --expected-mhz 100.0 --measured-mhz 100.005
```

## Validate station notes

```bash
python tools/validate_station_notes.py data/sample_station_notes.json
```

Exit code 0 means required fields are present and numeric fields parse. Replace the sample with your SDR++ or GQRX settings after the build.
