import re

from aviation_weather.components import Component
from aviation_weather.components.wind import Wind
from aviation_weather.exceptions import WindShearDecodeError, WindDecodeError


class WindShear(Component):

    def __init__(self, raw):
        """Parse `raw` to create a new WindShear object.

        Args:
            raw (str): The wind shear to be parsed.

        Raises:
            WindShearDecodeError: If `raw` could not be parsed.
        """

        m = re.search(r"\bWS(?P<altitude>\d{3})/(?P<wind>.+)\b", raw)

        if not m:
            raise WindShearDecodeError("WindShear(%r) could not be parsed" % raw)

        self.altitude = int(m.group("altitude")) * 100

        try:
            self.wind = Wind(m.group("wind"))
        except WindDecodeError as e:
            raise WindShearDecodeError("WindShear(%r) could not be parsed" % raw) from e

    @property
    def raw(self):
        return "WS%(altitude)03d/%(wind)s" % {
            "altitude": self.altitude // 100,
            "wind": self.wind.raw
        }
