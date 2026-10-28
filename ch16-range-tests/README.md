# ch16-range-tests

Companion folder for **Range Tests Done Right** (Signal, Chapter 16).

Book steps live in the manuscript. This folder holds control-sheet validation,
a blank five-point results template, RSSI-versus-distance plotting, limitation
note checks, worksheets, BOM and tests.

**Blank results only in the book sense.** Do not invent outdoor kilometer claims.
The `data/sample_results_fixture.json` file is a **synthetic CI fixture** so the
plotter has numbers to test -- not a field claim. **Not legal advice.**

## Layout

| Path | Purpose |
| --- | --- |
| `range/` | Results, controls, haversine, plot, limitation |
| `tools/` | CLIs for validate and plot |
| `data/` | Blank templates + synthetic fixture |
| `bom.md` | Parts list |
| `worksheets/` | Controls, results table, plot, limitation |
| `tests/` | Unit + tool tests |

## Run tests

```bash
cd ch16-range-tests
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/validate_controls.py data/sample_controls.json
python tools/validate_results.py data/blank_results.json
python tools/validate_results.py data/sample_results_fixture.json
python tools/plot_rssi_distance.py data/sample_results_fixture.json --out /tmp/rssi.png
python tools/validate_limitation.py data/sample_limitation.json
```
