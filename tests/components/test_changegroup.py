import unittest

import aviation_weather


class TestChangeGroup(unittest.TestCase):

    def _test_change_group(self, raw, group, wind, visibility, weather_groups, sky_conditions):
        self.assertEqual(wind, group.wind)
        self.assertEqual(visibility, group.visibility)
        self.assertEqual(weather_groups, group.weather_groups)
        self.assertEqual(sky_conditions, group.sky_conditions)
        self.assertEqual(raw, group.raw)

    def _test_becoming_group(self, raw, start_time, end_time, **kwargs):
        group = aviation_weather.BecomingGroup(raw)
        self.assertEqual(start_time, group.start_time)
        self.assertEqual(end_time, group.end_time)
        self._test_change_group(raw, group, **kwargs)

    def _test_from_group(self, time, raw, **kwargs):
        group = aviation_weather.FromGroup(raw)
        self.assertEqual(time, group.time)
        self._test_change_group(raw, group, **kwargs)

    def _test_probability_group(self, raw, probability, start_time, end_time, **kwargs):
        group = aviation_weather.ProbabilityGroup(raw)
        self.assertEqual(probability, group.probability)
        self.assertEqual(start_time, group.start_time)
        self.assertEqual(end_time, group.end_time)
        self._test_change_group(raw, group, **kwargs)

    def _test_temporary_group(self, raw, start_time, end_time, **kwargs):
        group = aviation_weather.TemporaryGroup(raw)
        self.assertEqual(start_time, group.start_time)
        self.assertEqual(end_time, group.end_time)
        self._test_change_group(raw, group, **kwargs)

    def test_becoming_group_1(self):
        self._test_becoming_group(
            raw="BECMG 1013/1015 P6SM NSW SKC",
            start_time=aviation_weather.Time("101300Z"),
            end_time=aviation_weather.Time("101500Z"),
            wind=None,
            visibility=aviation_weather.Visibility("P6SM"),
            weather_groups=(aviation_weather.WeatherGroup("NSW"),),
            sky_conditions=(aviation_weather.SkyCondition("SKC"),)
        )

    def test_becoming_group_2(self):
        self._test_becoming_group(
            raw="BECMG 0205/0208 BKN020",
            start_time=aviation_weather.Time("020500Z"),
            end_time=aviation_weather.Time("020800Z"),
            wind=None,
            visibility=None,
            weather_groups=(),
            sky_conditions=(aviation_weather.SkyCondition("BKN020"),)
        )

    def test_becoming_group_3(self):
        self._test_becoming_group(
            raw="BECMG 0200/0203 VRB03KT",
            start_time=aviation_weather.Time("020000Z"),
            end_time=aviation_weather.Time("020300Z"),
            wind=aviation_weather.Wind("VRB03KT"),
            visibility=None,
            weather_groups=(),
            sky_conditions=()
        )

    def test_from_group_1(self):
        self._test_from_group(
            raw="FM091930 30015G25KT 3SM SHRA OVC015",
            time=aviation_weather.Time("091930Z"),
            wind=aviation_weather.Wind("30015G25KT"),
            visibility=aviation_weather.Visibility("3SM"),
            weather_groups=(aviation_weather.WeatherGroup("SHRA"),),
            sky_conditions=(aviation_weather.SkyCondition("OVC015"),)
        )

    def test_from_group_2(self):
        self._test_from_group(
            raw="FM100100 27008KT 5SM SHRA BKN020 OVC040",
            time=aviation_weather.Time("100100Z"),
            wind=aviation_weather.Wind("27008KT"),
            visibility=aviation_weather.Visibility("5SM"),
            weather_groups=(aviation_weather.WeatherGroup("SHRA"),),
            sky_conditions=(aviation_weather.SkyCondition("BKN020"), aviation_weather.SkyCondition("OVC040"))
        )

    def test_from_group_3(self):
        self._test_from_group(
            raw="FM101015 18005KT 6SM -SHRA OVC020",
            time=aviation_weather.Time("101015Z"),
            wind=aviation_weather.Wind("18005KT"),
            visibility=aviation_weather.Visibility("6SM"),
            weather_groups=(aviation_weather.WeatherGroup("-SHRA"),),
            sky_conditions=(aviation_weather.SkyCondition("OVC020"),)
        )

    def test_probability_group_1(self):
        self._test_probability_group(
            raw="PROB30 1004/1007 1SM -RA BR",
            probability=30,
            start_time=aviation_weather.Time("100400Z"),
            end_time=aviation_weather.Time("100700Z"),
            wind=None,
            visibility=aviation_weather.Visibility("1SM"),
            weather_groups=(aviation_weather.WeatherGroup("-RA"), aviation_weather.WeatherGroup("BR")),
            sky_conditions=()
        )

    def test_probability_group_2(self):
        self._test_probability_group(
            raw="PROB30 0121/0206 2SM BR OVC006",
            probability=30,
            start_time=aviation_weather.Time("012100Z"),
            end_time=aviation_weather.Time("020600Z"),
            wind=None,
            visibility=aviation_weather.Visibility("2SM"),
            weather_groups=(aviation_weather.WeatherGroup("BR"),),
            sky_conditions=(aviation_weather.SkyCondition("OVC006"),)
        )

    def test_probability_group_3(self):
        self._test_probability_group(
            raw="PROB30",
            probability=30,
            start_time=None,
            end_time=None,
            wind=None,
            visibility=None,
            weather_groups=(),
            sky_conditions=()
        )

    def test_temporary_group_1(self):
        self._test_temporary_group(
            raw="TEMPO 0920/0922 1/2SM +TSRA OVC008CB",
            start_time=aviation_weather.Time("092000Z"),
            end_time=aviation_weather.Time("092200Z"),
            wind=None,
            visibility=aviation_weather.Visibility("1/2SM"),
            weather_groups=(aviation_weather.WeatherGroup("+TSRA"),),
            sky_conditions=(aviation_weather.SkyCondition("OVC008CB"),)
        )

    def test_temporary_group_2(self):
        self._test_temporary_group(
            raw="TEMPO 0100/0102 2SM -SN BR FEW007 OVC010",
            start_time=aviation_weather.Time("010000Z"),
            end_time=aviation_weather.Time("010200Z"),
            wind=None,
            visibility=aviation_weather.Visibility("2SM"),
            weather_groups=(aviation_weather.WeatherGroup("-SN"), aviation_weather.WeatherGroup("BR")),
            sky_conditions=(aviation_weather.SkyCondition("FEW007"), aviation_weather.SkyCondition("OVC010"))
        )

    def test_temporary_group_3(self):
        self._test_temporary_group(
            raw="TEMPO 0100/0103 4SM -RA BR",
            start_time=aviation_weather.Time("010000Z"),
            end_time=aviation_weather.Time("010300Z"),
            wind=None,
            visibility=aviation_weather.Visibility("4SM"),
            weather_groups=(aviation_weather.WeatherGroup("-RA"), aviation_weather.WeatherGroup("BR")),
            sky_conditions=()
        )

    def test_temporary_group_4(self):
        self._test_temporary_group(
            raw="TEMPO 0121/0124 8000 -RA",
            start_time=aviation_weather.Time("012100Z"),
            end_time=aviation_weather.Time("012400Z"),
            wind=None,
            visibility=aviation_weather.Visibility("8000"),
            weather_groups=(aviation_weather.WeatherGroup("-RA"),),
            sky_conditions=()
        )

    def test_temporary_group_5(self):
        self._test_temporary_group(
            raw="TEMPO 0207/0212 22018G28KT 4000 RA BKN012",
            start_time=aviation_weather.Time("020700Z"),
            end_time=aviation_weather.Time("021200Z"),
            wind=aviation_weather.Wind("22018G28KT"),
            visibility=aviation_weather.Visibility("4000"),
            weather_groups=(aviation_weather.WeatherGroup("RA"),),
            sky_conditions=(aviation_weather.SkyCondition("BKN012"),)
        )

    def test_temporary_group_6(self):
        self._test_temporary_group(
            raw="TEMPO 0215/0218 7000 SHRA BKN014",
            start_time=aviation_weather.Time("021500Z"),
            end_time=aviation_weather.Time("021800Z"),
            wind=None,
            visibility=aviation_weather.Visibility("7000"),
            weather_groups=(aviation_weather.WeatherGroup("SHRA"),),
            sky_conditions=(aviation_weather.SkyCondition("BKN014"),)
        )
