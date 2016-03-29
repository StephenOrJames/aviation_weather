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
            r"\b(?:(?P<less>M)?(?P<distance1>\d[ \d/]{,4})(?P<unit>SM)|(?P=less)?(?P<distance2>\d{4}))\b",
            raw
        )
        if not m:
            raise VisibilityDecodeError("Visibility(%s) could not be parsed" % raw)
        self.is_less_than = True if m.group("less") else False
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
        raw = "M" if self.is_less_than else ""

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
