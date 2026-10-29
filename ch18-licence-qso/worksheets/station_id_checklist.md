# Station identification checklist

Not legal advice. Summarize ID rules from the official URL you opened; do not invent intervals.

Required:

- path_chosen
- official_url (https)
- access_date (YYYY-MM-DD)
- id_rules_summary (your short paraphrase from that page)
- checklist (at least three steps with `step` text)
- not_legal_advice_ack

Validate:

```bash
PYTHONPATH=. python tools/validate_station_id.py data/my_station_id.json
```
