import unittest
from aviation_weather import Visibility
from aviation_weather.exceptions import VisibilityDecodeException


class TestVisibility(unittest.TestCase):
    """Unit tests for aviation_weather.components.visibility.Visibility"""

    def _valid_tests(self, raw, is_less_than, distance, unit):
        v = Visibility(raw)
        self.assertEqual(str(v), raw)
        self.assertEqual(v.is_less_than, is_less_than)
        self.assertEqual(v.distance, distance)
        self.assertEqual(v.unit, unit)

    def test_valid_1_SM(self):
        self._valid_tests("1SM", False, 1, "SM")

    def test_valid_20_SM(self):
        self._valid_tests("20SM", False, 20, "SM")

    def test_valid_fraction_SM(self):
        self._valid_tests("1/2SM", False, .5, "SM")

    def test_valid_less_fraction_SM(self):
        self._valid_tests("M1/2SM", True, .5, "SM")

    def test_valid_less_mixed_SM(self):
        self._valid_tests("M1 1/4SM", True, 1.25, "SM")

    def test_valid_9999_m(self):
        self._valid_tests("9999", False, 9999, "m")

    def test_valid_2000_m(self):
        self._valid_tests("2000", False, 2000, "m")

    def _invalid_tests(self, raw):
        with self.assertRaises(VisibilityDecodeException):
            Visibility(raw)

    def test_invalid_empty(self):
        self._invalid_tests("")

    def test_invalid_no_value(self):
        self._invalid_tests("MSM")

    def test_invalid_short(self):
        self._invalid_tests("120")

    def test_invalid_long(self):
        self._invalid_tests("12345")

    def test_invalid_long_SM(self):
        self._invalid_tests("123456SM")


if __name__ == "__main__":
    unittest.main()
