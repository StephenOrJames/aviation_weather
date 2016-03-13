import unittest
from aviation_weather import Remarks
from aviation_weather.exceptions import RemarksDecodeException


class TestRemarks(unittest.TestCase):
    """Unit tests for aviation_weather.components.remarks.Remarks"""

    def test_valid(self):
        s = "RMK AO2 PK WND 14027/1802 SLP183 P0018 T01170106"
        r = Remarks(s)
        self.assertEqual(s, str(r))
        self.assertEqual(s, r.text)

    def test_invalid(self):
        with self.assertRaises(RemarksDecodeException):
            Remarks("AO2 PK WND 14027/1802 SLP183 P0018 T01170106")


if __name__ == "__main__":
    unittest.main()
