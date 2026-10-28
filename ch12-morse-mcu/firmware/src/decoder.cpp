#include "decoder.h"

#include "alphabet.h"
#include "timing.h"

#include <string.h>

static const size_t kMaxElements = 8;

static uint8_t g_wpm = 20;
static uint16_t g_unit_ms = 60;
static decoder_char_fn g_on_char = nullptr;

static bool g_have_edge = false;
static bool g_last_down = false;
static uint32_t g_last_ms = 0;
static uint16_t g_last_dit_ms = 60;

static char g_pattern[kMaxElements + 1];
static size_t g_pattern_len = 0;
static bool g_char_open = false;
static bool g_word_space_pending = false;

static void reset_pattern(void) {
  g_pattern_len = 0;
  g_pattern[0] = '\0';
  g_char_open = false;
}

static void emit_char(char c) {
  if (g_on_char != nullptr) {
    g_on_char(c);
  }
}

static void flush_character(void) {
  if (!g_char_open || g_pattern_len == 0) {
    reset_pattern();
    return;
  }
  g_pattern[g_pattern_len] = '\0';
  emit_char(morse_decode_pattern(g_pattern));
  reset_pattern();
}

void decoder_begin(uint8_t wpm, decoder_char_fn on_char) {
  g_on_char = on_char;
  decoder_set_wpm(wpm);
  g_have_edge = false;
  g_last_down = false;
  g_last_ms = 0;
  g_last_dit_ms = g_unit_ms;
  g_word_space_pending = false;
  reset_pattern();
}

void decoder_set_wpm(uint8_t wpm) {
  g_wpm = clamp_wpm(wpm);
  g_unit_ms = unit_ms_from_wpm(g_wpm);
}

void decoder_on_edge(bool key_down, uint32_t now_ms) {
  if (!g_have_edge) {
    g_have_edge = true;
    g_last_down = key_down;
    g_last_ms = now_ms;
    return;
  }

  const uint32_t dt = now_ms - g_last_ms;
  g_last_ms = now_ms;

  if (g_last_down) {
    // Mark just ended: classify dit vs dah.
    const uint16_t dah_threshold = static_cast<uint16_t>(g_unit_ms * 2U);
    char mark = '.';
    if (dt >= dah_threshold) {
      mark = '-';
    } else {
      g_last_dit_ms = static_cast<uint16_t>(dt > 0 ? dt : 1);
    }
    if (g_pattern_len < kMaxElements) {
      g_pattern[g_pattern_len++] = mark;
      g_pattern[g_pattern_len] = '\0';
      g_char_open = true;
    }
    g_word_space_pending = false;
  } else {
    // Space just ended: maybe close character or word.
    const uint16_t char_gap = static_cast<uint16_t>(g_unit_ms * 2U);
    const uint16_t word_gap = static_cast<uint16_t>(g_unit_ms * 5U);
    if (dt >= word_gap) {
      flush_character();
      emit_char(' ');
      g_word_space_pending = false;
    } else if (dt >= char_gap) {
      flush_character();
      g_word_space_pending = true;
    }
  }

  g_last_down = key_down;
}

void decoder_poll_idle(uint32_t now_ms) {
  if (!g_have_edge || g_last_down || !g_char_open) {
    return;
  }
  const uint32_t dt = now_ms - g_last_ms;
  const uint16_t char_gap = static_cast<uint16_t>(g_unit_ms * 2U);
  const uint16_t word_gap = static_cast<uint16_t>(g_unit_ms * 5U);
  if (dt >= word_gap) {
    flush_character();
    if (!g_word_space_pending) {
      emit_char(' ');
    }
    g_word_space_pending = false;
    g_last_ms = now_ms;
    return;
  }
  if (dt >= char_gap) {
    flush_character();
    g_word_space_pending = true;
  }
}

uint16_t decoder_last_dit_ms(void) { return g_last_dit_ms; }
