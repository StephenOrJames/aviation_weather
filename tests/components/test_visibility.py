import unittest
from aviation_weather import Visibility
from aviation_weather.exceptions import VisibilityDecodeException


class TestVisibility(unittest.TestCase):
    """Unit tests for aviation_weather.components.visibility.Visibility"""

    def test_valid(self):
        """Test valid visibilities"""

        tests = [
            ("1SM", False, 1, "SM"),
            ("20SM", False, 20, "SM"),
            ("1/2SM", False, .5, "SM"),
            ("M1/2SM", True, .5, "SM"),
            ("M1 1/4SM", True, 1.25, "SM"),
            ("9999", False, 9999, "m"),
            ("2000", False, 2000, "m"),
        ]
        for test in tests:
            v = Visibility(test[0])
            self.assertEqual(test[0], str(v))
            self.assertEqual(test[1], v.is_less_than)
            self.assertEqual(test[2], v.distance)
            self.assertEqual(test[3], v.unit)

    def test_invalid(self):
        """Test invalid visibilities"""

        tests = [
            "",  # Empty
            "MSM",  # No value
            "120",  # Expect 4 digits if no unit specified
            "12345",  # Too long (no unit)
            "123456SM",  # Too long (SM)
        ]
        for test in tests:
            with self.assertRaises(VisibilityDecodeException):
                Visibility(test)


if __name__ == "__main__":
    unittest.main()
