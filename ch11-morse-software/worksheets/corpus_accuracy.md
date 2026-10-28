# Worksheet: Decode accuracy on a fixed corpus

Chapter 11, Exercise 3.

## Goal

Run the fixed corpus through encode -> decode and record overall accuracy.
Do not invent scores. Use the tool output.

## Steps

```bash
cd ch11-morse-software
PYTHONPATH=. python tools/measure_accuracy.py --corpus data/sample_corpus.json --wpm 20
```

Optional: write JSON for your notes:

```bash
PYTHONPATH=. python tools/measure_accuracy.py --corpus data/sample_corpus.json --wpm 20 --json-out data/my_accuracy.json
```

## Notes (fill in)

| Phrase id | Accuracy | Decoded |
| --- | --- | --- |
| cq |  |  |
| paris |  |  |
| hello |  |  |
| digits |  |  |
| test |  |  |

- Overall accuracy:
- WPM used:
- Any phrase that failed (id + reason), or "none":
