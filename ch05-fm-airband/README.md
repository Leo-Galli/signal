# ch05-fm-airband

Companion folder for **Broadcast FM and Airband Listening** (Signal, Chapter 5).

Book steps live in the manuscript. This folder holds listening-log validation, relative antenna-position comparison, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `listening/snr.py` | Relative score delta and preferred position |
| `listening/log.py` | Required-field checks for listening-log JSON |
| `tools/compare_snr.py` | CLI: compare two unitless position scores |
| `tools/validate_listen_log.py` | CLI to validate listening-log JSON |
| `data/sample_listen_log.json` | Example log (replace with yours) |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Why AM, SNR positions, ethics rules |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch05-fm-airband
python -m unittest discover -s tests -v
```

## Compare antenna positions

```bash
python tools/compare_snr.py --position-a 3 --position-b 5 --label-a desk --label-b window
```

## Validate listening log

```bash
python tools/validate_listen_log.py data/sample_listen_log.json
```

Exit code 0 means required fields are present and modes/frequencies parse. Replace the sample with your receive-only practice notes after the build. Do not commit private recordings or sensitive operational details.
