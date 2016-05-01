import unittest

from aviation_weather.components.pressure import Pressure
from aviation_weather.components.remarks import Remarks
from aviation_weather.components.runwayvisualrange import RunwayVisualRange
from aviation_weather.components.skycondition import SkyCondition
from aviation_weather.components.location import Location
from aviation_weather.components.temperature import Temperature
from aviation_weather.components.time import Time
from aviation_weather.components.visibility import Visibility
from aviation_weather.components.weathergroup import WeatherGroup
from aviation_weather.components.wind import Wind
from aviation_weather.report import Report


class TestReport(unittest.TestCase):
    """Unit tests for the Report parser"""

    def _test_parse(self, raw, location, time, wind, visibility, runway_visual_range,
                    weather_groups, sky_conditions, temperature, pressure, remarks):
        report = Report(raw)

        self.assertEqual(report.raw, raw)
        # TODO: assert report.type and report.modifier
        self.assertEqual(report.location, location)
        self.assertEqual(report.time, time)
        self.assertEqual(report.wind, wind)
        self.assertEqual(report.visibility, visibility)
        self.assertEqual(report.runway_visual_range, runway_visual_range)
        self.assertEqual(report.weather_groups, weather_groups)
        self.assertEqual(report.sky_conditions, sky_conditions)
        self.assertEqual(report.temperature, temperature)
        self.assertEqual(report.pressure, pressure)
        self.assertEqual(report.remarks, remarks)

    def test_parse_KJFK(self):
        self._test_parse(
            raw=("KJFK 182151Z 28022G34KT 10SM SCT065 M04/M17 A2990 RMK AO2 "
                 "PK WND 30034/2145 SLP123 VIRGA OHD AND E-SE T10391167"),
            location=Location("KJFK"),
            time=Time("182151Z"),
            wind=Wind("28022G34KT"),
            visibility=Visibility("10SM"),
            runway_visual_range=None,
            weather_groups=None,
            sky_conditions=(SkyCondition("SCT065"),),
            temperature=Temperature("M04/M17"),
            pressure=Pressure("A2990"),
            remarks=Remarks("RMK AO2 PK WND 30034/2145 SLP123 VIRGA OHD AND E-SE T10391167")
        )

    def test_parse_MKJP(self):
        self._test_parse(
            raw="MKJP 182300Z 14014KT 9999 SCT022 28/22 Q1015",
            location=Location("MKJP"),
            time=Time("182300Z"),
            wind=Wind("14014KT"),
            visibility=Visibility("9999"),
            runway_visual_range=None,
            weather_groups=None,
            sky_conditions=(SkyCondition("SCT022"),),
            temperature=Temperature("28/22"),
            pressure=Pressure("Q1015"),
            remarks=None
        )

    def test_parse_LBBG(self):
        self._test_parse(
            raw=("METAR LBBG 041600Z 12003MPS 290V310 1400 R04/P1500N R22/P1500U "
                 "+SN BKN022 OVC050 M04/M07 Q1020 NOSIG 8849//91="),
            location=Location("LBBG"),
            time=Time("041600Z"),
            wind=Wind("12003MPS 290V310"),
            visibility=Visibility("1400"),
            runway_visual_range=(RunwayVisualRange("R04/P1500N"), RunwayVisualRange("R22/P1500U")),
            weather_groups=(WeatherGroup("+SN"),),
            sky_conditions=(SkyCondition("BKN022"), SkyCondition("OVC050")),
            temperature=Temperature("M04/M07"),
            pressure=Pressure("Q1020"),
            remarks=None
        )

    def test_parse_KTTN(self):
        self._test_parse(
            raw=("METAR KTTN 051853Z 04011KT 1/2SM VCTS SN FZFG BKN003 OVC010 "
                 "M02/M02 A3006 RMK AO2 TSB40 SLP176 P0002 T10171017="),
            location=Location("KTTN"),
            time=Time("051853Z"),
            wind=Wind("04011KT"),
            visibility=Visibility("1/2SM"),
            runway_visual_range=None,
            weather_groups=(WeatherGroup("VCTS"), WeatherGroup("SN"), WeatherGroup("FZFG")),
            sky_conditions=(SkyCondition("BKN003"), SkyCondition("OVC010")),
            temperature=Temperature("M02/M02"),
            pressure=Pressure("A3006"),
            remarks=Remarks("RMK AO2 TSB40 SLP176 P0002 T10171017=")
        )

    def test_parse_KSLC(self):
        self._test_parse(
            raw="KSLC 192353Z 30004KT 10SM CLR 29/02 A3000 RMK AO2 SLP110 T02940017 10306 20261 56014",
            location=Location("KSLC"),
            time=Time("192353Z"),
            wind=Wind("30004KT"),
            visibility=Visibility("10SM"),
            runway_visual_range=None,
            weather_groups=None,
            sky_conditions=(SkyCondition("CLR"),),
            temperature=Temperature("29/02"),
            pressure=Pressure("A3000"),
            remarks=Remarks("RMK AO2 SLP110 T02940017 10306 20261 56014")
        )

    def test_parse_KAZO(self):
        self._test_parse(
            raw=("KAZO 270257Z 26013KT 1 3/4SM R35/4500VP6000FT -SN BKN016 "
                 "OVC022 M02/M06 A3009 RMK AO2 P0000 T10221056"),
            location=Location("KAZO"),
            time=Time("270257Z"),
            wind=Wind("26013KT"),
            visibility=Visibility("1 3/4SM"),
            runway_visual_range=(RunwayVisualRange("R35/4500VP6000FT"),),
            weather_groups=(WeatherGroup("-SN"),),
            sky_conditions=(SkyCondition("BKN016"), SkyCondition("OVC022")),
            temperature=Temperature("M02/M06"),
            pressure=Pressure("A3009"),
            remarks=Remarks("RMK AO2 P0000 T10221056")
        )

    def test_parse_TJSJ(self):
        self._test_parse(
            raw=("SPECI TJSJ 270256Z 12003KT 10SM FEW020 SCT036 BKN095 24/22 A3013 "
                 "RMK AO2 RAB06E37 SLP203 SHRA DSNT W P0024 60026 T02440222 50005"),
            location=Location("TJSJ"),
            time=Time("270256Z"),
            wind=Wind("12003KT"),
            visibility=Visibility("10SM"),
            runway_visual_range=None,
            weather_groups=None,
            sky_conditions=(SkyCondition("FEW020"), SkyCondition("SCT036"), SkyCondition("BKN095")),
            temperature=Temperature("24/22"),
            pressure=Pressure("A3013"),
            remarks=Remarks("RMK AO2 RAB06E37 SLP203 SHRA DSNT W P0024 60026 T02440222 50005")
        )

    def test_parse_EIDW(self):
        self._test_parse(
            raw="EIDW 092307Z 24035G55KT 210V270 1700 +SHRA BKN007 OVC015CB 08/07",
            location=Location("EIDW"),
            time=Time("092307Z"),
            wind=Wind("24035G55KT 210V270"),
            visibility=Visibility("1700"),
            runway_visual_range=None,
            weather_groups=(WeatherGroup("+SHRA"),),
            sky_conditions=(SkyCondition("BKN007"), SkyCondition("OVC015CB")),
            temperature=Temperature("08/07"),
            pressure=None,
            remarks=None
        )

    def _test_retrieve(self, code):
        self.assertIsInstance(Report.retrieve(code), Report)

    def test_retrieve_KJFK(self):
        self._test_retrieve("KJFK")

    def test_retrieve_EGLL(self):
        self._test_retrieve("EGLL")


if __name__ == "__main__":
    unittest.main()
