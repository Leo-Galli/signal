#include <stddef.h>
#include <string.h>

struct MorseEntry {
  char symbol;
  const char *pattern;
};

static const MorseEntry kTable[] = {
    {'A', ".-"},    {'B', "-..."},  {'C', "-.-."}, {'D', "-.."},
    {'E', "."},     {'F', "..-."},  {'G', "--."},  {'H', "...."},
    {'I', ".."},    {'J', ".---"},  {'K', "-.-"},  {'L', ".-.."},
    {'M', "--"},    {'N', "-."},    {'O', "---"},  {'P', ".--."},
    {'Q', "--.-"},  {'R', ".-."},   {'S', "..."},  {'T', "-"},
    {'U', "..-"},   {'V', "...-"},  {'W', ".--"},  {'X', "-..-"},
    {'Y', "-.--"},  {'Z', "--.."},  {'0', "-----"}, {'1', ".----"},
    {'2', "..---"}, {'3', "...--"}, {'4', "....-"}, {'5', "....."},
    {'6', "-...."}, {'7', "--..."}, {'8', "---.."}, {'9', "----."},
    {'.', ".-.-.-"},
};

const char *morse_pattern(char symbol) {
  if (symbol >= 'a' && symbol <= 'z') {
    symbol = static_cast<char>(symbol - 'a' + 'A');
  }
  for (size_t i = 0; i < sizeof(kTable) / sizeof(kTable[0]); ++i) {
    if (kTable[i].symbol == symbol) {
      return kTable[i].pattern;
    }
  }
  return nullptr;
}
