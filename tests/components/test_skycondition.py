import unittest
from aviation_weather import SkyCondition
from aviation_weather.exceptions import SkyConditionDecodeException


class TestSkyCondition(unittest.TestCase):
    """Unit tests for aviation_weather.components.skycondition.SkyCondition"""

    def test_valid(self):
        """Test valid sky conditions"""

        tests = [
            "CLR",
            "SKC",
            "NCD",
            "VV004",
            "FEW012",
            "SCT024",
            "BKN048",
            "OVC120",
            "OVC015CB"
        ]
        for test in tests:
            self.assertEqual(test, str(SkyCondition(test)))

    def test_invalid(self):
        """Test invalid sky conditions"""

        tests = [
            "",  # Empty
            "FEW12",  # Height should be 3 digits
            "RED220",  # Invalid type
            "SCTCLD",  # Invalid height
        ]
        for test in tests:
            with self.assertRaises(SkyConditionDecodeException):
                SkyCondition(test)


if __name__ == "__main__":
    unittest.main()
