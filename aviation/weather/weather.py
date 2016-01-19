import re
from aviation.exceptions import *


class Station:
    """Represents a weather station"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<id>[A-Z][A-Z0-9]{3})\b", raw.upper())
        if not m:
            raise StationDecodeException
        self.identifier = m.group("id")

    def __str__(self):
        return self.identifier


class Time:
    # TODO: use the datetime library to provide additional features?

    def __init__(self, raw):
        self.day = raw[0:2]
        self.hour = raw[2:4]
        self.minute = raw[4:6]
        self.timezone = raw[6]

    def __str__(self):
        return self.day + self.hour + self.minute + self.timezone


class Wind:
    # TODO: support conversion from KT to MPS (and vice versa)?

    def __init__(self, raw):
        m = re.search(
                r"(?P<direction>(?:\d{3}|VRB))(?P<speed>\d{2,3})(?:G(?P<gusts>\d{2,3}))?(?P<unit>(?:KT|MPS))"
                r"(?: (?P<v_from>\d{3})V(?P<v_to>\d{3}))?",
                raw
        )
        if not m:
            raise WindDecodeException
        self.direction = m.group("direction")
        self.speed = m.group("speed")
        self.gusts = m.group("gusts")
        self.unit = m.group("unit")
        self.variable = (m.group("v_from"), m.group("v_to"))

    def __str__(self):
        raw = self.direction + self.speed
        if self.gusts:
            raw += "G" + self.gusts
        raw += self.unit
        if all(self.variable):
            raw += " " + self.variable[0] + "V" + self.variable[1]
        return raw


class Visibility:

    def __init__(self, raw):
        m = re.search(r"(?:\b(?P<less>M)?(?P<distance1>\d[ \d/]*)(?P<unit>SM)|\b(?P=less)?(?P<distance2>\d{4})\b)", raw)
        # int: \d{4}
        # USA: M?\d[ 0-9/]{,4}\dSM
        #
        if not m:
            raise VisibilityDecodeException
        self.less_than = True if m.group("less") else False
        self.distance = m.group("distance1") or m.group("distance2")
        self.unit = m.group("unit")

    def __str__(self):
        raw = "M" if self.less_than else ""
        raw += self.distance
        if self.unit:
            raw += self.unit
        return raw


class RunwayVisualRange:
    """Represents the runway visual range"""

    def __init__(self, raw):
        m = re.search(
                r"R(?P<runway>\d{2}[LRC]?)/(?P<pm>[PM])?(?P<d_min>\d{4})(?:V(?P<d_max>\d{4}))?(?P<unit>FT)?(?P<trend>[UND])?",
                raw
        )
        if not m:
            raise RunwayVisualRangeDecodeException
        self.runway = m.group("runway")
        self.pm = m.group("pm")
        if m.group("d_max"):
            self.distance = (m.group("d_min"), m.group("d_max"))
        else:
            self.distance = m.group("d_min")
        self.unit = m.group("unit")
        self.trend = m.group("trend")

    def __str__(self):
        raw = "R" + self.runway + "/"
        if self.pm:
            raw += self.pm
        if isinstance(self.distance, tuple):
            raw += self.distance[0] + "V" + self.distance[1]
        else:
            raw += self.distance
        if self.unit:
            raw += self.unit
        if self.trend:
            raw += self.trend
        return raw


class WeatherGroup:
    # TODO: see FMH-1 12.6.8 for specific formatting instructions

    INTENSITIES = {
        "-": "light",
        "": "moderate",
        "+": "heavy",
        "VC": "in the vicinity"  # proximity
    }
    DESCRIPTORS = {
        "BC": "patches",
        "BL": "blowing",
        "DR": "low drifting",
        "FZ": "freezing",
        "MI": "shallow",
        "PR": "partial",
        "SH": "shower(s)",
        "TS": "thunderstorm"
    }
    PHENOMENA = {
        # Precipitation
        "DZ": "drizzle",
        "GR": "hail",
        "GS": "small hail and/or snow pellets",
        "IC": "ice crystals",
        "PL": "ice pellets",
        "RA": "rain",
        "SG": "snow grains",
        "SN": "snow",
        "UP": "unknown precipitation",
        # Obscuration
        "BR": "mist",
        "DU": "widespread dust",
        "FG": "fog",
        "FU": "smoke",
        "HZ": "haze",
        "PY": "spray",
        "SA": "sand",
        "VA": "volcanic ash",
        # Other
        "DS": "duststorm",
        "FC": "funnel clouds",
        "PO": "well-developed dust/sand whirls",
        "SQ": "squalls",
        "SS": "sandstorm"
    }

    def __init__(self, raw):
        m = re.search(
            r"(?P<intensity>(?:%(intensities)s))?(?P<descriptor>(?:%(descriptors)s))?(?P<phenomenon>(?:%(phenomena)s){1,3})?" %
            {
                "intensities": "|".join(WeatherGroup.INTENSITIES).replace("+", "\+").strip("|"),
                "descriptors": "|".join(WeatherGroup.DESCRIPTORS),
                "phenomena": "|".join(WeatherGroup.PHENOMENA)
            },
            raw
        )
        if not any(m.groups()):
            raise WeatherGroupDecodeException  # TODO: also raise if only intensity is set
        self.intensity = m.group("intensity") or ""  # "" is valid for moderate
        self.descriptor = m.group("descriptor")
        p = m.group("phenomenon")
        if p and len(p) > 2:
            self.phenomenon = tuple((p[0+i:2+i] for i in range(0, len(p), 2)))
        else:
            self.phenomenon = p

    def __str__(self):
        raw = self.intensity
        if self.descriptor:
            raw += self.descriptor
        if self.phenomenon:
            raw += "".join(self.phenomenon)
        return raw


class SkyCondition:

    TYPES = {
        "VV": "vertical visibility",
        "SKC": "clear",
        "CLR": "clear",
        "NCD": "no cloud detected",
        "FEW": "few",
        "SCT": "scattered",
        "BKN": "broken",
        "OVC": "overcast"
    }

    def __init__(self, raw):
        m = re.search(
                r"(?P<type>(?:%(types)s))(?P<height>\d{3})?" % {"types": "|".join(SkyCondition.TYPES)},
                raw
        )
        if not m:
            raise SkyConditionDecodeException
        self.type = m.group("type")
        self.height = m.group("height")

    def __str__(self):
        raw = self.type
        if self.height:
            raw += self.height
        return raw


class Temperature:
    """The temperature (and dew point) group"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<temperature>M?\d{1,2})/(?P<dew_point>M?\d{,2})", raw)
        if not m:
            # print("'%s'" % raw)  # TODO: remove this line
            raise TemperatureDecodeException
        self.temperature = m.group("temperature")
        self.dew_point = m.group("dew_point")

    def __str__(self):
        raw = self.temperature + "/"
        if self.dew_point:
            raw += self.dew_point
        return raw


class AltimeterSetting:

    def __init__(self, raw):
        m = re.search(r"(?P<indicator>[AQ])(?P<value>\d{4})", raw)
        if not m:
            raise AltimeterSettingDecodeException
        self.indicator = m.group("indicator")
        self.value = m.group("value")

    def __str__(self):
        return self.indicator + self.value


class Remarks:

    def __init__(self, raw):
        self.text = raw

    def __str__(self):
        return self.text
