# Exercise 1 -- Practice string (initials or callsign-shaped)

If you are unlicensed, use your initials (2-4 letters) or a short nonsense
practice token. If you hold a licence, you may use your own callsign.

Do not invent someone else's callsign as "yours."

Draft here, then put the same values in `data/practice_string.json`:

practice_text: ________________________________

kind_expected (`initials` / `callsign_shaped` / `practice_token`): ________

licensed_or_unlicensed (`licensed` / `unlicensed` / `studying`): ________

notes (why this string; if callsign-shaped while unlicensed, say it is practice only):
___________________________________________________________________________

Validate:

```bash
python tools/validate_practice_string.py data/practice_string.json
```
