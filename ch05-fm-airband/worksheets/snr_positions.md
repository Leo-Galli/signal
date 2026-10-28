# SNR / quality at two antenna positions

Keep frequency, mode, PPM, sample rate, and gain fixed. Change only antenna position.

| Field | Position A | Position B |
| --- | --- | --- |
| Label | | |
| Description (desk / window / balcony / other) | | |
| Frequency MHz | | |
| Mode (WBFM or AM) | | |
| Relative score (1-5 or meter reading) | | |
| Notes (noise, overload, body shadow) | | |

Preferred position for next session:

Why:

CLI check (optional):

```bash
python tools/compare_snr.py --position-a N --position-b N --label-a A --label-b B
```
