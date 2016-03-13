import re

from aviation_weather.components import _Component
from aviation_weather.exceptions import PressureDecodeError


class Pressure(_Component):
    """Represents pressure in either inches of mercury or hectopascals/millibars"""

    def __init__(self, raw):
        m = re.search(r"\b(?P<indicator>[AQ])(?P<value>\d{4})\b", raw)
        if not m:
            raise PressureDecodeError("Pressure(%s) could not be parsed" % raw)
        self.indicator = m.group("indicator")
        value = m.group("value")
        if self.indicator == "A":
            self.value = int(value) / 100
        elif self.indicator == "Q":
            self.value = int(value)
        else:
            raise PressureDecodeError("Pressure(%s) contains an invalid indicator" % raw)

    @property
    def raw(self):
        if self.indicator == "A":
            return "A%d" % int(self.value * 100)
        elif self.indicator == "Q":
            return "Q%d" % self.value
