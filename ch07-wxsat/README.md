# ch07-wxsat

Companion folder for **Weather from Orbit** (Signal, Chapter 7).

Book steps live in the manuscript. This folder holds Doppler math, pass-log validation, practice APT encode/decode to grayscale PNG, artifact-rating validation, worksheets, BOM and tests.

Classic NOAA POES APT (NOAA-15/18/19) was decommissioned in 2025. The practice WAV/PNG path is a lab pattern only -- not a satellite image and not a live NOAA APT capture.

## Layout

| Path | Purpose |
| --- | --- |
| `wxsat/doppler.py` | First-order Doppler helpers |
| `wxsat/pass_log.py` | Required-field checks for pass-log JSON |
| `wxsat/artifacts.py` | Artifact-rating checklist validation |
| `wxsat/apt_practice.py` | Practice WAV encode + grayscale PNG decode |
| `tools/doppler_shift.py` | CLI: Doppler shift |
| `tools/validate_pass_log.py` | CLI: validate pass-log JSON |
| `tools/rate_artifacts.py` | CLI: validate artifact-rating JSON |
| `tools/apt_practice_roundtrip.py` | CLI: practice WAV -> PNG |
| `data/sample_pass_log.json` | Example pass log (replace with yours) |
| `data/sample_artifact_rating.json` | Example artifact rating |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Pass predict, Doppler, artifacts |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch07-wxsat
python -m unittest discover -s tests -v
```

## Doppler example

```bash
python tools/doppler_shift.py --carrier-hz 137100000 --v-radial-mps 1000
```

## Practice grayscale image

```bash
python tools/apt_practice_roundtrip.py --lines 64
```

## Validate logs

```bash
python tools/validate_pass_log.py data/sample_pass_log.json
python tools/rate_artifacts.py data/sample_artifact_rating.json
```

Exit code 0 means required fields parse. Replace samples with your receive-only practice notes. Do not commit exact home coordinates or claim sample rows are live NOAA APT.
