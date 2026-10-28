# Exercise 1 -- Filter one device ID

Date: __________

rtl_433 version / build: __________

Antenna / band note: __________

1. Run a short receive session and save JSON (`-F json`) to a file, or use your sensor-log JSON.
2. List unique ids:

```bash
python tools/filter_device_id.py path/to/log.jsonl --id x --list-ids
```

Unique ids seen: __________

3. Pick one id that belongs to a sensor you own or that you treat as anonymous practice data.
   Chosen id: __________
   Model string: __________

4. Filter:

```bash
python tools/filter_device_id.py path/to/log.jsonl --id YOUR_ID
```

Matched line count: __________

5. One sentence: why filtering by id matters before plotting or sharing notes.
___________________________________________________________________________
