import unittest
from aviation_weather import Station
from aviation_weather.exceptions import StationDecodeError


class TestStation(unittest.TestCase):
    """Unit tests for aviation_weather.components.station.Station"""

    def _test_valid(self, identifier):
        s = Station(identifier)
        self.assertEqual(identifier, s.raw)
        self.assertEqual(identifier, s.identifier)

    def test_valid_4letter(self):
        self._test_valid("KATL")

    def test_valid_alphanumeric(self):
        self._test_valid("K7R3")

    def _test_invalid(self, identifier):
        with self.assertRaises(StationDecodeError):
            Station(identifier)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_numbers(self):
        self._test_invalid("1234")

    def test_invalid_short(self):
        self._test_invalid("Bad")

    def test_invalid_long(self):
        self._test_invalid("Worse")


if __name__ == "__main__":
    unittest.main()
