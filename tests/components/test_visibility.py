import unittest
from aviation_weather import Visibility
from aviation_weather.exceptions import VisibilityDecodeException


class TestVisibility(unittest.TestCase):
    """Unit tests for aviation_weather.components.visibility.Visibility"""

    def test_valid(self):
        """Test valid visibilities"""

        tests = [
            "1SM",
            "20SM",
            "1/2SM",
            "M1/2SM",
            "M1 1/4SM",
            "9999",
            "2000",
        ]
        for test in tests:
            self.assertEqual(test, str(Visibility(test)))

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
