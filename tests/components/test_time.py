import unittest
from aviation_weather import Time
from aviation_weather.exceptions import TimeDecodeException


class TestTime(unittest.TestCase):
    """Unit tests for aviation_weather.components.time.Time"""

    def test_valid(self):
        time_str = "161851Z"
        time_obj = Time(time_str)
        self.assertEqual(time_str, str(time_obj))
        self.assertEqual(time_obj.day, 16)
        self.assertEqual(time_obj.hour, 18)
        self.assertEqual(time_obj.minute, 51)
        self.assertEqual(time_obj.timezone, "Z")

    def invalid_tests(self, raw):
        with self.assertRaises(TimeDecodeException):
            Time(raw)

    def test_invalid_empty(self):
        self.invalid_tests("")

    def test_invalid_letters(self):
        self.invalid_tests("ABCDEFZ")

    def test_invalid_short(self):
        self.invalid_tests("1851Z")

    def test_invalid_long(self):
        self.invalid_tests("02101851Z")

    def test_invalid_unit(self):
        self.invalid_tests("101851A")

    def test_invalid_day(self):
        self.invalid_tests("321456Z")

    def test_invalid_hour(self):
        self.invalid_tests("092507Z")

    def test_invalid_minute(self):
        self.invalid_tests("122384Z")


if __name__ == "__main__":
    unittest.main()
