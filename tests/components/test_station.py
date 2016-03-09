import unittest
from aviation_weather import Station
from aviation_weather.exceptions import StationDecodeException


class TestStation(unittest.TestCase):
    """Unit tests for aviation_weather.components.station.Station"""

    def test_valid(self):
        """Test valid stations"""

        self.assertEqual("KATL", str(Station("KATL")))  # 4-letter code
        self.assertEqual("K7R3", str(Station("K7R3")))  # Alphanumeric code

    def test_invalid(self):
        """Test invalid stations"""

        tests = [
            "",  # Empty
            "1234",  # Starts with a number
            "Bad",  # Too short
            "Worse",  # Too long
        ]
        for test in tests:
            with self.assertRaises(StationDecodeException):
                Station(test)


if __name__ == "__main__":
    unittest.main()
