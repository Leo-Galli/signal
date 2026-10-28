# Station notes template -- Chapter 4

Fill these fields, then copy values into `data/station_notes.json` and validate.

| Field | Your value |
| --- | --- |
| software_name | |
| software_version | |
| device_name | |
| sample_rate_hz | |
| ppm_correction | |
| default_gain | |
| antenna_notes | |
| last_expected_mhz | |
| last_measured_mhz | |
| iq_recording_path | |
| iq_duration_s | |
| access_date | |

Optional free notes:

Validate:

```bash
PYTHONPATH=. python tools/validate_station_notes.py data/station_notes.json
```
