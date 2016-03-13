import re
from aviation_weather.exceptions import RunwayVisualRangeDecodeException


class RunwayVisualRange:
    """Represents the runway visual range"""

    def __init__(self, raw):
        m = re.search(
            r"\bR(?P<runway>\d{2}[LRC]?)/(?P<d_min>[PM]?\d{4})"
            r"(?:V(?P<d_max>[PM]?\d{4}))?(?P<unit>FT)?(?P<trend>[UND])?\b",
            raw
        )
        if not m:
            raise RunwayVisualRangeDecodeException("RunwayVisualRange(%s) could not be parsed" % raw)
        self.runway = m.group("runway")
        if m.group("d_max"):
            self.distance = (m.group("d_min"), m.group("d_max"))
        else:
            self.distance = m.group("d_min")
        self.unit = m.group("unit") or "m"
        self.trend = m.group("trend")

    def __str__(self):
        raw = "R" + self.runway + "/"
        if isinstance(self.distance, tuple):
            raw += "V".join(self.distance)
        else:
            raw += self.distance
        if self.unit != "m":
            raw += self.unit
        if self.trend:
            raw += self.trend
        return raw
