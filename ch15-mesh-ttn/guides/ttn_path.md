# TTN / The Things Stack path checklist (Path B)

Not legal advice. Follow current official docs; console labels change.

Official starting points:

- https://www.thethingsnetwork.org/
- https://www.thethingsnetwork.org/docs/
- https://www.thethingsindustries.com/docs/

## Steps

1. Create or sign in to your account per official community flow for your area.
2. Create one application.
3. Register one end device (prefer OTAA) with regional parameters matching your hardware.
4. Configure device firmware using credentials stored **outside** git (see `templates/.env.example`).
5. Attach a matched antenna; power up; complete join.
6. Send **one** unconfirmed uplink; confirm it in live data.
7. Fill region and path worksheets; run the secret scanner on your firmware directory.
8. Prefer deleting or rotating any key that appeared in a screenshot.

## Done when

- One uplink visible in the official console **or** an honest "no gateway" note.
- Region note validates with `tools/validate_region_notes.py`.
- AppKey / API tokens not in git.
