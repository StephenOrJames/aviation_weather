import re
from aviation_weather.exceptions import WindDecodeException


class Wind:
    # TODO: support conversion from KT to MPS (and vice versa)?

    def __init__(self, raw):
        m = re.search(
            r"\b(?P<direction>(?:\d{3}|VRB))(?P<speed>\d{2,3})(?:G(?P<gusts>\d{2,3}))?(?P<unit>(?:KT|MPS))"
            r"(?: (?P<v_from>\d{3})V(?P<v_to>\d{3}))?\b",
            raw
        )
        if not m:
            raise WindDecodeException
        self.direction = m.group("direction")
        self.speed = m.group("speed")
        self.gusts = m.group("gusts")
        self.unit = m.group("unit")
        self.variable = (m.group("v_from"), m.group("v_to"))

    def __str__(self):
        raw = self.direction + self.speed
        if self.gusts:
            raw += "G" + self.gusts
        raw += self.unit
        if all(self.variable):
            raw += " " + self.variable[0] + "V" + self.variable[1]
        return raw
