from urllib.error import HTTPError
from urllib.request import urlopen
import aviation_weather
import aviation_weather.exceptions as exceptions
from aviation_weather.exceptions import ReportDecodeError


class Report(object):

    def __init__(self, raw):
        if " RMK " in raw:
            body, remarks = raw.split(" RMK ", 1)
            remarks = aviation_weather.Remarks("RMK " + remarks)  # re-add RMK so it gets parsed properly
        else:
            body, remarks = raw, None
        self.body = self._parse_body(body)  # TODO: deprecate and eliminate self.body
        self.remarks = remarks

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.raw)

    def __str__(self):
        return self.raw  # TODO: change to self.decoded (if and when it is implemented)

    @property
    def raw(self):
        raw = " ".join((part.raw for part in self.body))
        if self.remarks:
            raw += " " + self.remarks.raw
        return raw

    def _parse_body(self, text):
        parts = text.split()
        if len(parts) == 0:
            raise exceptions.ReportDecodeError

        if parts[0] in ("METAR", "SPECI"):
            self.type = _Container(parts[0])
            parts = parts[1:]
        else:
            self.type = None

        if "AUTO" in parts:
            self.modifier = "AUTO"
        # elif "COR" in parts:
        #     self.modifier = "COR"
        else:
            self.modifier = None
        if self.modifier:
            parts.remove(self.modifier)

        self.station = aviation_weather.Station(parts[0])
        self.time = aviation_weather.Time(parts[1])

        try:
            self.wind = aviation_weather.Wind(text)
        except (exceptions.WindDecodeError, IndexError):
            self.wind = None
            parts = parts[2:]
        else:
            parts = " ".join(parts[2:]).split(self.wind.raw, 1)[1].split()  # remove used parts

        try:
            self.visibility = aviation_weather.Visibility(" ".join(parts[:2]))
        except (exceptions.VisibilityDecodeError, IndexError):
            self.visibility = None
        else:
            parts = text.split(self.visibility.raw, 1)[1].split()  # remove used parts

        t = list()
        i = 0
        try:
            while True:
                t.append(aviation_weather.RunwayVisualRange(parts[i]))
                i += 1
        except (exceptions.RunwayVisualRangeDecodeError, IndexError):
            parts = parts[i:]
        self.runway_visual_range = tuple(t) or None

        t = list()
        i = 0
        try:
            while True:
                t.append(aviation_weather.WeatherGroup(parts[i]))
                i += 1
        except (exceptions.WeatherGroupDecodeError, IndexError):
            parts = parts[i:]
        self.weather_groups = tuple(t) or None

        t = list()
        i = 0
        try:
            while True:
                t.append(aviation_weather.SkyCondition(parts[i]))
                i += 1
        except (exceptions.SkyConditionDecodeError, IndexError):
            parts = parts[i:]
        self.sky_conditions = tuple(t) or None

        try:
            self.temperature = aviation_weather.Temperature(parts[0])
        except (exceptions.TemperatureDecodeError, IndexError):
            self.temperature = None
        else:
            parts = parts[1:]

        try:
            self.pressure = aviation_weather.Pressure(parts[0])
        except (exceptions.PressureDecodeError, IndexError):
            self.pressure = None

        end = " ".join(parts[1:])
        if end:
            end = _Container(end)
        else:
            end = None

        body = [self.type, self.station, self.time, self.modifier, self.wind, self.visibility]
        unpack = [self.runway_visual_range, self.weather_groups, self.sky_conditions]
        for group in unpack:
            if group:
                body += list(group)
        body += [self.temperature, self.pressure, end]
        return list(filter(None, body))

    @staticmethod
    def retrieve(code):
        url = "http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT"
        try:
            with urlopen(url % code.upper()) as response:
                metar = response.read().decode('utf-8').splitlines()[1].strip()
                return Report(metar)
        except HTTPError:
            return None


class _Container(object):
    """Container for "unknown" elements within the report"""

    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return "report._Container(%r)" % self.raw
