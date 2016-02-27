import re
from aviation_weather.exceptions import StationDecodeException


class Station:
    """Represents a weather station"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<id>[A-Z][A-Z0-9]{3})\b", raw.upper())
        if not m:
            raise StationDecodeException
        self.identifier = m.group("id")

    def __str__(self):
        return self.identifier
