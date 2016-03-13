import unittest
from aviation_weather import Wind
from aviation_weather.exceptions import WindDecodeException


class TestWind(unittest.TestCase):
    """Unit tests for aviation_weather.components.wind.Wind"""

    def _test_valid(self, raw, direction, speed, gusts, variable):
        w = Wind(raw)
        self.assertEqual(raw, str(w))
        self.assertEqual(w.direction, direction)
        self.assertEqual(w.speed, speed)
        self.assertEqual(w.gusts, gusts)
        self.assertEqual(w.variable, variable)

    def test_valid_simpleKT(self):
        self._test_valid("35007KT", 350, 7, None, None)

    def test_valid_simpleMPS(self):
        self._test_valid("21007MPS", 210, 7, None, None)

    def test_valid_strong_winds(self):
        self._test_valid("350107KT", 350, 107, None, None)

    def test_valid_gusts(self):
        self._test_valid("32013G17KT", 320, 13, 17, None)

    def test_valid_strong_gusts(self):
        self._test_valid("05013G127KT", 50, 13, 127, None)

    def test_valid_variable_weak(self):
        self._test_valid("VRB01MPS", "VRB", 1, None, None)

    def test_valid_variable_strong(self):
        self._test_valid("14003KT 110V170", 140, 3, None, (110, 170))

    def _test_invalid(self, raw):
        with self.assertRaises(WindDecodeException):
            Wind(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_short(self):
        self._test_invalid("1012KT")

    def test_invalid_long(self):
        self._test_invalid("3210123KT")

    def test_invalid_bad_unit(self):
        self._test_invalid("21012KN")

    def test_invalid_strength(self):
        self._test_invalid("VRBMPS")

    def test_invalid_no_unit(self):
        self._test_invalid("21012G21")


if __name__ == "__main__":
    unittest.main()
