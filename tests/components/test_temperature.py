import unittest
from aviation_weather import Temperature
from aviation_weather.exceptions import TemperatureDecodeException


class TestTemperature(unittest.TestCase):
    """Unit tests for aviation_weather.components.temperature.Temperature"""

    def test_valid(self):
        """Test valid temperatures"""

        tests = [
            "21/12",
            "21/M12",
            "M01/M04",
        ]
        for test in tests:
            self.assertEqual(test, str(Temperature(test)))

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
