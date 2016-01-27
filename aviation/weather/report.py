from urllib.error import HTTPError
from urllib.request import urlopen
from .weather import *


class Report:
    def __init__(self, raw):
        if " RMK " in raw:
            body, remarks = raw.split(" RMK ", 1)
        else:
            body, remarks = raw, None
        self.body = self._parse_body(body)
        self.remarks = self._parse_remarks(remarks)

    def __str__(self):
        raw = " ".join((str(part) for part in self.body))
        if self.remarks:
            raw += " RMK " + " ".join((str(part) for part in self.remarks))
        return raw

    def _parse_body(self, text):
        parts = text.split()
        if len(parts) == 0:
            raise ReportDecodeException

        if parts[0] in ("METAR", "SPECI"):
            self.type = parts[0]
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

        self.station = Station(parts[0])
        self.time = Time(parts[1])

        try:
            self.wind = Wind(text)
        except (WindDecodeException, IndexError):
            self.wind = None
            parts = parts[2:]
        else:
            parts = " ".join(parts[2:]).split(str(self.wind), 1)[1].split()  # remove used parts

        try:
            self.visibility = Visibility(" ".join(parts[:2]))
        except (VisibilityDecodeException, IndexError):
            self.visibility = None
        else:
            parts = text.split(str(self.visibility), 1)[1].split()  # remove used parts

        t = list()
        i = 0
        try:
            while True:
                t.append(RunwayVisualRange(parts[i]))
                i += 1
        except (RunwayVisualRangeDecodeException, IndexError):
            parts = parts[i:]
        self.runway_visual_range = tuple(t)

        t = list()
        i = 0
        try:
            while True:
                t.append(WeatherGroup(parts[i]))
                i += 1
        except (WeatherGroupDecodeException, IndexError):
            parts = parts[i:]
        self.weather_groups = tuple(t)

        t = list()
        i = 0
        try:
            while True:
                t.append(SkyCondition(parts[i]))
                i += 1
        except (SkyConditionDecodeException, IndexError):
            parts = parts[i:]
        self.sky_conditions = tuple(t)

        try:
            self.temperature = Temperature(parts[0])
        except (TemperatureDecodeException, IndexError):
            self.temperature = None
        else:
            parts = parts[1:]

        try:
            self.altimeter_setting = Pressure(parts[0])
        except (PressureDecodeException, IndexError):
            self.altimeter_setting = None

        body = [self.type, self.station, self.time, self.modifier, self.wind, self.visibility,
                *self.runway_visual_range, *self.weather_groups, *self.sky_conditions, self.temperature,
                self.altimeter_setting, " ".join(parts[1:])]
        return list(filter(None, body))

    def _parse_remarks(self, text):
        if not text:
            return []
        else:
            return [Remarks(text)]  # TODO: consider more detail from remarks?

    @staticmethod
    def retrieve(code):
        url = "http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT"
        try:
            with urlopen(url % code.upper()) as response:
                metar = response.read().decode('utf-8').splitlines()[1].strip()
                return Report(metar)
        except HTTPError:
            return None
