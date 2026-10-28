# ch11-morse-software

Companion folder for **Encode and Decode CW in Software** (Signal, Chapter 11).

Book steps live in the manuscript. This folder holds a Morse alphabet table,
PARIS timing, WAV encode/decode CLIs, a timing-fuzz helper, a fixed corpus
accuracy tool, worksheets, BOM and tests.

## Layout

| Path | Purpose |
| --- | --- |
| `morse/alphabet.py` | International Morse + prosigns |
| `morse/timing.py` | PARIS unit length |
| `morse/encode.py` | Text to on/off timeline |
| `morse/audio.py` | Tone synthesis and WAV I/O |
| `morse/decode.py` | Envelope decoder |
| `morse/corpus.py` | Fixed phrases + accuracy scoring |
| `tools/` | CLI wrappers |
| `data/` | Sample corpus / phrase |
| `bom.md` | Parts list |
| `worksheets/` | Prosigns, timing fuzz, corpus accuracy |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch11-morse-software
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Encode text to WAV

```bash
python tools/encode_wav.py "HELLO WORLD" -o /tmp/hello.wav --wpm 20
```

## Decode WAV to text

```bash
python tools/decode_wav.py /tmp/hello.wav --wpm-hint 20
```

## Fuzz timing +/- 10%

```bash
python tools/fuzz_timing.py "PARIS" --wpm 20 --scales 0.9,1.0,1.1
```

## Measure corpus accuracy

```bash
python tools/measure_accuracy.py --corpus data/sample_corpus.json --wpm 20
```

Host-only practice audio. Not legal advice. Do not key RF from these WAVs
unless your Chapter 3 worksheet and licence allow it.
