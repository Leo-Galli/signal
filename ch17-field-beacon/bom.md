# Bill of materials -- ch17-field-beacon

Teaching build. Substitute equivalents that match your pin map and band.

| Item | Qty | Notes |
| --- | ---: | --- |
| ESP32 DevKit | 1 | Arduino-core / PlatformIO `esp32dev` |
| LoRa module | 1 | SX1276/78 breakout, SX1262, or E22-400M30S class |
| Antenna | 1 | Matched to programmed band; attach before any live TX |
| GPS module (UART NMEA) | 1 | 9600 baud typical; TX -> ESP32 GPS_RX (GPIO16 default) |
| SSD1306 OLED (optional) | 1 | Status mirrors to serial by default; OLED is optional wiring |
| Momentary buttons | 4 | SOS arm, SEND, MORSE, DRY (active-low pull-ups) |
| Piezo / buzzer or headphone amp | 1 | Morse sidetone on TONE_PIN (GPIO25 default) |
| Li-ion cell + charger / USB power bank | 1 | Follow Chapter 2 power and fuse practice |
| Enclosure | 1 | Field-capable; strain-relieve antenna and USB |
| Breadboard / proto + jumpers | 1 | Bench bring-up before enclosure |

Never commit private GPS tracks, callsign credentials or secrets.
