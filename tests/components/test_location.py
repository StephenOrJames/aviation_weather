import unittest
from aviation_weather import Location
from aviation_weather.exceptions import LocationDecodeError


class TestLocation(unittest.TestCase):
    """Unit tests for aviation_weather.components.location.Location"""

    def _test_valid(self, identifier):
        location = Location(identifier)
        self.assertEqual(identifier, location.raw)
        self.assertEqual(identifier, location.identifier)

    def test_valid_4letter(self):
        self._test_valid("KATL")

    def test_valid_alphanumeric(self):
        self._test_valid("K7R3")

    def _test_invalid(self, identifier):
        with self.assertRaises(LocationDecodeError):
            Location(identifier)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_numbers(self):
        self._test_invalid("1234")

    def test_invalid_short(self):
        self._test_invalid("Bad")

    def test_invalid_long(self):
        self._test_invalid("Worse")
