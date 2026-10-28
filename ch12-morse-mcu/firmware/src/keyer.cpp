#include "keyer.h"

#include <Arduino.h>

static uint8_t g_tone_pin = 0;
static uint16_t g_tone_hz = 700;
static bool g_on = false;

void keyer_begin(uint8_t tone_pin, uint16_t tone_hz) {
  g_tone_pin = tone_pin;
  g_tone_hz = tone_hz == 0 ? 700 : tone_hz;
  g_on = false;
  pinMode(g_tone_pin, OUTPUT);
  digitalWrite(g_tone_pin, LOW);
  noTone(g_tone_pin);
}

void keyer_set_tone_hz(uint16_t tone_hz) {
  if (tone_hz == 0) {
    return;
  }
  g_tone_hz = tone_hz;
  if (g_on) {
    tone(g_tone_pin, g_tone_hz);
  }
}

void keyer_update(bool key_down) {
  if (key_down && !g_on) {
    tone(g_tone_pin, g_tone_hz);
    g_on = true;
    return;
  }
  if (!key_down && g_on) {
    noTone(g_tone_pin);
    digitalWrite(g_tone_pin, LOW);
    g_on = false;
  }
}

bool keyer_tone_on(void) { return g_on; }
