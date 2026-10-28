# Contributing

This repo holds the working code, worksheets and diagrams for *Signal*.

## Rules

- English only in user-facing docs and comments.
- No secrets, callsign credentials, TTN keys or private GPS tracks.
- Keep chapter folders aligned with the book outline (`ch01-waves` through `ch18-licence-qso`).
- Add or update tests / CI jobs when you add code that appears in the book.
- Prefer small, focused pull requests.

## Local checks

Run the CI smoke path locally when you can:

```bash
python -c "print('smoke ok')"
```

Chapter-specific test commands will be documented in each chapter folder README.
