import unittest
from aviation_weather import WeatherGroup
from aviation_weather.exceptions import WeatherGroupDecodeException


class TestWeatherGroup(unittest.TestCase):
    """Unit tests for aviation_weather.components.weathergroup.WeatherGroup"""

    def test_valid(self):
        """Test valid weather groups"""

        tests = [
            "BR",
            "+SN",
            "FZFG",
            "VCTS",
            "-RA",
            "-RASN"
        ]
        for test in tests:
            self.assertEqual(test, str(WeatherGroup(test)))

    def test_invalid(self):
        """Test invalid weather groups"""

        tests = [
            "",  # Empty
            "+AA",  # Invalid descriptor/phenomenon
            "VCBIRD"  # Invalid descriptor/phenomenon
        ]
        for test in tests:
            with self.assertRaises(WeatherGroupDecodeException):
                WeatherGroup(test)


if __name__ == "__main__":
    unittest.main()
