import re
import aviation_weather
from aviation_weather import exceptions


class Forecast(object):
    """The Forecast class represents a weather forecast.

    Attributes:
        type (MessageType): The type of forecast (e.g. 'TAF' or 'TAF AMD').
        location (Location): The location associated with the forecast.
        time (Time): The issuance time of the forecast.
        valid_period (str): The time period for which the forecast is valid.
        wind (Wind): The forecast winds.
        visibility (Visibility): The forecast prevailing visibility.
        weather_groups (tuple(WeatherGroup)): The forecast weather groups.
        sky_conditions (tuple(SkyConditions)): The forecast sky conditions.
        wind_shear (WindShear): The forecast wind shear.
        changes (list(ChangeGroup)): A list of the change groups (BECMG, FM, PROB, or TEMPO).
    """

    def __init__(self, raw):
        parts = re.split(r"\s(?=(?:BECMG|FM\d{6}|PROB\d{2}|TEMPO)\s)", raw)  # separate the major parts

        part = parts[0]
        t = re.match(r"TAF(?: AMD)?\s+", raw)
        if t is None:
            self.type = None
            r = part.split()
        else:
            tg = t.group()
            self.type = aviation_weather.MessageType(tg.rstrip())
            r = part.lstrip(tg).split()

        self.location = aviation_weather.Location(r[0])
        self.time = aviation_weather.Time(r[1])
        self.valid_period = tuple(aviation_weather.Time("%s00Z" % period) for period in r[2].split("/"))
        self.wind = aviation_weather.Wind(r[3])
        self.visibility = aviation_weather.Visibility(r[4])

        # Weather groups
        t = list()
        i = 5
        try:
            while True:
                t.append(aviation_weather.WeatherGroup(r[i]))
                i += 1
        except (exceptions.WeatherGroupDecodeError, IndexError):
            r = r[i:]
        self.weather_groups = tuple(t)

        # Sky conditions
        t = list()
        i = 0
        try:
            while True:
                t.append(aviation_weather.SkyCondition(r[i]))
                i += 1
        except (exceptions.SkyConditionDecodeError, IndexError):
            r = r[i:]
        self.sky_conditions = tuple(t)

        if r:
            self.wind_shear = aviation_weather.WindShear(r[0])
        else:
            self.wind_shear = None

        # Changes
        self.changes = list()
        for part in parts[1:]:
            if part.startswith("BECMG"):
                p = aviation_weather.BecomingGroup(part)
            elif part.startswith("FM"):
                p = aviation_weather.FromGroup(part)
            elif part.startswith("PROB"):
                p = aviation_weather.ProbabilityGroup(part)
            elif part.startswith("TEMPO"):
                p = aviation_weather.TemporaryGroup(part)
            else:
                p = None
            if p:
                self.changes.append(p)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.raw)

    def __str__(self):
        return self.raw  # TODO: change to self.decoded (if and when it is implemented)

    @property
    def raw(self):
        raw = ""
        if self.type:
            raw += " %s" % self.type.raw
        raw += " %s" % self.location.raw
        raw += " %s" % self.time.raw
        raw += " %s/%s" % (self.valid_period[0].raw[:-3], self.valid_period[1].raw[:-3])
        raw += " %s" % self.wind.raw
        raw += " %s" % self.visibility.raw
        for weather_group in self.weather_groups:
            raw += " %s" % weather_group.raw
        for sky_condition in self.sky_conditions:
            raw += " %s" % sky_condition.raw
        if self.wind_shear:
            raw += " %s" % self.wind_shear.raw
        for change in self.changes:
            raw += " %s" % change.raw

        return raw[1:]
