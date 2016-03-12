import unittest
from aviation_weather import Temperature
from aviation_weather.exceptions import TemperatureDecodeException


class TestTemperature(unittest.TestCase):
    """Unit tests for aviation_weather.components.temperature.Temperature"""

    def test_valid(self):
        """Test valid temperatures"""

        s = "21/12"
        o = Temperature(s)
        self.assertEqual(s, str(o))
        self.assertEqual(o.temperature, 21)
        self.assertEqual(o.dew_point, 12)

        s = "21/M12"
        o = Temperature(s)
        self.assertEqual(s, str(o))
        self.assertEqual(o.temperature, 21)
        self.assertEqual(o.dew_point, -12)

        s = "M01/M04"
        o = Temperature(s)
        self.assertEqual(s, str(o))
        self.assertEqual(o.temperature, -1)
        self.assertEqual(o.dew_point, -4)

    def test_invalid(self):
        """Test invalid temperatures"""

        tests = [
            "M/M",
            "1200",
            "////"
        ]
        for test in tests:
            with self.assertRaises(TemperatureDecodeException):
                Temperature(test)


if __name__ == "__main__":
    unittest.main()
