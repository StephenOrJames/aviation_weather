import unittest
from aviation_weather import WeatherGroup
from aviation_weather.exceptions import WeatherGroupDecodeException


class TestWeatherGroup(unittest.TestCase):
    """Unit tests for aviation_weather.components.weathergroup.WeatherGroup"""

    def _valid_tests(self, raw, intensity, descriptor, phenomenon):
        w = WeatherGroup(raw)
        self.assertEqual(str(w), raw)
        self.assertEqual(w.intensity, intensity)
        self.assertEqual(w.descriptor, descriptor)
        self.assertEqual(w.phenomenon, phenomenon)

    def test_valid_mist(self):
        self._valid_tests("BR", "", None, "BR")

    def test_valid_heavy_snow(self):
        self._valid_tests("+SN", "+", None, "SN")

    def test_valid_freezing_fog(self):
        self._valid_tests("FZFG", "", "FZ", "FG")

    def test_valid_vicinity_thunderstorm(self):
        self._valid_tests("VCTS", "VC", "TS", None)

    def test_valid_light_rain(self):
        self._valid_tests("-RA", "-", None, "RA")

    def test_valid_light_rain_snow(self):
        self._valid_tests("-RASN", "-", None, ("RA", "SN"))

    def _invalid_tests(self, raw):
        with self.assertRaises(WeatherGroupDecodeException):
            WeatherGroup(raw)

    def test_invalid_empty(self):
        self._invalid_tests("")

    def test_invalid_description_phenomenon_1(self):
        self._invalid_tests("+AA")

    def test_invalid_description_phenomenon_2(self):
        self._invalid_tests("VCBIRD")


if __name__ == "__main__":
    unittest.main()
