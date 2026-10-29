# First-QSO cheat card

Not legal advice. Do not key RF until your national authorization allows it.

Required fields (see `data/sample_cheat_card.json`):

- callsign_or_practice
- path_chosen
- listen_first_ack (exact: `I will listen before transmitting`)
- phonetic_name
- band_or_frequency_note
- script_lines (at least four non-empty lines)
- not_legal_advice_ack

Phonetic helper:

```bash
PYTHONPATH=. python tools/spell_callsign.py YOURCALL
```

Validate:

```bash
PYTHONPATH=. python tools/validate_cheat_card.py data/my_cheat_card.json
```
