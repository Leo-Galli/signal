# Signal companion repository

[![ci](https://github.com/Leo-Galli/signal/actions/workflows/ci.yml/badge.svg)](https://github.com/Leo-Galli/signal/actions/workflows/ci.yml)

This repository accompanies **Signal: Radio for Makers -- SDR, Morse, LoRa and Your License** by Leonardo Galli.

Instructions for exercises and chapter walkthroughs are printed in the book only. This repository does not contain the manuscript.

## Quick start

### Windows (PowerShell)
```powershell
git clone https://github.com/Leo-Galli/signal.git
cd signal
python -c "print('smoke ok')"
```

### macOS / Linux
```bash
git clone https://github.com/Leo-Galli/signal.git
cd signal
python -c "print('smoke ok')"
```

Chapter folders land as the book is written. Follow the book for lab steps; run that chapter's tests from its folder.

## Folder map
| Path | Purpose |
| --- | --- |
| `ch01-waves/` | Wavelength/dBm converters, relative-strength plot tool, sample CSV, BOM |
| `ch02-safety/` | Field checklist + 5 V rail-verify validators, worksheets, BOM |
| `ch03-law/` | Jurisdiction worksheet validator, official-URL worksheets, BOM |
| `ch04-sdr-station/` | PPM calibration, station-notes validator, worksheets, BOM |
| `ch05-fm-airband/` | Listening-log validator, relative SNR compare, worksheets, BOM |
| `ch06-adsb/` | ADS-B session-log validator, decode-rate + antenna compare, worksheets, BOM |
| `ch07-wxsat/` | WX sat Doppler + pass-log + practice APT WAV/PNG, worksheets, BOM |
| `ch08-rtl433/` | rtl_433 sensor-log + device filter + temperature plot, worksheets, BOM |
| `ch09-gnuradio/` | GNU Radio WBFM `.grc` flowgraphs + sample-rate / session-note tools, worksheets, BOM |
| `ch10-morse-learn/` | Morse ear-training practice log + Farnsworth timing + Koch order, worksheets, BOM |
| `ch11-morse-software/` | Morse encode/decode WAV tools + corpus accuracy + timing fuzz, worksheets, BOM |
| `ch12-morse-mcu/` | ESP32/Arduino Morse keyer+decoder firmware + WPM/decode-log tools, worksheets, BOM |
| `ch13-lora-physics/` | LoRa airtime + first-order link budget + SRD duty-cycle helpers, worksheets, BOM |
| `ch14-esp32-lora/` | ESP32 LoRa P2P firmware + packet/duty-cycle/RSSI tools |
| `ch15-mesh-ttn/` | Meshtastic/TTN guides + airtime/region/opsec tools |
| `ch16-range-tests/` | Range-walk controls + blank results + RSSI plot tools |
| `ch17-field-beacon/` | Field beacon dry-run firmware + Morse payload tools |
| `ch18-licence-qso/` | Licence study calendar + practice quiz + QSO cheat card tools |
| `.github/workflows/` | CI smoke plus per-chapter test jobs |

### Chapter 1 tests
```bash
cd ch01-waves
pip install matplotlib   # optional locally; required for PNG output
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 2 tests
```bash
cd ch02-safety
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 3 tests
```bash
cd ch03-law
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 4 tests
```bash
cd ch04-sdr-station
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 5 tests
```bash
cd ch05-fm-airband
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 6 tests
```bash
cd ch06-adsb
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 7 tests
```bash
cd ch07-wxsat
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 8 tests
```bash
cd ch08-rtl433
pip install matplotlib   # optional locally; required for PNG output
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 9 tests
```bash
cd ch09-gnuradio
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 10 tests
```bash
cd ch10-morse-learn
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 11 tests
```bash
cd ch11-morse-software
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 12 tests and firmware build
```bash
cd ch12-morse-mcu
PYTHONPATH=. python -m unittest discover -s tests -v
pio run -e esp32dev   # requires PlatformIO; CI runs this job
```

### Chapter 13 tests
```bash
cd ch13-lora-physics
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Chapter 18 tests
```bash
cd ch18-licence-qso
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Finding a chapter folder
1. Open the chapter folder that matches the book companion path (for example `ch13-lora-physics`).
2. Open that folder's `README.md` for the title and book location only.
3. Follow the book for steps; run any listed tests from that folder.

## License
MIT for repository code, worksheets and diagrams. The book manuscript is not included and is not licensed under MIT.
