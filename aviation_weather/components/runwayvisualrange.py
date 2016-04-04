import re

from aviation_weather.components import Component
from aviation_weather.exceptions import RunwayVisualRangeDecodeError


class RunwayVisualRange(Component):
    """Represents the runway visual range"""

    def __init__(self, raw):
        """Parse `raw` to create a new RunwayVisualRange object.

        Args:
            raw (str): The runway visual range to be parsed.

        Raises:
            RunwayVisualRangeDecodeError: If `raw` could not be parsed.
        """
        m = re.search(
            r"\bR(?P<runway>\d{2}[LRC]?)/(?P<d_min>[PM]?\d{4})"
            r"(?:V(?P<d_max>[PM]?\d{4}))?(?P<unit>FT)?(?P<trend>[UND])?\b",
            raw
        )
        if not m:
            raise RunwayVisualRangeDecodeError("RunwayVisualRange(%r) could not be parsed" % raw)
        self.runway = m.group("runway")
        if m.group("d_max"):
            self.distance = (m.group("d_min"), m.group("d_max"))
        else:
            self.distance = m.group("d_min")
        self.unit = m.group("unit") or "m"
        self.trend = m.group("trend")

    @property
    def raw(self):
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
