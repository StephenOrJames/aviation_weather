import unittest
from aviation_weather import SkyCondition
from aviation_weather.exceptions import SkyConditionDecodeException


class TestSkyCondition(unittest.TestCase):
    """Unit tests for aviation_weather.components.skycondition.SkyCondition"""

    def _valid_tests(self, raw, type_, height, cumulonimbus):
        s = SkyCondition(raw)
        self.assertEqual(str(s), raw)
        self.assertEqual(s.type, type_)
        self.assertEqual(s.height, height)
        self.assertEqual(s.cumulonimbus, cumulonimbus)

    def test_valid_clr(self):
        self._valid_tests("CLR", "CLR", None, False)

    def test_valid_skc(self):
        self._valid_tests("SKC", "SKC", None, False)

    def test_valid_ncd(self):
        self._valid_tests("NCD", "NCD", None, False)

    def test_valid_vv(self):
        self._valid_tests("VV004", "VV", 400, False)

    def test_valid_few(self):
        self._valid_tests("FEW012", "FEW", 1200, False)

    def test_valid_sct(self):
        self._valid_tests("SCT024", "SCT", 2400, False)

    def test_valid_bkn(self):
        self._valid_tests("BKN048", "BKN", 4800, False)

    def test_valid_ovc(self):
        self._valid_tests("OVC120", "OVC", 12000, False)

    def test_valid_cb(self):
        self._valid_tests("OVC015CB", "OVC", 1500, True)

    def _invalid_tests(self, raw):
        with self.assertRaises(SkyConditionDecodeException):
            SkyCondition(raw)

    def test_invalid_empty(self):
        self._invalid_tests("")

    def test_invalid_short(self):
        self._invalid_tests("FEW12")

    def test_invalid_type(self):
        self._invalid_tests("RED220")

    def test_invalid_height(self):
        self._invalid_tests("SCTCLD")


if __name__ == "__main__":
    unittest.main()
