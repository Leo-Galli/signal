# ch08-rtl433

Companion folder for **Decoding the ISM Band with rtl_433** (Signal, Chapter 8).

Book steps live in the manuscript. This folder holds sensor-log validation, device-id filtering, temperature summary/plot helpers, privacy-note checks, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `rtl433/log.py` | Required-field checks for sensor-log JSON |
| `rtl433/filter_id.py` | Filter records by device id |
| `rtl433/temperature.py` | Celsius series + summary |
| `rtl433/privacy.py` | Privacy-note required fields |
| `tools/validate_sensor_log.py` | CLI: validate sensor-log JSON |
| `tools/filter_device_id.py` | CLI: filter JSONL / log by id |
| `tools/plot_temperature.py` | CLI: summarize / plot temperature_C |
| `tools/validate_privacy_note.py` | CLI: validate privacy-note JSON |
| `data/sample_sensor_log.json` | Example wrapped log (replace with yours) |
| `data/sample_rtl433.jsonl` | Example raw rtl_433 JSON lines |
| `data/sample_privacy_note.json` | Example privacy note |
| `bom.md` | Parts list for the chapter build |
| `worksheets/` | Filter, temperature hour, privacy |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch08-rtl433
python -m unittest discover -s tests -v
```

## Validate sensor log

```bash
python tools/validate_sensor_log.py data/sample_sensor_log.json
```

## Filter by device id

```bash
python tools/filter_device_id.py data/sample_rtl433.jsonl --list-ids
python tools/filter_device_id.py data/sample_rtl433.jsonl --id 1001
```

## Temperature summary

```bash
python tools/plot_temperature.py data/sample_sensor_log.json --id 1001
```

Optional PNG (needs matplotlib):

```bash
python tools/plot_temperature.py data/sample_sensor_log.json --id 1001 --out temp.png
```

## Privacy note

```bash
python tools/validate_privacy_note.py data/sample_privacy_note.json
```

Exit code 0 means required fields are present. Replace samples with your receive-only practice notes after the build. Do not commit neighbor addresses, exact home coordinates or long-term raw dumps of other people's sensors.
