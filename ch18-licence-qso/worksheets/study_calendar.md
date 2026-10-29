# Four-week study calendar

Not legal advice. Fill from official syllabus / question-pool sources for your path.

Copy structure into `data/my_calendar.json` (start from `data/sample_calendar.json`).

## Header

- path_chosen: `italy_mimit` | `us_fcc` | `other`
- start_date: YYYY-MM-DD
- not_legal_advice_ack: exact phrase from the sample JSON

## Weeks

Exactly four weeks. Each week needs a theme and seven days.

For each day:

- focus: short study target (blank only if minutes is 0)
- minutes: non-negative integer
- done: true/false when you finish

## Validate

```bash
PYTHONPATH=. python tools/validate_calendar.py data/my_calendar.json
```
