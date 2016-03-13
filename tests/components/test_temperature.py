import unittest
from aviation_weather import Temperature
from aviation_weather.exceptions import TemperatureDecodeError


class TestTemperature(unittest.TestCase):
    """Unit tests for aviation_weather.components.temperature.Temperature"""

    def _test_valid(self, raw, temperature, dew_point):
        t = Temperature(raw)
        self.assertEqual(str(t), raw)
        self.assertEqual(t.temperature, temperature)
        self.assertEqual(t.dew_point, dew_point)

    def test_valid_positive_positive(self):
        self._test_valid("21/12", 21, 12)

    def test_valid_positive_negative(self):
        self._test_valid("21/M12", 21, -12)

    def test_valid_negative_negative(self):
        self._test_valid("M01/M04", -1, -4)

    def _test_invalid(self, raw):
        with self.assertRaises(TemperatureDecodeError):
            Temperature(raw)

    def test_invalid_no_numbers(self):
        self._test_invalid("M/M")

    def test_invalid_no_separator(self):
        self._test_invalid("1200")

    def test_invalid_slashes(self):
        self._test_invalid("////")


if __name__ == "__main__":
    unittest.main()
