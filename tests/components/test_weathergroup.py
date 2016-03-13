import unittest
from aviation_weather import WeatherGroup
from aviation_weather.exceptions import WeatherGroupDecodeError


class TestWeatherGroup(unittest.TestCase):
    """Unit tests for aviation_weather.components.weathergroup.WeatherGroup"""

    def _test_valid(self, raw, intensity, descriptor, phenomenon):
        w = WeatherGroup(raw)
        self.assertEqual(str(w), raw)
        self.assertEqual(w.intensity, intensity)
        self.assertEqual(w.descriptor, descriptor)
        self.assertEqual(w.phenomenon, phenomenon)

    def test_valid_mist(self):
        self._test_valid("BR", "", None, "BR")

    def test_valid_heavy_snow(self):
        self._test_valid("+SN", "+", None, "SN")

    def test_valid_freezing_fog(self):
        self._test_valid("FZFG", "", "FZ", "FG")

    def test_valid_vicinity_thunderstorm(self):
        self._test_valid("VCTS", "VC", "TS", None)

    def test_valid_light_rain(self):
        self._test_valid("-RA", "-", None, "RA")

    def test_valid_light_rain_snow(self):
        self._test_valid("-RASN", "-", None, ("RA", "SN"))

    def _test_invalid(self, raw):
        with self.assertRaises(WeatherGroupDecodeError):
            WeatherGroup(raw)

    def test_invalid_empty(self):
        self._test_invalid("")

    def test_invalid_description_phenomenon_1(self):
        self._test_invalid("+AA")

    def test_invalid_description_phenomenon_2(self):
        self._test_invalid("VCBIRD")


if __name__ == "__main__":
    unittest.main()
