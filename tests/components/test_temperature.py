import unittest
from aviation_weather import Temperature
from aviation_weather.exceptions import TemperatureDecodeException


class TestTemperature(unittest.TestCase):
    """Unit tests for aviation_weather.components.temperature.Temperature"""

    def valid_tests(self, raw, temperature, dew_point):
        t = Temperature(raw)
        self.assertEqual(str(t), raw)
        self.assertEqual(t.temperature, temperature)
        self.assertEqual(t.dew_point, dew_point)

    def test_valid_positive_positive(self):
        self.valid_tests("21/12", 21, 12)

    def test_valid_positive_negative(self):
        self.valid_tests("21/M12", 21, -12)

    def test_valid_negative_negative(self):
        self.valid_tests("M01/M04", -1, -4)

    def invalid_tests(self, raw):
        with self.assertRaises(TemperatureDecodeException):
            Temperature(raw)

    def test_invalid_no_numbers(self):
        self.invalid_tests("M/M")

    def test_invalid_no_separator(self):
        self.invalid_tests("1200")

    def test_invalid_slashes(self):
        self.invalid_tests("////")


if __name__ == "__main__":
    unittest.main()
