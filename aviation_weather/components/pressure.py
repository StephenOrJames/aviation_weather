import re
from aviation_weather.exceptions import PressureDecodeException


class Pressure:

    def __init__(self, raw):
        m = re.search(r"\b(?P<indicator>[AQ])(?P<value>\d{4})\b", raw)
        if not m:
            raise PressureDecodeException
        self.indicator = m.group("indicator")
        self.value = m.group("value")

    def __str__(self):
        return self.indicator + self.value
