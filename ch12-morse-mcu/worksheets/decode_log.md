# Exercise 2 -- Log decoded text

1. Flash the firmware and open the serial monitor at 115200 baud.
2. Send a short practice word on the straight key (for example PARIS).
3. Copy the decoded characters (ignore `#` comment lines) into a JSON file.

Template (`data/my_decode_log.json` -- keep personal callsigns private):

```json
{
  "session_id": "bench-YYYY-MM-DD-x",
  "board": "esp32dev",
  "wpm": 20,
  "decoded_text": "",
  "practice_only": true,
  "notes": ""
}
```

Validate:

```bash
python tools/validate_decode_log.py data/my_decode_log.json
```

Fill:

decoded_text observed: ________________________________

mismatches / retries: ________________________________

practice_only confirmed true: ________

Not legal advice. Do not claim RF transmit in this log.
