# ch14-esp32-lora

Companion folder for **ESP32 with SX127x, SX126x and E22** (Signal, Chapter 14).

Book steps live in the manuscript. This folder holds PlatformIO firmware for a
two-node LoRa ping (RSSI/SNR on serial), host-side packet/CRC/duty-cycle tools,
worksheets, BOM and tests.

Fail-safe defaults: low TX power (`LORA_TX_DBM=2`), software duty-cycle cap
(`DUTY_CYCLE_PERCENT=10`), SF7 / 125 kHz / CR 4/5, CRC-16 + sequence in the
payload. Module max power can exceed EU SRD planning highlights -- match
settings to your Chapter 3 worksheet. **Not legal advice.**

## Layout

| Path | Purpose |
| --- | --- |
| `platformio.ini` | SX1276 / SX1262 / E22 envs, node A (ping) and B (pong) |
| `firmware/` | Packet, duty-cycle gate, airtime estimate, RadioLib P2P |
| `lora/` | Host Python mirrors |
| `tools/` | CLI encode/decode, duty-cycle sim, RSSI log validator |
| `data/` | Sample packet + RSSI log fixtures |
| `bom.md` | Parts list |
| `worksheets/` | RSSI walk, duty-cycle cap, CRC/sequence |
| `tests/` | Unit + tool tests |

## Build firmware (CI builds node A SX1276)

```bash
cd ch14-esp32-lora
pio run -e esp32-sx1276-a
pio run -e esp32-sx1276-b
# also: esp32-sx1262-a/b , esp32-e22-a/b
```

Upload on your bench (not required for CI):

```bash
pio run -e esp32-sx1276-a -t upload
pio run -e esp32-sx1276-b -t upload
pio device monitor -b 115200
```

Default ESP32 SPI pin map (override in `platformio.ini`):

| Signal | GPIO |
| --- | ---: |
| CS | 5 |
| DIO0 / IRQ | 26 |
| RST | 14 |
| DIO1 / BUSY | 33 |
| SCK | 18 |
| MISO | 19 |
| MOSI | 23 |

## Run host tests

```bash
cd ch14-esp32-lora
PYTHONPATH=. python -m unittest discover -s tests -v
```

## Host tools

```bash
python tools/build_packet.py encode --seq 1 --name ping --lat 0 --lon 0
python tools/duty_cycle_cap.py --percent 10 --airtime-ms 50 --packets 100
python tools/validate_rssi_log.py data/sample_rssi_log.json
```

Never commit TTN keys, private GPS tracks or secrets. Teaching lat/lon in the
firmware ping are placeholders (0,0), not a real fix.
