# Timed practice quiz / syllabus checklist

Not legal advice. Not an official exam.

## US path

1. Prefer the current public Element 2 question pool from official examination sources.
2. Optionally warm up with companion `data/sample_quiz_us.json` (original practice items).
3. Time yourself (for example 25-30 minutes for the companion set).
4. Write answers in a responses JSON map, then score:

```bash
PYTHONPATH=. python tools/score_quiz.py data/sample_quiz_us.json --responses data/my_responses_us.json
```

## Italy path

1. Open CEPT T/R 61-02 and current MIMIT pages.
2. Use `data/sample_quiz_it_checklist.json` as a readiness checklist template.
3. Set each `ready` flag honestly after study, then score:

```bash
PYTHONPATH=. python tools/score_quiz.py data/sample_quiz_it_checklist.json
```

A score is a study signal only. It is not authorization to transmit.
