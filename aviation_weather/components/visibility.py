import re
from aviation_weather.exceptions import VisibilityDecodeException


class Visibility:

    def __init__(self, raw):
        m = re.search(
            r"\b(?:(?P<less>M)?(?P<distance1>\d[ \d/]{,4})(?P<unit>SM)|(?P=less)?(?P<distance2>\d{4}))\b",
            raw
        )
        if not m:
            raise VisibilityDecodeException
        self.less_than = True if m.group("less") else False
        self.distance = m.group("distance1") or m.group("distance2")
        self.unit = m.group("unit")

    def __str__(self):
        raw = "M" if self.less_than else ""
        raw += self.distance
        if self.unit:
            raw += self.unit
        return raw
