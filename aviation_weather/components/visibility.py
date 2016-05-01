import re
from fractions import Fraction

from aviation_weather.components import Component
from aviation_weather.exceptions import VisibilityDecodeError


class Visibility(Component):

    def __init__(self, raw):
        """Parse `raw` to create a new Visibility object.

        Args:
            raw (str): The visibility to be parsed.

        Raises:
            VisibilityDecodeError: If `raw` could not be parsed.
        """
        m = re.search(
            r"\b(?:(?P<lt_gt>[MP])?(?P<distance1>\d[ \d/]{,4})(?P<unit>SM)|(?P=lt_gt)?(?P<distance2>\d{4}))\b",
            raw
        )
        if not m:
            raise VisibilityDecodeError("Visibility(%r) could not be parsed" % raw)
        self.less_than = m.group("lt_gt") == "M"
        self.greater_than = m.group("lt_gt") == "P"
        distance = m.group("distance1") or m.group("distance2")
        self.unit = m.group("unit") or "m"

        if "/" in distance:
            parts = distance.split(" ", 1)
            if len(parts) == 1:
                self.distance = float(Fraction(parts[0]))
            else:
                self.distance = int(parts[0]) + float(Fraction(parts[1]))
        else:
            self.distance = int(distance)

    @property
    def raw(self):
        if self.less_than:
            raw = "M"
        elif self.greater_than:
            raw = "P"
        else:
            raw = ""

        whole = self.distance // 1
        fraction = Fraction(self.distance % 1)
        if whole and fraction:
            raw += "%d %s" % (whole, fraction)
        elif whole:
            raw += str(whole)
        elif fraction:
            raw += str(fraction)
        else:
            raw += "0"

        if self.unit != "m":
            raw += self.unit
        return raw
