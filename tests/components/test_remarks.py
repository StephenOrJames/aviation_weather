import unittest
from aviation_weather import Remarks
from aviation_weather.exceptions import RemarksDecodeException


class TestRemarks(unittest.TestCase):
    """Unit tests for aviation_weather.components.remarks.Remarks"""

    def test_valid(self):
        """Test valid remarks"""

        test = "RMK AO2 PK WND 14027/1802 SLP183 P0018 T01170106"
        self.assertEqual(test, str(Remarks(test)))

    def test_invalid(self):
        """Test invalid remarks"""

        with self.assertRaises(RemarksDecodeException):
            Remarks("AO2 PK WND 14027/1802 SLP183 P0018 T01170106")


if __name__ == "__main__":
    unittest.main()
