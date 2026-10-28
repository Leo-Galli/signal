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

Chapter folders and tests land here as the book is written. Starters are expected to fail until you complete the exercise using the book.

## Folder map
| Path | Purpose |
| --- | --- |
| `ch01-waves/` ... `ch18-licence-qso/` | Per-chapter firmware, Python tools, worksheets, BOM, tests |
| `.github/workflows/` | CI (smoke now; firmware and unit tests as chapters land) |

## Finding a chapter folder
1. Open the chapter folder that matches the book companion path (for example `ch04-sdr-station`).
2. Open that folder's `README.md` for the title and book location only.
3. Follow the book for steps; run any listed tests from that folder.

## License
MIT for repository code, worksheets and diagrams. The book manuscript is not included and is not licensed under MIT.
