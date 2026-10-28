# Rate image artifacts

Inspect the practice PNG from `apt_practice_roundtrip.py`, or a live decode if you completed one. Do not rate a fabricated NOAA APT capture.

| Field | Value |
| --- | --- |
| Access date | |
| Image source (`companion-practice-wav` / `live-meteor-lrpt` / `live-other` / `archived-public-sample`) | |
| Sync quality (`clean` / `intermittent` / `lost` / `n/a`) | |
| Noise level (`low` / `medium` / `high` / `n/a`) | |
| Slant or skew (`none` / `mild` / `severe` / `n/a`) | |
| Overall usable (`yes` / `partial` / `no`) | |
| Notes (what you see; limitations) | |

After filling, copy the same fields into JSON and run:

```bash
PYTHONPATH=. python tools/rate_artifacts.py data/sample_artifact_rating.json
```

Replace the sample file with yours before treating the result as your lab record.
