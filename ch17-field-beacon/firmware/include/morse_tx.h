#pragma once

#include <stddef.h>
#include <stdint.h>

// Non-blocking Morse sidetone player on TONE_PIN. Practice / local audio only
// unless a separate legal RF path is explicitly enabled by the reader.

typedef struct {
  uint8_t tone_pin;
  uint16_t wpm;
  uint32_t dit_ms;
  const char *text;
  size_t index;
  const char *pattern;
  size_t pattern_index;
  uint32_t next_ms;
  bool tone_on;
  bool active;
  bool between_chars;
  bool between_words;
} MorseTx;

void morse_tx_init(MorseTx *tx, uint8_t tone_pin, uint16_t wpm);
bool morse_tx_start(MorseTx *tx, const char *text);
bool morse_tx_busy(const MorseTx *tx);
void morse_tx_poll(MorseTx *tx, uint32_t now_ms);
void morse_tx_stop(MorseTx *tx);
