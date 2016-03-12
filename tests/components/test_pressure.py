import unittest
from aviation_weather import Pressure
from aviation_weather.exceptions import PressureDecodeException


class TestPressure(unittest.TestCase):
    """Unit tests for aviation_weather.components.pressure.Pressure"""

    def test_valid(self):
        """Test valid pressures"""

        p = Pressure("A2992")
        self.assertEqual(str(p), "A2992")
        self.assertEqual(p.indicator, "A")
        self.assertEqual(p.value, 29.92)

        p = Pressure("Q1013")
        self.assertEqual(str(p), "Q1013")
        self.assertEqual(p.indicator, "Q")
        self.assertEqual(p.value, 1013)

    def test_invalid(self):
        """Test invalid pressures"""

        with self.assertRaises(PressureDecodeException):
            Pressure("3000")  # no unit indicator; more likely visibility


if __name__ == "__main__":
    unittest.main()
