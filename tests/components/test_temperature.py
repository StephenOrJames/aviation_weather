import unittest
from aviation_weather import Temperature
from aviation_weather.exceptions import TemperatureDecodeException


class TestTemperature(unittest.TestCase):
    """Unit tests for aviation_weather.components.temperature.Temperature"""

    def test_valid(self):
        """Test valid temperatures"""

        tests = [
            ("21/12", 21, 12),
            ("21/M12", 21, -12),
            ("M01/M04", -1, -4)
        ]
        for test in tests:
            t = Temperature(test[0])
            self.assertEqual(test[0], str(t))
            self.assertEqual(test[1], t.temperature)
            self.assertEqual(test[2], t.dew_point)

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
