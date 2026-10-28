# ch02-safety

Companion folder for **Safety on the Bench and in the Field** (Signal, Chapter 2).

Book steps live in the manuscript. This folder holds checklist validation, rail-verify log checks, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `safety/checklist.py` | Required-field checks for field checklist and rail-verify logs |
| `tools/validate_rail_log.py` | CLI to validate a rail-verify JSON log |
| `data/sample_checklist.json` | Example filled checklist (replace with yours) |
| `data/sample_rail_verify_log.json` | Example rail verify log for CI |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Field card, pre-power checklist, packing list |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch02-safety
python -m unittest discover -s tests -v
```

## Validate a rail log

```bash
python tools/validate_rail_log.py data/sample_rail_verify_log.json
```

Exit code 0 means all required fields are present and non-empty. Replace the sample with your multimeter results after the build.
