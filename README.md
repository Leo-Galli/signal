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
| `ch09-gnuradio/` ... `ch18-licence-qso/` | Later chapters (as written) |
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


## Finding a chapter folder
1. Open the chapter folder that matches the book companion path (for example `ch08-rtl433`).
2. Open that folder's `README.md` for the title and book location only.
3. Follow the book for steps; run any listed tests from that folder.

## License
MIT for repository code, worksheets and diagrams. The book manuscript is not included and is not licensed under MIT.
