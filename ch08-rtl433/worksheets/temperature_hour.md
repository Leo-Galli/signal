# Exercise 2 -- Plot temperature over an hour

Date: __________

Device id used: __________

Session start: __________  Session end: __________

1. Keep JSON lines for about 60 minutes (or note if your sensor transmits less often).
2. Filter to your id, then summarize / plot:

```bash
python tools/plot_temperature.py path/to/log.json --id YOUR_ID
python tools/plot_temperature.py path/to/log.json --id YOUR_ID --out temp.png
```

Paste the summary line here:
___________________________________________________________________________

Sample count: __________  Min C: __________  Max C: __________  Mean C: __________

3. If you have fewer than several samples in an hour, write why (sparse TX interval, weak signal, wrong id) -- do not invent temperatures.
___________________________________________________________________________
