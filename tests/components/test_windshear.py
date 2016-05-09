import unittest

from aviation_weather.components.wind import Wind
from aviation_weather.components.windshear import WindShear
from aviation_weather.exceptions import WindShearDecodeError


class TestWindShear(unittest.TestCase):

    def _test_valid(self, raw, altitude, wind):
        ws = WindShear(raw)
        self.assertEqual(raw, ws.raw)
        self.assertEqual(altitude, ws.altitude)
        self.assertEqual(wind, ws.wind)

    def test_valid_1(self):
        self._test_valid(
            raw="WS010/31022KT",
            altitude=1000,
            wind=Wind("31022KT")
        )

    def test_valid_2(self):
        self._test_valid(
            raw="WS020/18040KT",
            altitude=2000,
            wind=Wind("18040KT")
        )

    def _test_invalid(self, raw):
        with self.assertRaises(WindShearDecodeError):
            WindShear(raw)

    def test_invalid_blank(self):
        self._test_invalid("")

    def test_invalid_altitude(self):
        self._test_invalid("WS20/02020KT")

    def test_invalid_wind(self):
        self._test_invalid("WS100/100")
