# Worksheet: document block versions

Chapter 9, Exercise 3.

## Host

- OS:
- GNU Radio version (Help / About or package string):
- Companion build note (if shown):
- Date:

## Blocks used

| Block id | Label in palette | Notes |
| --- | --- | --- |
| rtlsdr_source or osmosdr_source | | |
| low_pass_filter | | |
| analog_wfm_rcv | | |
| audio_sink | | |
| blocks_file_source | | |
| blocks_throttle | | |
| blocks_file_sink | | |

Copy the same data into a JSON file and validate:

```bash
python tools/validate_session_notes.py data/your_block_versions.json --kind blocks
```
