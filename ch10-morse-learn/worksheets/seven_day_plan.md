# Hands-on -- 7-day Morse practice plan

Use headphones and one open-source or free trainer listed in this folder's `README.md`.
Copy (receive by ear). Do not transmit RF for this worksheet.

Fill `data/practice_log.json` (copy from `data/sample_practice_log.json`) with your
own minutes, WPM and accuracy. Sample numbers are placeholders -- replace them.

Then run:

```bash
python tools/validate_practice_log.py data/practice_log.json
```

Daily targets (adjust to your life; honesty beats heroic minutes you invent):

| Day | Focus | Suggested minutes |
| --- | --- | ---: |
| 1 | Install trainer; learn two Koch characters at target character speed | 20 |
| 2 | Same characters; Farnsworth effective speed as set on day 1 | 20 |
| 3 | Add one character if accuracy held; else repeat | 20-25 |
| 4 | Mixed groups; log accuracy honestly | 20 |
| 5 | One-minute solid copy attempt (Exercise 2 warm-up) | 20 |
| 6 | Shorter session OK; protect the habit | 15-20 |
| 7 | Review week; note plateau or win in `notes` | 20-25 |

`receive_only_ack` must be `yes`, `true`, or `acknowledged` in the JSON.

This worksheet is practice hygiene, not a licence exam. Not legal advice.
