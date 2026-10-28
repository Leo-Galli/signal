# ch15-mesh-ttn

Companion folder for **Meshtastic and The Things Network** (Signal, Chapter 15).

Book steps live in the manuscript. This folder holds airtime comparison tools,
region-note validation, secret scanning, path checklists for Meshtastic and TTN,
worksheets, BOM and tests.

Reader chooses **one** hands-on path: flash Meshtastic on a supported board, or
register a TTN application and send one uplink. Companion provides both
checklists. **Not legal advice.** Never commit AppKeys, API tokens, private
channel keys or GPS tracks.

## Layout

| Path | Purpose |
| --- | --- |
| `mesh/` | Airtime, compare, region labels, secret scan |
| `tools/` | CLIs for compare, validate, scan |
| `guides/` | Meshtastic and TTN durable checklists |
| `templates/` | `.env.example` and note templates (no live secrets) |
| `data/` | Sample fixtures |
| `bom.md` | Parts list |
| `worksheets/` | Airtime, misconfig, region, path choice |
| `tests/` | Unit + tool tests |

## Run tests

```bash
cd ch15-mesh-ttn
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/compare_airtime.py --mesh-text "HELP BASE 1" --uplink-bytes 12 --sf 7
python tools/validate_region_notes.py data/sample_region_notes.json
python tools/validate_opsec_note.py data/sample_opsec_note.json
python tools/scan_secrets.py --path templates --path data
```

Official docs change; prefer:

- https://meshtastic.org/docs/
- https://www.thethingsnetwork.org/docs/
