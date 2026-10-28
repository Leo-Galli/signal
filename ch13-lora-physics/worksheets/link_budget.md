# Worksheet -- first-order link budget

Copy sensitivity from YOUR module datasheet. Do not invent numbers.

| Field | Value |
| --- | --- |
| Module family | SX127x / SX126x / E22 / other: |
| Datasheet title | |
| Revision or date | |
| Table or page | |
| SF / BW used for that row | |
| Sensitivity (dBm) | |
| TX power (mW or dBm) | |
| TX antenna gain (dBi) | |
| RX antenna gain (dBi) | |
| Other losses (dB) | |
| Distance (m) | |
| Frequency (MHz) | |
| FSPL (dB) | |
| Prx (dBm) | |
| Margin (dB) | |

Validate citation JSON:

```
python tools/validate_datasheet_note.py path/to/your_note.json
```

Then:

```
python tools/compute_link_budget.py --tx-mw 10 --distance-m ... --freq-mhz ... --sensitivity-dbm ... --sensitivity-source "..."
```

Honest limitation note (one paragraph -- free-space only, no invented km claims):
