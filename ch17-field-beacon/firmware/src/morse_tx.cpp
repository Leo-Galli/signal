#include "morse_tx.h"

#include "alphabet.h"

#include <Arduino.h>
#include <string.h>

static uint32_t dit_ms_from_wpm(uint16_t wpm) {
  if (wpm < 5) {
    wpm = 5;
  }
  if (wpm > 40) {
    wpm = 40;
  }
  return 1200UL / static_cast<uint32_t>(wpm);
}

void morse_tx_init(MorseTx *tx, uint8_t tone_pin, uint16_t wpm) {
  if (tx == nullptr) {
    return;
  }
  memset(tx, 0, sizeof(*tx));
  tx->tone_pin = tone_pin;
  tx->wpm = wpm;
  tx->dit_ms = dit_ms_from_wpm(wpm);
  pinMode(tone_pin, OUTPUT);
  noTone(tone_pin);
}

void morse_tx_stop(MorseTx *tx) {
  if (tx == nullptr) {
    return;
  }
  noTone(tx->tone_pin);
  tx->tone_on = false;
  tx->active = false;
  tx->text = nullptr;
  tx->pattern = nullptr;
}

bool morse_tx_busy(const MorseTx *tx) {
  return tx != nullptr && tx->active;
}

bool morse_tx_start(MorseTx *tx, const char *text) {
  if (tx == nullptr || text == nullptr || text[0] == '\0') {
    return false;
  }
  morse_tx_stop(tx);
  tx->text = text;
  tx->index = 0;
  tx->pattern = nullptr;
  tx->pattern_index = 0;
  tx->between_chars = false;
  tx->between_words = false;
  tx->next_ms = millis();
  tx->active = true;
  return true;
}

static void tone_on(MorseTx *tx) {
  tone(tx->tone_pin, 600);
  tx->tone_on = true;
}

static void tone_off(MorseTx *tx) {
  noTone(tx->tone_pin);
  tx->tone_on = false;
}

void morse_tx_poll(MorseTx *tx, uint32_t now_ms) {
  if (tx == nullptr || !tx->active) {
    return;
  }
  if (now_ms < tx->next_ms) {
    return;
  }

  if (tx->between_words) {
    tx->between_words = false;
    tx->next_ms = now_ms;
    return;
  }
  if (tx->between_chars) {
    tx->between_chars = false;
    tx->next_ms = now_ms;
    return;
  }

  if (tx->pattern != nullptr) {
    if (tx->tone_on) {
      tone_off(tx);
      tx->pattern_index++;
      if (tx->pattern[tx->pattern_index] == '\0') {
        tx->pattern = nullptr;
        tx->between_chars = true;
        tx->next_ms = now_ms + 3UL * tx->dit_ms;
      } else {
        tx->next_ms = now_ms + tx->dit_ms;
      }
      return;
    }

    const char mark = tx->pattern[tx->pattern_index];
    const uint32_t dur = (mark == '-') ? (3UL * tx->dit_ms) : tx->dit_ms;
    tone_on(tx);
    tx->next_ms = now_ms + dur;
    return;
  }

  // Advance to next character in text.
  while (tx->text[tx->index] != '\0') {
    const char ch = tx->text[tx->index++];
    if (ch == ' ') {
      tx->between_words = true;
      tx->next_ms = now_ms + 4UL * tx->dit_ms;  // plus prior char gap ~= 7 dits
      return;
    }
    const char *pat = morse_pattern(ch);
    if (pat == nullptr) {
      continue;
    }
    tx->pattern = pat;
    tx->pattern_index = 0;
    tx->next_ms = now_ms;
    return;
  }

  morse_tx_stop(tx);
}
