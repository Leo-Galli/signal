# ch03-law

Companion folder for **Lawful Operation** (Signal, Chapter 3).

Book steps live in the manuscript. This folder holds jurisdiction worksheet validation, sample JSON, printable worksheets and tests.

Not legal advice. Official URLs belong in your filled worksheet; this sample data is for CI and schema checks only.

## Layout

| Path | Purpose |
| --- | --- |
| `law/jurisdiction.py` | Required-field and acknowledgement checks |
| `tools/validate_jurisdiction.py` | CLI to validate a jurisdiction JSON document |
| `data/sample_jurisdiction.json` | Example document for CI (replace with yours locally) |
| `bom.md` | No radio parts -- browser + worksheet |
| `worksheets/` | Jurisdiction, project-class map, licence-actions |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch03-law
python -m unittest discover -s tests -v
```

## Validate a worksheet JSON

```bash
python tools/validate_jurisdiction.py data/sample_jurisdiction.json
```

Exit code 0 means required fields, https URLs, ISO access date and the not-legal-advice acknowledgement are present.
