import re
from aviation_weather.exceptions import TemperatureDecodeException


class Temperature:
    """The temperature (and dew point) group"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<temperature>M?\d{1,2})/(?P<dew_point>M?\d{1,2})?\b", raw)
        if not m:
            raise TemperatureDecodeException
        self.temperature = m.group("temperature")
        self.dew_point = m.group("dew_point")

    def __str__(self):
        raw = self.temperature + "/"
        if self.dew_point:
            raw += self.dew_point
        return raw
