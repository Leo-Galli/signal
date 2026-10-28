# BOM -- ch14-esp32-lora

Two-node point-to-point LoRa ping (reader picks one module family for both ends).

| Qty | Item | Notes |
| ---: | --- | --- |
| 2 | ESP32 DevKit | Same class as Chapter 12 |
| 2 | LoRa module | SX1276/78 breakout, SX1262 breakout, **or** E22-400M30S class -- document which |
| 2 | Antenna matched to band | 433 MHz (EU teaching default) or your worksheet band |
| 2 | USB cable | Power + serial |
| 2 | Breadboard + jumpers | Or PCB / Dupont wiring |
| 1 | Host computer | PlatformIO + serial monitors |

Optional: multimeter from Chapter 2 checklist; notebook for RSSI log.

Fail-safe firmware defaults: `LORA_TX_DBM=2`, `DUTY_CYCLE_PERCENT=10`, SF7 / 125 kHz. Module maximum power can exceed EU SRD e.r.p. planning highlights -- never confuse module capability with a legal limit. Not legal advice.
