# ch13-lora-physics

Companion folder for **LoRa From First Principles** (Signal, Chapter 13).

Book steps live in the manuscript. This folder holds Semtech-style airtime math, a first-order free-space link budget (sensitivity pasted from your datasheet), SRD duty-cycle planning helpers, a runnable lab script, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `lora/airtime.py` | Symbol time + packet airtime |
| `lora/link_budget.py` | FSPL + margin (sensitivity required + cited) |
| `lora/srd.py` | Locked ERC/REC 70-03 planning entries + duty-cycle budget |
| `tools/compute_airtime.py` | CLI airtime |
| `tools/compare_sf.py` | CLI SF7 vs SF12 (or any pair) |
| `tools/compute_link_budget.py` | CLI link budget |
| `tools/duty_cycle_packets.py` | CLI max packets under duty cycle |
| `tools/validate_datasheet_note.py` | CLI datasheet citation JSON check |
| `notebooks/link_budget_lab.py` | Runnable lab walkthrough |
| `data/sample_*.json` | CI fixtures (not datasheet claims) |
| `worksheets/` | SF airtime, link budget, duty cycle |
| `tests/` | Unit + tool tests |

## Run tests

```bash
cd ch13-lora-physics
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Lab script

```bash
PYTHONPATH=. python notebooks/link_budget_lab.py
```

## Compare SF7 vs SF12

```bash
python tools/compare_sf.py --sf-a 7 --sf-b 12 --payload 10
```

## Link budget (paste YOUR sensitivity)

```bash
python tools/compute_link_budget.py --tx-mw 10 --distance-m 1000 --freq-mhz 433 \
  --sensitivity-dbm -120 --sensitivity-source "replace with datasheet citation"
```

Sample JSON under `data/` is marked `fixture_only`. Replace sensitivity with a number from the datasheet row that matches your SF and bandwidth. Do not treat fixture margins as field range.
