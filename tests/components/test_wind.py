import unittest
from aviation_weather import Wind
from aviation_weather.exceptions import WindDecodeException


class TestWind(unittest.TestCase):
    """Unit tests for aviation_weather.components.wind.Wind"""

    def test_valid(self):
        """Test valid winds"""

        tests = [
            "35007KT",  # simple (KT)
            "21007MPS",  # simple (MPS)
            "350107KT",  # strong winds
            "32013G17KT",  # gusts
            "32013G127KT",  # strong gusts
            "VRB01MPS",  # variable (weak)
            "14003KT 110V170",  # variable (strong)
        ]
        for test in tests:
            self.assertEqual(test, str(Wind(test)))

    def test_invalid(self):
        """Test invalid winds"""

        tests = [
            "",  # Empty
            "1012KT",  # Too short
            "3210123KT",  # Too long
            "21012KN",  # Bad unit
            "VRBMPS",  # No strength
            "21012G21",  # No unit
        ]
        for test in tests:
            with self.assertRaises(WindDecodeException):
                Wind(test)


if __name__ == "__main__":
    unittest.main()
