import unittest
from aviation_weather import Station
from aviation_weather.exceptions import StationDecodeException


class TestStation(unittest.TestCase):
    """Unit tests for aviation_weather.components.station.Station"""

    def _valid_tests(self, identifier):
        s = Station(identifier)
        self.assertEqual(identifier, str(s))
        self.assertEqual(identifier, s.identifier)

    def test_valid_4letter(self):
        self._valid_tests("KATL")

    def test_valid_alphanumeric(self):
        self._valid_tests("K7R3")

    def _invalid_tests(self, identifier):
        with self.assertRaises(StationDecodeException):
            Station(identifier)

    def test_invalid_empty(self):
        self._invalid_tests("")

    def test_invalid_numbers(self):
        self._invalid_tests("1234")

    def test_invalid_short(self):
        self._invalid_tests("Bad")

    def test_invalid_long(self):
        self._invalid_tests("Worse")


if __name__ == "__main__":
    unittest.main()
