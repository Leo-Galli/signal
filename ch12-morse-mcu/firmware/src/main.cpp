#include <Arduino.h>

#include "alphabet.h"
#include "decoder.h"
#include "keyer.h"
#include "timing.h"

#ifndef KEY_PIN
#define KEY_PIN 15
#endif
#ifndef TONE_PIN
#define TONE_PIN 25
#endif
#ifndef POT_PIN
#define POT_PIN 34
#endif
#ifndef LED_PIN
#define LED_PIN 2
#endif

static const uint16_t kToneHz = 700;
static const uint32_t kPotSampleMs = 200;

static bool g_last_key = false;
static uint8_t g_wpm = 20;
static uint32_t g_last_pot_ms = 0;

static void on_decoded_char(char c) {
  Serial.write(static_cast<uint8_t>(c));
  if (c == ' ') {
    Serial.flush();
  }
}

static bool read_key_down(void) {
  // Active-low with internal pull-up: closed key pulls pin to GND.
  return digitalRead(KEY_PIN) == LOW;
}

static void refresh_wpm_from_pot(uint32_t now_ms) {
  if (now_ms - g_last_pot_ms < kPotSampleMs) {
    return;
  }
  g_last_pot_ms = now_ms;
#if defined(ARDUINO_ARCH_ESP32)
  const uint16_t raw = static_cast<uint16_t>(analogRead(POT_PIN));
  const uint16_t adc_max = 4095;
#else
  const uint16_t raw = static_cast<uint16_t>(analogRead(POT_PIN));
  const uint16_t adc_max = 1023;
#endif
  const uint8_t next = wpm_from_adc(raw, adc_max);
  if (next != g_wpm) {
    g_wpm = next;
    decoder_set_wpm(g_wpm);
    Serial.print(F("\n# WPM "));
    Serial.println(g_wpm);
  }
}

void setup() {
  pinMode(KEY_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200);
  delay(200);
  Serial.println();
  Serial.println(F("# Signal ch12-morse-mcu"));
  Serial.println(F("# PRACTICE OSCILLATOR ONLY -- no RF in this firmware"));
  Serial.println(F("# Not legal advice. Key closed = active-low on KEY_PIN."));
  Serial.print(F("# KEY_PIN="));
  Serial.print(KEY_PIN);
  Serial.print(F(" TONE_PIN="));
  Serial.print(TONE_PIN);
  Serial.print(F(" POT_PIN="));
  Serial.println(POT_PIN);

  keyer_begin(TONE_PIN, kToneHz);
  decoder_begin(g_wpm, on_decoded_char);
  g_last_key = read_key_down();
  Serial.print(F("# WPM "));
  Serial.println(g_wpm);
  Serial.println(F("# Ready. Close the key for sidetone; decoded text follows."));
}

void loop() {
  const uint32_t now = millis();
  const bool key_down = read_key_down();

  keyer_update(key_down);
  digitalWrite(LED_PIN, key_down ? HIGH : LOW);

  if (key_down != g_last_key) {
    decoder_on_edge(key_down, now);
    g_last_key = key_down;
  }
  decoder_poll_idle(now);
  refresh_wpm_from_pot(now);
}
