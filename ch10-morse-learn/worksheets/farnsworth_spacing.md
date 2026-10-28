# Exercise 3 -- Adjust Farnsworth spacing

Keep character speed fixed. Change only effective (overall) speed so gaps stretch
or shrink. Listen to the same short drill at two effective speeds.

Suggested starting pair (change if your trainer uses different defaults):

- Trial A: character 20 WPM, effective 10 WPM
- Trial B: character 20 WPM, effective 15 WPM

Compute timing numbers:

```bash
python tools/farnsworth_timing.py --character-wpm 20 --effective-wpm 10
python tools/farnsworth_timing.py --character-wpm 20 --effective-wpm 15
```

Or validate `data/sample_timing.json` / your own timing JSON:

```bash
python tools/farnsworth_timing.py --json data/sample_timing.json
```

Write what you heard:

Trial A (effective _____ WPM): 
___________________________________________________________________________

Trial B (effective _____ WPM): 
___________________________________________________________________________

Which effective speed let you copy more accurately today?
___________________________________________________________________________
