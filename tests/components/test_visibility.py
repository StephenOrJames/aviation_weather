import unittest
from aviation_weather import Visibility
from aviation_weather.exceptions import VisibilityDecodeError


class TestVisibility(unittest.TestCase):
    """Unit tests for aviation_weather.components.visibility.Visibility"""

    def _test_valid(self, raw, is_less_than, distance, unit):
        v = Visibility(raw)
        self.assertEqual(raw, v.raw)
        self.assertEqual(is_less_than, v.is_less_than)
        self.assertEqual(distance, v.distance)
        self.assertEqual(unit, v.unit)

    def test_valid_1_SM(self):
        self._test_valid("1SM", False, 1, "SM")

    def test_valid_20_SM(self):
        self._test_valid("20SM", False, 20, "SM")

    def test_valid_fraction_SM(self):
        self._test_valid("1/2SM", False, .5, "SM")

    def test_valid_less_fraction_SM(self):
        self._test_valid("M1/2SM", True, .5, "SM")

    def test_valid_less_mixed_SM(self):
        self._test_valid("M1 1/4SM", True, 1.25, "SM")

    def test_valid_9999_m(self):
        self._test_valid("9999", False, 9999, "m")

    def test_valid_2000_m(self):
        self._test_valid("2000", False, 2000, "m")

    def _test_invalid(self, raw):
        with self.assertRaises(VisibilityDecodeError):
            Visibility(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_no_value(self):
        self._test_invalid("MSM")

    def test_invalid_short(self):
        self._test_invalid("120")

    def test_invalid_long(self):
        self._test_invalid("12345")

    def test_invalid_long_SM(self):
        self._test_invalid("123456SM")


if __name__ == "__main__":
    unittest.main()
