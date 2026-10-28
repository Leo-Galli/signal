# Exercise: fill the blank five-point results table

Copy `data/blank_results.json` or use the CSV. Leave empty cells empty. Do not invent ranges.

Session id: ____________  Date: ____________  Region: ____________

Fixed height (m): ______  Walking height (m): ______

SF: ____  BW (kHz): ____  CR: ____  TX (dBm): ____  Payload bytes: ____

Antenna fixed: ____________  Antenna walking: ____________  Distance method: ____________

| Point | Time | Distance_m | Lat | Lon | RSSI_dBm | SNR_dB | Decode (Y/N) | Notes |
| ---: | --- | ---: | --- | --- | ---: | ---: | --- | --- |
| 1 |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

Validate:

```bash
PYTHONPATH=. python tools/validate_results.py path/to/your_results.json
```
