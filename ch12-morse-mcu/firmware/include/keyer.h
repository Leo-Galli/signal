#pragma once

#include <stdint.h>

// Non-blocking straight-key sidetone keyer.
// key_down true means the contact is closed (active).
void keyer_begin(uint8_t tone_pin, uint16_t tone_hz);
void keyer_set_tone_hz(uint16_t tone_hz);
void keyer_update(bool key_down);
bool keyer_tone_on(void);
