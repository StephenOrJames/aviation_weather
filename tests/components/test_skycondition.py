import unittest
from aviation_weather import SkyCondition
from aviation_weather.exceptions import SkyConditionDecodeException


class TestSkyCondition(unittest.TestCase):
    """Unit tests for aviation_weather.components.skycondition.SkyCondition"""

    def valid_tests(self, raw, type, height, cumulonimbus):
        s = SkyCondition(raw)
        self.assertEqual(str(s), raw)
        self.assertEqual(s.type, type)
        self.assertEqual(s.height, height)
        self.assertEqual(s.cumulonimbus, cumulonimbus)

    def test_valid_clr(self):
        self.valid_tests("CLR", "CLR", None, False)

    def test_valid_skc(self):
        self.valid_tests("SKC", "SKC", None, False)

    def test_valid_ncd(self):
        self.valid_tests("NCD", "NCD", None, False)

    def test_valid_vv(self):
        self.valid_tests("VV004", "VV", 400, False)

    def test_valid_few(self):
        self.valid_tests("FEW012", "FEW", 1200, False)

    def test_valid_sct(self):
        self.valid_tests("SCT024", "SCT", 2400, False)

    def test_valid_bkn(self):
        self.valid_tests("BKN048", "BKN", 4800, False)

    def test_valid_ovc(self):
        self.valid_tests("OVC120", "OVC", 12000, False)

    def test_valid_cb(self):
        self.valid_tests("OVC015CB", "OVC", 1500, True)

    def invalid_tests(self, raw):
        with self.assertRaises(SkyConditionDecodeException):
            SkyCondition(raw)

    def test_invalid_empty(self):
        self.invalid_tests("")

    def test_invalid_short(self):
        self.invalid_tests("FEW12")

    def test_invalid_type(self):
        self.invalid_tests("RED220")

    def test_invalid_height(self):
        self.invalid_tests("SCTCLD")


if __name__ == "__main__":
    unittest.main()
