from urllib.error import HTTPError
from urllib.request import urlopen
import aviation_weather
import aviation_weather.exceptions as exceptions


class Report(object):
    """The Report class represents a weather report.

    Attributes:
        type (MessageType): The specified type of the Report.
        location (Location): The location for which the report was produced.
        time (Time): The time date at which the report was produced.
        wind (Wind): The reported winds.
        visibility (Visibility): The reported visibility.
        runway_visual_range (tuple(RunwayVisualRange)): The reported runway visual ranges.
        weather_groups (tuple(WeatherGroup)): The reported weather groups.
        sky_conditions (tuple(SkyCondition)): The reported sky conditions.
        temperature (Temperature): The reported temperature and dew point.
        pressure (Pressure): The reported pressure.
        remarks (Remarks): The remarks made in the report.
    """
    # TODO: complete docstring above

    def __init__(self, raw):
        if " RMK " in raw:
            body, remarks = raw.split(" RMK ", 1)
            remarks = aviation_weather.Remarks("RMK " + remarks)  # re-add RMK so it gets parsed properly
        else:
            body, remarks = raw, None
        try:
            self._parse_body(body)
        except (exceptions.ComponentDecodeError, IndexError) as e:
            raise exceptions.ReportDecodeError("Report(%r) could not be parsed" % raw) from e
        self.remarks = remarks

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.raw)

    def __str__(self):
        return self.raw  # TODO: change to self.decoded (if and when it is implemented)

    @property
    def raw(self):
        raw = ""
        if self.type:
            raw += "%s " % self.type.raw
        if self.modifier:
            raw += "%s " % self.modifier
        raw += "%s " % self.location.raw
        raw += "%s " % self.time.raw
        raw += "%s " % self.wind.raw
        raw += "%s " % self.visibility.raw
        if self.runway_visual_range:
            for rvr in self.runway_visual_range:
                raw += "%s " % rvr.raw
        if self.weather_groups:
            for wg in self.weather_groups:
                raw += "%s " % wg.raw
        if self.sky_conditions:
            for sc in self.sky_conditions:
                raw += "%s " % sc.raw
        if self.temperature:
            raw += "%s " % self.temperature.raw
        if self.pressure:
            raw += "%s " % self.pressure.raw
        if self.remarks:
            raw += "%s " % self.remarks.raw
        if self._end:
            raw += "%s " % self._end.raw
        return raw.rstrip()

    def _parse_body(self, text):
        parts = text.split()
        if len(parts) == 0:
            raise exceptions.ReportDecodeError

        if parts[0] in ("METAR", "SPECI"):
            self.type = aviation_weather.MessageType(parts[0])
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

        self.location = aviation_weather.Location(parts[0])
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
        self._end = end

    @staticmethod
    def retrieve(code: str):
        """Retrieve a METAR from NOAA.

        Args:
            code (str): The station identifier for which a METAR should be retrieved.

        Returns:
            A Report object, or None if a METAR could not be found.
        """
        URL = "ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/%s.TXT"
        try:
            with urlopen(URL % code.upper()) as response:
                metar = response.read().decode('utf-8').splitlines()[1].strip()
                return Report(metar)
        except HTTPError:
            return None


class _Container(object):
    """A container for "unknown" elements within the Report."""

    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return "report._Container(%r)" % self.raw
