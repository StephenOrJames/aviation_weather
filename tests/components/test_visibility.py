import unittest
from aviation_weather import Visibility
from aviation_weather.exceptions import VisibilityDecodeError


class TestVisibility(unittest.TestCase):
    """Unit tests for aviation_weather.components.visibility.Visibility"""

    def _test_valid(self, raw, less_than, greater_than, distance, unit):
        v = Visibility(raw)
        self.assertEqual(raw, v.raw)
        self.assertEqual(less_than, v.less_than)
        self.assertEqual(greater_than, v.greater_than)
        self.assertEqual(distance, v.distance)
        self.assertEqual(unit, v.unit)

    def test_valid_1_SM(self):
        self._test_valid("1SM", False, False, 1, "SM")

    def test_valid_20_SM(self):
        self._test_valid("20SM", False, False, 20, "SM")

    def test_valid_fraction_SM(self):
        self._test_valid("1/2SM", False, False, .5, "SM")

    def test_valid_less_fraction_SM(self):
        self._test_valid("M1/2SM", True, False, .5, "SM")

    def test_valid_less_mixed_SM(self):
        self._test_valid("M1 1/4SM", True, False, 1.25, "SM")

    def test_valid_greater_SM(self):
        self._test_valid("P6SM", False, True, 6, "SM")

    def test_valid_9999_m(self):
        self._test_valid("9999", False, False, 9999, "m")

    def test_valid_2000_m(self):
        self._test_valid("2000", False, False, 2000, "m")

    def _test_invalid(self, raw):
        with self.assertRaises(VisibilityDecodeError):
            Visibility(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_no_value(self):
        self._test_invalid("SM")

    def test_invalid_no_value_lt(self):
        self._test_invalid("MSM")

    def test_invalid_no_value_gt(self):
        self._test_invalid("PSM")

    def test_invalid_short(self):
        self._test_invalid("120")

    def test_invalid_long(self):
        self._test_invalid("12345")

    def test_invalid_long_SM(self):
        self._test_invalid("123456SM")


if __name__ == "__main__":
    unittest.main()
