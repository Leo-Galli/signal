#pragma once

#include <stddef.h>

// Look up an element pattern ('.' and '-') for a single A-Z / 0-9 character.
// Returns nullptr if unknown.
const char *morse_pattern(char symbol);

// Decode a null-terminated pattern of '.' and '-' into a character.
// Returns '?' if unknown. Prosigns are not expanded on the MCU (host can).
char morse_decode_pattern(const char *pattern);
