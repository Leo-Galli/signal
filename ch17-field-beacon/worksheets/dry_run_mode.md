# Worksheet: Dry-run mode

Goal: prove the beacon never keys RF while dry-run is active.

1. Flash `esp32-beacon-dry` (compile-time `DRY_RUN=1`).
2. Arm SOS, press SEND. Serial must print `DRY-RUN: would TX` and never claim a live transmit.
3. Press MORSE. Confirm sidetone / serial Morse text only.
4. Press DRY. Confirm dry-run stays ON (compile force cannot clear).
5. Host check: `python tools/dry_run_sim.py --would-key` -> `keyed_rf: false`.

Date: __________  Pass: [ ]  Notes: __________
