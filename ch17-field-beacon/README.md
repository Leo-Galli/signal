# ch17-field-beacon

Companion folder for **Capstone: Field Beacon** (Signal, Chapter 17).

Inspired by Aegis-Beacon (MIT-licensed mountain rescue beacon on ESP32 +
E22-400M30S): this teaching build reads GPS, builds a name + lat/lon LoRa
packet, and can play the same content as Morse sidetone. It is **not**
production Aegis-Beacon. Defaults stay meek. **Dry-run mode never keys RF.**

Not legal advice. Match frequency, power and duty cycle to your Chapter 3
jurisdiction worksheet. Never send false distress.

## Layout

| Path | Purpose |
| --- | --- |
| `platformio.ini` | `esp32-beacon-dry` (CI default), SX1276 live, E22 live |
| `firmware/` | Packet, duty-cycle, GPS NMEA, Morse payload/sidetone, dry-run |
| `beacon/` | Host Python mirrors |
| `tools/` | Morse payload CLI, dry-run sim, checklist validator |
| `data/` | Sample payload, checklist, NMEA lines |
| `bom.md` | Parts list |
| `worksheets/` | Dry-run, Morse payload, field checklist |
| `tests/` | Unit + tool tests |

## Build firmware (CI builds dry-run env)

```bash
cd ch17-field-beacon
pio run -e esp32-beacon-dry
# live RF only after worksheet + antenna:
# pio run -e esp32-sx1276   # env name: esp32-beacon-sx1276
# pio run -e esp32-beacon-e22
```

Upload / monitor on your bench (not required for CI):

```bash
pio run -e esp32-beacon-dry -t upload
pio device monitor -b 115200
```

Buttons (active-low): SOS arm, SEND (LoRa or dry-run log), MORSE sidetone, DRY force.

## Run host tests

```bash
cd ch17-field-beacon
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/build_morse_payload.py --name MAKER --lat 45.46427 --lon 9.18951
python tools/dry_run_sim.py --would-key
python tools/validate_checklist.py data/sample_checklist.json
```

Never commit secrets, TTN keys or private GPS tracks. Sample coordinates in
fixtures are teaching numbers only.
