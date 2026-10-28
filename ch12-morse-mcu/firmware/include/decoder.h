#pragma once

#include <stdint.h>

typedef void (*decoder_char_fn)(char c);

// Decode mark/space durations from a straight key into characters.
// Call decoder_begin once, then decoder_on_edge on each key edge with millis().
void decoder_begin(uint8_t wpm, decoder_char_fn on_char);
void decoder_set_wpm(uint8_t wpm);
void decoder_on_edge(bool key_down, uint32_t now_ms);
void decoder_poll_idle(uint32_t now_ms);
uint16_t decoder_last_dit_ms(void);
