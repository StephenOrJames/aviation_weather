import unittest
from aviation_weather import Pressure
from aviation_weather.exceptions import PressureDecodeError


class TestPressure(unittest.TestCase):
    """Unit tests for aviation_weather.components.pressure.Pressure"""

    def _test_valid(self, raw, indicator, value, is_slp):
        p = Pressure(raw)
        self.assertEqual(raw, p.raw)
        self.assertEqual(indicator, p.indicator)
        self.assertEqual(value, p.value)
        self.assertEqual(is_slp, p.is_slp)

    def test_valid_altimeter(self):
        self._test_valid("A2992", "A", 29.92, False)

    def test_valid_QNH(self):
        self._test_valid("Q1013", "Q", 1013, False)

    def test_valid_SLPNO(self):
        self._test_valid("SLPNO", "Q", None, True)

    def test_valid_SLP1(self):
        self._test_valid("SLP138", "Q", 1013.8, True)

    def test_valid_SLP2(self):
        self._test_valid("SLP237", "Q", 1023.7, True)

    def test_valid_SLP9(self):
        self._test_valid("SLP933", "Q", 993.3, True)

    def test_invalid(self):
        with self.assertRaises(PressureDecodeError):
            Pressure("3000")  # no unit indicator; more likely visibility
