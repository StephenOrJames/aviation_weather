import re
from aviation_weather.exceptions import PressureDecodeException


class Pressure:

    def __init__(self, raw):
        m = re.search(r"\b(?P<indicator>[AQ])(?P<value>\d{4})\b", raw)
        if not m:
            raise PressureDecodeException
        self.indicator = m.group("indicator")
        value = m.group("value")
        if self.indicator == "A":
            self.value = int(value) / 100
        elif self.indicator == "Q":
            self.value = int(value)

    def __str__(self):
        if self.indicator == "A":
            return "A%d" % int(self.value * 100)
        elif self.indicator == "Q":
            return "Q%d" % self.value
