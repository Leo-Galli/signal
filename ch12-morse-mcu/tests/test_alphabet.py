import unittest

from keyer.alphabet import decode_pattern, encode_symbol, known_characters


class AlphabetTests(unittest.TestCase):
    def test_known_count(self) -> None:
        self.assertEqual(len(known_characters()), 36)

    def test_round_trip_letters(self) -> None:
        for symbol in "PARIS":
            pattern = encode_symbol(symbol)
            self.assertEqual(decode_pattern(pattern), symbol)

    def test_unknown_pattern(self) -> None:
        self.assertEqual(decode_pattern(".-.-.-.-"), "?")

    def test_unknown_symbol_raises(self) -> None:
        with self.assertRaises(KeyError):
            encode_symbol("@")


if __name__ == "__main__":
    unittest.main()
