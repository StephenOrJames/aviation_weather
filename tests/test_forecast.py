import unittest
import aviation_weather


class TestForecast(unittest.TestCase):
    """Unit tests for the Forecast parser"""

    def _test_parse(self, raw, type_, location, time, valid_period, wind, visibility,
                    weather_groups, sky_conditions, wind_shear, changes):
        forecast = aviation_weather.Forecast(raw)
        self.assertEqual(raw, forecast.raw)
        self.assertEqual(type_, forecast.type)
        self.assertEqual(location, forecast.location)
        self.assertEqual(time, forecast.time)
        self.assertEqual(valid_period, forecast.valid_period)
        self.assertEqual(wind, forecast.wind)
        self.assertEqual(visibility, forecast.visibility)
        self.assertEqual(weather_groups, forecast.weather_groups)
        self.assertEqual(sky_conditions, forecast.sky_conditions)
        self.assertEqual(wind_shear, forecast.wind_shear)
        self.assertEqual(changes, forecast.changes)

    def test_parse_1(self):
        self._test_parse(
            raw=("TAF KPIT 091730Z 0918/1024 15005KT 5SM HZ FEW020 WS010/31022KT"
                 " FM091930 30015G25KT 3SM SHRA OVC015"
                 " TEMPO 0920/0922 1/2SM +TSRA OVC008CB"
                 " FM100100 27008KT 5SM SHRA BKN020 OVC040"
                 " PROB30 1004/1007 1SM -RA BR"
                 " FM101015 18005KT 6SM -SHRA OVC020"
                 " BECMG 1013/1015 P6SM NSW SKC"),
            type_=aviation_weather.MessageType("TAF"),
            location=aviation_weather.Location("KPIT"),
            time=aviation_weather.Time("091730Z"),
            valid_period=(aviation_weather.Time("091800Z"), aviation_weather.Time("102400Z")),
            wind=aviation_weather.Wind("15005KT"),
            visibility=aviation_weather.Visibility("5SM"),
            weather_groups=(aviation_weather.WeatherGroup("HZ"),),
            sky_conditions=(aviation_weather.SkyCondition("FEW020"),),
            wind_shear=aviation_weather.WindShear("WS010/31022KT"),
            changes=[
                aviation_weather.FromGroup("FM091930 30015G25KT 3SM SHRA OVC015"),
                aviation_weather.TemporaryGroup("TEMPO 0920/0922 1/2SM +TSRA OVC008CB"),
                aviation_weather.FromGroup("FM100100 27008KT 5SM SHRA BKN020 OVC040"),
                aviation_weather.ProbabilityGroup("PROB30 1004/1007 1SM -RA BR"),
                aviation_weather.FromGroup("FM101015 18005KT 6SM -SHRA OVC020"),
                aviation_weather.BecomingGroup("BECMG 1013/1015 P6SM NSW SKC")
            ]
        )

    def test_parse_2(self):
        self._test_parse(
            raw=("TAF EGKK 082259Z 0900/1006 08008KT CAVOK"
                 " BECMG 0909/0912 BKN040"
                 " TEMPO 0912/0921 6000 SHRA"
                 " PROB30"
                 " TEMPO 0913/0920 4000 +SHRA BKN012 BKN025CB"
                 " PROB30 0921/1004 5000 HZ"
                 " BECMG 1004/1006 6000 -RADZ BKN010"
                 " PROB40"
                 " TEMPO 1005/1006 4000 RADZ BKN006"),
            type_=aviation_weather.MessageType("TAF"),
            location=aviation_weather.Location("EGKK"),
            time=aviation_weather.Time("082259Z"),
            valid_period=(aviation_weather.Time("090000Z"), aviation_weather.Time("100600Z")),
            wind=aviation_weather.Wind("08008KT"),
            visibility=aviation_weather.Visibility("CAVOK"),
            weather_groups=(),
            sky_conditions=(),
            wind_shear=None,
            changes=[
                aviation_weather.BecomingGroup("BECMG 0909/0912 BKN040"),
                aviation_weather.TemporaryGroup("TEMPO 0912/0921 6000 SHRA"),
                aviation_weather.ProbabilityGroup("PROB30"),
                aviation_weather.TemporaryGroup("TEMPO 0913/0920 4000 +SHRA BKN012 BKN025CB"),
                aviation_weather.ProbabilityGroup("PROB30 0921/1004 5000 HZ"),
                aviation_weather.BecomingGroup("BECMG 1004/1006 6000 -RADZ BKN010"),
                aviation_weather.ProbabilityGroup("PROB40"),
                aviation_weather.TemporaryGroup("TEMPO 1005/1006 4000 RADZ BKN006")
            ]
        )

    def test_parse_3(self):
        self._test_parse(
            raw=("KMIA 090259Z 0903/0924 VRB05KT P6SM SKC"
                 " FM091400 12013KT P6SM SCT050"),
            type_=None,
            location=aviation_weather.Location("KMIA"),
            time=aviation_weather.Time("090259Z"),
            valid_period=(aviation_weather.Time("090300Z"), aviation_weather.Time("092400Z")),
            wind=aviation_weather.Wind("VRB05KT"),
            visibility=aviation_weather.Visibility("P6SM"),
            weather_groups=(),
            sky_conditions=(aviation_weather.SkyCondition("SKC"),),
            wind_shear=None,
            changes=[
                aviation_weather.FromGroup("FM091400 12013KT P6SM SCT050")
            ]
        )

    def test_parse_4(self):
        self._test_parse(
            raw=("TAF CYVR 090538Z 0906/1012 10010KT P6SM FEW040 FEW070"
                 " TEMPO 0906/0909 FEW020 SCT040 BKN070"
                 " PROB30 0906/0907 VRB15G25KT 6SM TSRA SCT015 BKN040CB"
                 " FM090900 10008KT P6SM FEW080"
                 " BECMG 0910/0912 33007KT"
                 " BECMG 0918/0920 28015KT"
                 " FM100800 VRB03KT P6SM SKC RMK NXT FCST BY 090900Z"),
            type_=aviation_weather.MessageType("TAF"),
            location=aviation_weather.Location("CYVR"),
            time=aviation_weather.Time("090538Z"),
            valid_period=(aviation_weather.Time("090600Z"), aviation_weather.Time("101200Z")),
            wind=aviation_weather.Wind("10010KT"),
            visibility=aviation_weather.Visibility("P6SM"),
            weather_groups=(),
            sky_conditions=(aviation_weather.SkyCondition("FEW040"), aviation_weather.SkyCondition("FEW070")),
            wind_shear=None,
            changes=[
                aviation_weather.TemporaryGroup("TEMPO 0906/0909 FEW020 SCT040 BKN070"),
                aviation_weather.ProbabilityGroup("PROB30 0906/0907 VRB15G25KT 6SM TSRA SCT015 BKN040CB"),
                aviation_weather.FromGroup("FM090900 10008KT P6SM FEW080"),
                aviation_weather.BecomingGroup("BECMG 0910/0912 33007KT"),
                aviation_weather.BecomingGroup("BECMG 0918/0920 28015KT"),
                aviation_weather.FromGroup("FM100800 VRB03KT P6SM SKC RMK NXT FCST BY 090900Z")
            ]
        )
