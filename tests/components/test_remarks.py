import unittest
from aviation_weather import Remarks
from aviation_weather.exceptions import RemarksDecodeError


class TestRemarks(unittest.TestCase):
    """Unit tests for aviation_weather.components.remarks.Remarks"""

    def _test_valid(self, raw, ao):
        rmk = Remarks(raw)
        self.assertEqual(raw, rmk.raw)
        self.assertEqual(raw, rmk.text)
        self.assertEqual(ao, rmk.ao)

    def test_valid_1(self):
        self._test_valid(
            raw="RMK AO2 PK WND 14027/1802 SLP183 P0018 T01170106",
            ao=2
        )

    def test_valid_2(self):
        self._test_valid(
            raw="RMK AO2 RAB06E37 SLP203 SHRA DSNT W P0024 60026 T02440222 50005",
            ao=2
        )

    def test_valid_3(self):
        self._test_valid(
            raw="RMK AO1",
            ao=1
        )

    def test_valid_4(self):
        self._test_valid(
            raw="RMK AO1 WEA:-RA KH P0001",
            ao=1
        )

    def test_valid_5(self):
        self._test_valid(
            raw="RMK 8/200 HZY MSGTX MMMD",
            ao=None
        )

    def _test_invalid(self, raw):
        with self.assertRaises(RemarksDecodeError):
            Remarks(raw)

    def test_invalid_1(self):
        self._test_invalid("")

    def test_invalid_2(self):
        self._test_invalid("AO2 PK WND 14027/1802 SLP183 P0018 T01170106")

    def test_invalid_3(self):
        self._test_invalid("This RMK is not valid")
