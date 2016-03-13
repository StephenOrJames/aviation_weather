import unittest
from aviation_weather import SkyCondition
from aviation_weather.exceptions import SkyConditionDecodeError


class TestSkyCondition(unittest.TestCase):
    """Unit tests for aviation_weather.components.skycondition.SkyCondition"""

    def _test_valid(self, raw, type_, height, cumulonimbus):
        s = SkyCondition(raw)
        self.assertEqual(str(s), raw)
        self.assertEqual(s.type, type_)
        self.assertEqual(s.height, height)
        self.assertEqual(s.cumulonimbus, cumulonimbus)

    def test_valid_clr(self):
        self._test_valid("CLR", "CLR", None, False)

    def test_valid_skc(self):
        self._test_valid("SKC", "SKC", None, False)

    def test_valid_ncd(self):
        self._test_valid("NCD", "NCD", None, False)

    def test_valid_vv(self):
        self._test_valid("VV004", "VV", 400, False)

    def test_valid_few(self):
        self._test_valid("FEW012", "FEW", 1200, False)

    def test_valid_sct(self):
        self._test_valid("SCT024", "SCT", 2400, False)

    def test_valid_bkn(self):
        self._test_valid("BKN048", "BKN", 4800, False)

    def test_valid_ovc(self):
        self._test_valid("OVC120", "OVC", 12000, False)

    def test_valid_cb(self):
        self._test_valid("OVC015CB", "OVC", 1500, True)

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


if __name__ == "__main__":
    unittest.main()
