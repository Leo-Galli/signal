# Worksheet: Fuzz timing +/- 10%

Chapter 11, Exercise 2.

## Goal

Show that a clean envelope decoder still recovers a known phrase when every
element duration is scaled by 0.9 and by 1.1.

## Steps

```bash
cd ch11-morse-software
PYTHONPATH=. python tools/fuzz_timing.py "PARIS HELLO" --wpm 20 --scales 0.9,1.0,1.1
```

## Notes (fill in)

| Scale | Accuracy | Decoded text |
| --- | --- | --- |
| 0.9 |  |  |
| 1.0 |  |  |
| 1.1 |  |  |

- Did all three scales stay at accuracy 1.0? (yes/no):
- One sentence on why a +/- 10% stretch is useful before MCU timing jitter:
