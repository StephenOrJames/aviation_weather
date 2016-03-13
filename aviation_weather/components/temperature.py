import re

from aviation_weather.components import _Component
from aviation_weather.exceptions import TemperatureDecodeError


class Temperature(_Component):
    """The temperature (and dew point) group"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<temperature>M?\d{1,2})/(?P<dew_point>M?\d{1,2})?\b", raw)
        if not m:
            raise TemperatureDecodeError("Temperature(%s) could not be parsed" % raw)
        self.temperature = m.group("temperature")
        self.dew_point = m.group("dew_point")
        if self.temperature.startswith("M"):
            self.temperature = -int(self.temperature[1:])
        else:
            self.temperature = int(self.temperature)
        if self.dew_point.startswith("M"):
            self.dew_point = -int(self.dew_point[1:])
        else:
            self.dew_point = int(self.dew_point)

    @property
    def raw(self):
        raw = ""
        if self.temperature < 0:
            raw += "M%02d/" % -self.temperature
        else:
            raw += "%02d/" % self.temperature
        if self.dew_point is not None:
            if self.dew_point < 0:
                raw += "M%02d" % -self.dew_point
            else:
                raw += "%02d" % self.dew_point
        return raw
