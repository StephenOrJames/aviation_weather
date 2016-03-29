import re

from aviation_weather.components import Component
from aviation_weather.exceptions import TemperatureDecodeError


class Temperature(Component):
    """The temperature and dew point group

    Attributes:
        temperature (int): The temperature in whole degrees Celcius.
        dew_point (int): The dew point in whole degrees Celcius.
    """

    def __init__(self, raw: str):
        """Parse `raw` to create a new Temperature object.

        Args:
            raw (str): The

        Raises:
            TemperatureDecodeError: If the input could not be parsed.
        """
        m = re.search(r"\b(?P<temperature>M?\d{1,2})/(?P<dew_point>M?\d{1,2})?\b", raw)
        if not m:
            raise TemperatureDecodeError("Temperature(%s) could not be parsed" % raw)
        temperature = m.group("temperature")
        dew_point = m.group("dew_point")
        if temperature.startswith("M"):
            self.temperature = -int(temperature[1:])
        else:
            self.temperature = int(temperature)
        if dew_point.startswith("M"):
            self.dew_point = -int(dew_point[1:])
        else:
            self.dew_point = int(dew_point)

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
