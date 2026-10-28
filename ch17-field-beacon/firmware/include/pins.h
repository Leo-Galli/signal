#pragma once

// Default ESP32 pin map for the teaching beacon. Override in platformio.ini.

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

#ifndef LORA_SCK
#define LORA_SCK 18
#endif
#ifndef LORA_MISO
#define LORA_MISO 19
#endif
#ifndef LORA_MOSI
#define LORA_MOSI 23
#endif

#ifndef GPS_RX_PIN
#define GPS_RX_PIN 16
#endif
#ifndef GPS_TX_PIN
#define GPS_TX_PIN 17
#endif

#ifndef TONE_PIN
#define TONE_PIN 25
#endif

#ifndef BTN_SOS_PIN
#define BTN_SOS_PIN 32
#endif
#ifndef BTN_SEND_PIN
#define BTN_SEND_PIN 27
#endif
#ifndef BTN_MORSE_PIN
#define BTN_MORSE_PIN 12
#endif
#ifndef BTN_DRY_PIN
#define BTN_DRY_PIN 13
#endif
