import unittest
from aviation_weather import SkyCondition
from aviation_weather.exceptions import SkyConditionDecodeError


class TestSkyCondition(unittest.TestCase):
    """Unit tests for aviation_weather.components.skycondition.SkyCondition"""

    def _test_valid(self, raw, type_, height, cumulonimbus, towering_cumulus):
        s = SkyCondition(raw)
        self.assertEqual(raw, s.raw)
        self.assertEqual(type_, s.type)
        self.assertEqual(height, s.height)
        self.assertEqual(cumulonimbus, s.cumulonimbus)
        self.assertEqual(towering_cumulus, s.towering_cumulus)

    def test_valid_clr(self):
        self._test_valid("CLR", "CLR", None, False, False)

    def test_valid_skc(self):
        self._test_valid("SKC", "SKC", None, False, False)

    def test_valid_ncd(self):
        self._test_valid("NCD", "NCD", None, False, False)

    def test_valid_vv(self):
        self._test_valid("VV004", "VV", 400, False, False)

    def test_valid_few(self):
        self._test_valid("FEW012", "FEW", 1200, False, False)

    def test_valid_sct(self):
        self._test_valid("SCT024", "SCT", 2400, False, False)

    def test_valid_bkn(self):
        self._test_valid("BKN048", "BKN", 4800, False, False)

    def test_valid_ovc(self):
        self._test_valid("OVC120", "OVC", 12000, False, False)

    def test_valid_cb(self):
        self._test_valid("OVC015CB", "OVC", 1500, True, False)

    def test_valid_tcu(self):
        self._test_valid("FEW018TCU", "FEW", 1800, False, True)

    def _test_invalid(self, raw):
        with self.assertRaises(SkyConditionDecodeError):
            SkyCondition(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_short(self):
        self._test_invalid("FEW12")

    def test_invalid_type(self):
        self._test_invalid("RED220")

    def test_invalid_height(self):
        self._test_invalid("SCTCLD")

    def test_invalid_suffix(self):
        self._test_invalid("SCT015CU")


if __name__ == "__main__":
    unittest.main()
