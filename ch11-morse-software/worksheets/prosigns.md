# Worksheet: Add prosigns

Chapter 11, Exercise 1.

## Goal

Encode and decode at least two prosigns using the companion alphabet.

## Supported tokens

Write prosigns in angle brackets: `<AR>`, `<SK>`, `<BT>`, `<KN>`, `<AS>`, `<SOS>`.

## Steps

1. Encode a short phrase that includes two prosigns, for example:

   ```bash
   PYTHONPATH=. python tools/encode_wav.py "CQ TEST <AR> <SK>" -o data/prosigns.wav --wpm 20
   ```

2. Decode it:

   ```bash
   PYTHONPATH=. python tools/decode_wav.py data/prosigns.wav --wpm-hint 20
   ```

3. Record the decoded string below.

## Notes (fill in)

- Phrase used:
- Decoded text:
- Did `<AR>` and `<SK>` round-trip? (yes/no):
- One sentence on when you would use AR vs SK in a real QSO (study only -- no RF required):
