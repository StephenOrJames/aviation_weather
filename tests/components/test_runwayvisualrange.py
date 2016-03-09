import unittest
from aviation_weather import RunwayVisualRange
from aviation_weather.exceptions import RunwayVisualRangeDecodeException


class TestRunwayVisualRange(unittest.TestCase):
    """Unit tests for aviation_weather.components.runwayvisualrange.RunwayVisualRange"""

    def test_valid(self):
        """Test valid runway visual ranges"""

        tests = [
            "R12/2000",
            "R12/M1000FT",
            "R26L/P2000N",
            "R08R/0800V2000U",
            "R09/1000VP6000FT"
        ]
        for test in tests:
            self.assertEqual(test, str(RunwayVisualRange(test)))

    def test_invalid(self):
        """Test invalid runway visual ranges"""

        tests = [
            "",  # Empty
            "R08C",  # No distance
            "R09C/",  # No distance
            "R10/M03",  # Invalid distance (4 digits expected)
            "R11/M0600V",  # Is it varying? If so, to what? "V" isn't a valid unit or trend.
            "R12L/2000V4000FTB",  # Invalid trend
        ]
        for test in tests:
            with self.assertRaises(RunwayVisualRangeDecodeException):
                RunwayVisualRange(test)


if __name__ == "__main__":
    unittest.main()
