# ch09-gnuradio

Companion folder for **GNU Radio Without Fear** (Signal, Chapter 9).

Book steps live in the manuscript. This folder holds checked-in `.grc` flowgraphs, sample-rate helpers, session-note validators, worksheets, BOM and tests.

GNU Radio itself is not installed in CI. Tests parse the `.grc` files and exercise Python helpers only.

## Layout

| Path | Purpose |
| --- | --- |
| `flowgraphs/wbfm_rtl_receive.grc` | Minimal live WBFM receive graph (RTL-SDR -> LPF -> WBFM -> Audio) |
| `flowgraphs/wbfm_file_source.grc` | File Source + Throttle practice graph (optional File Sink) |
| `gnuradio/sample_rates.py` | RF / quadrature / audio rate math |
| `gnuradio/grc_parse.py` | Required-block checks for the `.grc` files |
| `gnuradio/session_notes.py` | Session-notes + block-versions validation |
| `tools/validate_grc.py` | CLI: validate a `.grc` |
| `tools/check_sample_rates.py` | CLI: print rate chain |
| `tools/validate_session_notes.py` | CLI: validate session or block-versions JSON |
| `data/` | Example notes JSON (replace with yours) |
| `bom.md` | Parts list |
| `worksheets/` | Filter bandwidth, file sink, block versions |
| `tests/` | Unit tests |

## Run tests

```bash
cd ch09-gnuradio
python -m unittest discover -s tests -v
```

## Validate flowgraphs

```bash
python tools/validate_grc.py flowgraphs/wbfm_rtl_receive.grc --kind live
python tools/validate_grc.py flowgraphs/wbfm_file_source.grc --kind file
```

## Sample-rate chain

```bash
python tools/check_sample_rates.py --rf-rate 2400000 --channel-decim 10 --audio-decim 5
```

## Session notes

```bash
python tools/validate_session_notes.py data/sample_session_notes.json
python tools/validate_session_notes.py data/sample_block_versions.json --kind blocks
```

Open the `.grc` files in GNU Radio Companion on your machine. On some installs the live source block is Osmocom Source (`osmosdr_source`) instead of RTL-SDR Source -- retarget the source block if your palette differs, and document the id you used.

Receive-only. Not legal advice. Do not commit large IQ or audio captures.
