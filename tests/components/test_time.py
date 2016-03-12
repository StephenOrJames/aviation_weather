import unittest
from aviation_weather import Time
from aviation_weather.exceptions import TimeDecodeException


class TestTime(unittest.TestCase):
    """Unit tests for aviation_weather.components.time.Time"""

    def test_valid(self):
        """Test valid times"""

        time_str = "161851Z"
        time_obj = Time(time_str)
        self.assertEqual(time_str, str(time_obj))
        self.assertEqual(time_obj.day, 16)
        self.assertEqual(time_obj.hour, 18)
        self.assertEqual(time_obj.minute, 51)
        self.assertEqual(time_obj.timezone, "Z")

    def test_invalid(self):
        """Test invalid times"""

        with self.assertRaises(TimeDecodeException):
            Time("")  # Empty
        with self.assertRaises(TimeDecodeException):
            Time("ABCDEFZ")  # Definitely not a time
        with self.assertRaises(TimeDecodeException):
            Time("1851Z")  # Where's the date


if __name__ == "__main__":
    unittest.main()
