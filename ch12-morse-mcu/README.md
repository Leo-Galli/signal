# ch12-morse-mcu

Companion folder for **Microcontroller Keyer and Decoder** (Signal, Chapter 12).

Book steps live in the manuscript. This folder holds ESP32/Arduino firmware
(PlatformIO), host-side WPM/decode-log/dot-timing tools, worksheets, BOM and
tests. The firmware is a practice oscillator with serial decode display --
it does not key RF.

## Layout

| Path | Purpose |
| --- | --- |
| `platformio.ini` | ESP32 (default) and Uno build envs |
| `firmware/` | Sidetone keyer + mark/space decoder |
| `keyer/` | Host Python mirrors of timing / pot / log helpers |
| `tools/` | CLI wrappers |
| `data/` | Sample decode log, pot reading, key events |
| `bom.md` | Parts list |
| `worksheets/` | WPM pot, decode log, dit-length test |
| `tests/` | Unit tests |

## Build firmware

```bash
cd ch12-morse-mcu
pio run -e esp32dev
# optional: pio run -e uno
```

Upload (on your bench, not required for CI):

```bash
pio run -e esp32dev -t upload
pio device monitor -b 115200
```

Default ESP32 pins (override in `platformio.ini` build_flags):

| Signal | GPIO |
| --- | ---: |
| KEY_PIN | 15 |
| TONE_PIN | 25 |
| POT_PIN | 34 |
| LED_PIN | 2 |

## Run host tests

```bash
cd ch12-morse-mcu
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/wpm_from_pot.py --json data/sample_pot.json
python tools/validate_decode_log.py data/sample_decode_log.json
python tools/measure_dot_length.py data/sample_key_events.json --wpm-hint 20
```

Practice oscillator only. Not legal advice. Do not connect a transmitter
to TONE_PIN or KEY_PIN until your Chapter 3 worksheet and licence path
allow a legal RF project.
