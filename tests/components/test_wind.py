import unittest
from aviation_weather import Wind
from aviation_weather.exceptions import WindDecodeException


class TestWind(unittest.TestCase):
    """Unit tests for aviation_weather.components.wind.Wind"""

    def test_valid(self):
        """Test valid winds"""

        tests = [
            ("35007KT", 350, 7, None, None),  # simple (KT)
            ("21007MPS", 210, 7, None, None),  # simple (MPS)
            ("350107KT", 350, 107, None, None),  # strong winds
            ("32013G17KT", 320, 13, 17, None),  # gusts
            ("05013G127KT", 50, 13, 127, None),  # strong gusts
            ("VRB01MPS", "VRB", 1, None, None),  # variable (weak)
            ("14003KT 110V170", 140, 3, None, (110, 170))  # variable (strong)
        ]
        for test in tests:
            w = Wind(test[0])
            self.assertEqual(test[0], str(w))
            self.assertEqual(test[1], w.direction)
            self.assertEqual(test[2], w.speed)
            self.assertEqual(test[3], w.gusts)
            self.assertEqual(test[4], w.variable)

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
