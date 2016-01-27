import unittest
from aviation.weather.weather import *


class TestWeather(unittest.TestCase):
    """Unit tests for the various weather parsers"""

    def test_station(self):
        """Tests for weather.Station"""

        # Valid
        self.assertEqual("KATL", str(Station("KATL")))  # 4-letter code
        self.assertEqual("K7R3", str(Station("K7R3")))  # Alphanumeric code

        # Invalid
        tests = [
            "",  # Empty
            "1234",  # Starts with a number
            "Bad",  # Too short
            "Worse",  # Too long
        ]
        for test in tests:
            with self.assertRaises(StationDecodeException):
                Station(test)

    def test_time(self):
        """Tests for weather.Time"""

        # Valid
        self.assertEqual("161851Z", str(Time("161851Z")))

        # Invalid
        with self.assertRaises(TimeDecodeException):
            Time("")  # Empty
        with self.assertRaises(TimeDecodeException):
            Time("ABCDEFZ")  # Definitely not a time
        with self.assertRaises(TimeDecodeException):
            Time("1851Z")  # Where's the date

    def test_wind(self):
        """Tests for weather.Wind"""

        # Valid
        tests = [
            "35007KT",  # simple (KT)
            "21007MPS",  # simple (MPS)
            "350107KT",  # strong winds
            "32013G17KT",  # gusts
            "32013G127KT",  # strong gusts
            "VRB01MPS",  # variable (weak)
            "14003KT 110V170",  # variable (strong)
        ]
        for test in tests:
            self.assertEqual(test, str(Wind(test)))

        # Invalid
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

    def test_visibility(self):
        """Tests for weather.Visibility"""

        # Valid
        tests = [
            "1SM",
            "20SM",
            "1/2SM",
            "M1/2SM",
            "M1 1/4SM",
            "9999",
            "2000",
        ]
        for test in tests:
            self.assertEqual(test, str(Visibility(test)))

        # Invalid
        tests = [
            "",  # Empty
            "MSM",  # No value
            "120",  # Expect 4 digits if no unit specified
            "12345",  # Too long (no unit)
            "123456SM",  # Too long (SM)
        ]
        for test in tests:
            with self.assertRaises(VisibilityDecodeException):
                Visibility(test)

    def test_runway_visual_range(self):
        """Tests for weather.RunwayVisualRange"""

        # Valid
        tests = [
            "R12/2000",
            "R12/M1000FT",
            "R26L/P2000N",
            "R08R/0800V2000U",
            "R09/1000VP6000FT"
        ]
        for test in tests:
            self.assertEqual(test, str(RunwayVisualRange(test)))

        # Invalid
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

    def test_weather_group(self):
        """Tests for weather.WeatherGroup"""

        # Valid
        tests = [
            "BR",
            "+SN",
            "FZFG",
            "VCTS",
            "-RA",
            "-RASN"
        ]
        for test in tests:
            self.assertEqual(test, str(WeatherGroup(test)))

        # Invalid
        tests = [
            "",  # Empty
            "+AA",  # Invalid descriptor/phenomenon
            "VCBIRD"  # Invalid descriptor/phenomenon
        ]
        for test in tests:
            with self.assertRaises(WeatherGroupDecodeException):
                WeatherGroup(test)

    def test_sky_condition(self):
        """Tests for weather.SkyCondition"""

        # Valid
        tests = [
            "CLR",
            "SKC",
            "NCD",
            "VV004",
            "FEW012",
            "SCT024",
            "BKN048",
            "OVC120",
        ]
        for test in tests:
            self.assertEqual(test, str(SkyCondition(test)))

        # Invalid
        tests = [
            "",  # Empty
            "FEW12",  # Height should be 3 digits
            "RED220",  # Invalid type
            "SCTCLD",  # Invalid height
        ]
        for test in tests:
            with self.assertRaises(SkyConditionDecodeException):
                SkyCondition(test)

    def test_temperature(self):
        """Tests for weather.Temperature"""

        # Valid
        tests = [
            "21/12",
            "21/M12",
            "M01/M04",
        ]
        for test in tests:
            self.assertEqual(test, str(Temperature(test)))

        # Invalid
        tests = [
            "M/M",
            "1200",
            "////"
        ]
        for test in tests:
            with self.assertRaises(TemperatureDecodeException):
                Temperature(test)

    def test_altimeter_setting(self):
        """Tests for weather.AltimeterSetting"""

        # Valid
        self.assertEqual("A2992", str(AltimeterSetting("A2992")))
        self.assertEqual("Q1013", str(AltimeterSetting("Q1013")))

        # Invalid
        with self.assertRaises(AltimeterSettingDecodeException):
            AltimeterSetting("3000")  # no unit indicator; more likely visibility

    def test_remarks(self):
        """Tests for weather.Remarks"""

        # Pretty much valid if it can repeat what it was told
        test = "AO2 PK WND 14027/1802 SLP183 P0018 T01170106"
        self.assertEqual(test, str(Remarks(test)))


if __name__ == "__main__":
    unittest.main()
