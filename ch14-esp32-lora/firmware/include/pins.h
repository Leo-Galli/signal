#pragma once

// Default ESP32 <-> LoRa module SPI pin map used by the stock envs.
// Override with -DCS_PIN=... etc. in platformio.ini for your breakout.

#ifndef CS_PIN
#define CS_PIN 5
#endif
#ifndef DIO0_PIN
#define DIO0_PIN 26
#endif
#ifndef RST_PIN
#define RST_PIN 14
#endif
#ifndef DIO1_PIN
#define DIO1_PIN 33
#endif

// HSPI defaults on ESP32 Arduino core (SCK/MISO/MOSI). Documented for wiring.
#ifndef LORA_SCK
#define LORA_SCK 18
#endif
#ifndef LORA_MISO
#define LORA_MISO 19
#endif
#ifndef LORA_MOSI
#define LORA_MOSI 23
#endif
