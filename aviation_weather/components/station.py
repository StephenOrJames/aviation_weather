import re

from aviation_weather.components import _Component
from aviation_weather.exceptions import StationDecodeError


class Station(_Component):
    """Represents a weather station"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<id>[A-Z][A-Z0-9]{3})\b", raw.upper())
        if not m:
            raise StationDecodeError("Station(%s) could not be parsed" % raw)
        self.identifier = m.group("id")

    @property
    def raw(self):
        return self.identifier
