import re
from aviation_weather.exceptions import WeatherGroupDecodeException


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
            r"(?P<intensity>(?:%(intensities)s))?"
            r"(?P<descriptor>(?:%(descriptors)s))?"
            r"(?P<phenomenon>(?:%(phenomena)s){1,3})?\b"
            %
            {
                "intensities": "|".join(WeatherGroup.INTENSITIES).replace("+", "\+").replace("||", "|").strip("|"),
                "descriptors": "|".join(WeatherGroup.DESCRIPTORS),
                "phenomena": "|".join(WeatherGroup.PHENOMENA)
            },
            raw
        )
        if not (m and (m.group("descriptor") or m.group("phenomenon"))):
            raise WeatherGroupDecodeException("WeatherGroup(%s) could not be parsed" % raw)
        self.intensity = m.group("intensity") or ""  # Empty string for moderate intensity
        self.descriptor = m.group("descriptor")
        p = m.group("phenomenon")
        if p and len(p) > 2:
            self.phenomenon = tuple((p[0 + i:2 + i] for i in range(0, len(p), 2)))
        else:
            self.phenomenon = p

    def __str__(self):
        raw = self.intensity
        if self.descriptor:
            raw += self.descriptor
        if self.phenomenon:
            raw += "".join(self.phenomenon)
        return raw
