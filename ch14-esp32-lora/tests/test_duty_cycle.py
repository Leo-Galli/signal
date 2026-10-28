import unittest

from lora.duty_cycle import DutyCycleGate, budget_ms


class TestDutyCycle(unittest.TestCase):
    def test_budget_10_percent_hour(self) -> None:
        self.assertEqual(budget_ms(3_600_000, 10.0), 360_000)

    def test_gate_blocks_when_exhausted(self) -> None:
        gate = DutyCycleGate(10.0, window_ms=1000)
        self.assertTrue(gate.allow(0, 50))
        gate.record(0, 50)
        # budget = 100 ms; 50 used -> 50 left
        self.assertTrue(gate.allow(10, 50))
        gate.record(10, 50)
        self.assertFalse(gate.allow(20, 1))

    def test_window_rolls(self) -> None:
        gate = DutyCycleGate(10.0, window_ms=1000)
        gate.record(0, 100)
        self.assertEqual(gate.remaining_ms(0), 0)
        self.assertEqual(gate.remaining_ms(1000), 100)


if __name__ == "__main__":
    unittest.main()
