# Exercise 3 -- Test that times dit length

Capture mark/space durations from a key session (stopwatch notes, logic
analyzer, or a serial debug fork). Put them in JSON like
`data/sample_key_events.json`.

Run:

```bash
python tools/measure_dot_length.py data/sample_key_events.json --wpm-hint 20
python -m unittest tests.test_dot_timing -v
```

Record:

| Field | Value |
| --- | --- |
| average_dit_ms |  |
| expected_unit_ms (from WPM hint) |  |
| error_ms |  |
| sample_count |  |

At 20 WPM the PARIS unit is 60 ms. Your average dit should land near that
when you key cleanly. Large error usually means mixed dahs into the dit
bucket or a wrong WPM hint -- fix the measurement, do not invent a number.

Practice only. Not legal advice.
