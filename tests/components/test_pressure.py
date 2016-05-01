import unittest
from aviation_weather import Pressure
from aviation_weather.exceptions import PressureDecodeError


class TestPressure(unittest.TestCase):
    """Unit tests for aviation_weather.components.pressure.Pressure"""

    def _test_valid(self, raw, indicator, value):
        p = Pressure(raw)
        self.assertEqual(raw, p.raw)
        self.assertEqual(indicator, p.indicator)
        self.assertEqual(value, p.value)

    def test_valid_altimeter(self):
        self._test_valid("A2992", "A", 29.92)

    def test_valid_QNH(self):
        self._test_valid("Q1013", "Q", 1013)

    def test_invalid(self):
        with self.assertRaises(PressureDecodeError):
            Pressure("3000")  # no unit indicator; more likely visibility


if __name__ == "__main__":
    unittest.main()
