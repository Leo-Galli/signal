# Worksheet: Morse payload builder

Goal: unit-test the SOS + name + coordinates string.

1. Run: `python tools/build_morse_payload.py --name MAKER --lat 45.46427 --lon 9.18951`
2. Expect: `SOS MAKER 45.46427N 9.18951E`
3. Host tests: `python -m unittest tests.test_morse_payload -v`
4. Confirm firmware `morse_payload_build` uses the same format (no Unicode degree symbols).

Date: __________  Pass: [ ]
