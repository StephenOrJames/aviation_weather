import unittest
from aviation_weather import Pressure
from aviation_weather.exceptions import PressureDecodeException


class TestPressure(unittest.TestCase):
    """Unit tests for aviation_weather.components.pressure.Pressure"""

    def valid_tests(self, raw, indicator, value):
        p = Pressure(raw)
        self.assertEqual(str(p), raw)
        self.assertEqual(p.indicator, indicator)
        self.assertEqual(p.value, value)

    def test_valid_altimeter(self):
        self.valid_tests("A2992", "A", 29.92)

    def test_valid_QNH(self):
        self.valid_tests("Q1013", "Q", 1013)

    def test_invalid(self):
        with self.assertRaises(PressureDecodeException):
            Pressure("3000")  # no unit indicator; more likely visibility


if __name__ == "__main__":
    unittest.main()
