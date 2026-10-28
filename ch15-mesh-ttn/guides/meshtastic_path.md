# Meshtastic path checklist (Path A)

Not legal advice. Follow current official docs; UI labels change.

Official starting points:

- https://meshtastic.org/
- https://meshtastic.org/docs/

## Steps

1. Confirm your board on the official supported-hardware documentation.
2. Install the flashing method the docs recommend for that board.
3. Flash current firmware from the official channel described in the docs.
4. Set **region** to match your location and radio band (example labels: EU868, US915).
5. Configure a teaching channel; prefer a private channel for personal text.
6. Send one short test message (second node or phone app per docs).
7. Fill `worksheets/region_settings.md` and `worksheets/path_choice.md`.
8. Run `python tools/scan_secrets.py --path .` before archiving configs near git.

## Done when

- Region written down with official URL and date checked.
- One successful test message **or** an honest failure note (wrong channel, no peer).
- No private channel keys committed.
