import unittest
from aviation_weather import RunwayVisualRange
from aviation_weather.exceptions import RunwayVisualRangeDecodeError


class TestRunwayVisualRange(unittest.TestCase):
    """Unit tests for aviation_weather.components.runwayvisualrange.RunwayVisualRange"""

    def _test_valid(self, raw, runway, distance, unit, trend):
        r = RunwayVisualRange(raw)
        self.assertEqual(str(r), raw)
        self.assertEqual(r.runway, runway)
        self.assertEqual(r.distance, distance)
        self.assertEqual(r.unit, unit)
        self.assertEqual(r.trend, trend)

    def test_valid_1(self):
        self._test_valid("R12/2000", "12", "2000", "m", None)

    def test_valid_2(self):
        self._test_valid("R13C/M1000FT", "13C", "M1000", "FT", None)

    def test_valid_3(self):
        self._test_valid("R26L/P2000N", "26L", "P2000", "m", "N")

    def test_valid_4(self):
        self._test_valid("R08R/0800V2000U", "08R", ("0800", "2000"), "m", "U")

    def test_valid_5(self):
        self._test_valid("R09/1000VP6000FT", "09", ("1000", "P6000"), "FT", None)

    def _test_invalid(self, raw):
        with self.assertRaises(RunwayVisualRangeDecodeError):
            RunwayVisualRange(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_no_distance(self):
        self._test_invalid("R08C")

    def test_invalid_no_distance_with_slash(self):
        self._test_invalid("R09C/")

    def test_invalid_bad_distance(self):
        self._test_invalid("R10/M03")

    def test_invalid_varying(self):
        self._test_invalid("R11/M0600V")  # Is it varying? If so, to what? "V" isn't a valid unit or trend.

    def test_invalid_trend(self):
        self._test_invalid("R12L/2000V4000FTB")


if __name__ == "__main__":
    unittest.main()
