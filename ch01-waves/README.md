# ch01-waves

Companion folder for **Waves Before Wires** (Signal, Chapter 1).

Book steps live in the manuscript. This folder holds the converters, plot tool, sample scan CSV, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `waves/convert.py` | Frequency/wavelength and mW/dBm helpers |
| `tools/plot_relative_strength.py` | Plot relative strength from a two-column CSV |
| `data/sample_fm_scan.csv` | Example relative-strength scan (no live SDR required for CI) |
| `bom.md` | Parts list for the chapter build |
| `worksheets/link_diagram.md` | Blank link-diagram sketch prompt |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch01-waves
python -m unittest discover -s tests -v
```

## Plot a scan

```bash
python tools/plot_relative_strength.py data/sample_fm_scan.csv --out relative_strength.png
```

CSV columns: `frequency_mhz,relative_db` (header required). Replace the sample file with your own export from SDR++ / GQRX notes or a simple log you type by hand.
