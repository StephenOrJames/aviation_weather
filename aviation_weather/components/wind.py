import re

from aviation_weather.components import Component
from aviation_weather.exceptions import WindDecodeError


class Wind(Component):
    # TODO: support conversion from KT to MPS (and vice versa)?

    def __init__(self, raw):
        m = re.search(
            r"\b(?P<direction>(?:\d{3}|VRB))(?P<speed>\d{2,3})(?:G(?P<gusts>\d{2,3}))?(?P<unit>(?:KT|MPS))"
            r"(?: (?P<v_from>\d{3})V(?P<v_to>\d{3}))?\b",
            raw
        )
        if not m:
            raise WindDecodeError("Wind(%s) could not be parsed" % raw)
        self.direction = m.group("direction")
        if self.direction != "VRB":
            self.direction = int(self.direction)
        self.speed = int(m.group("speed"))
        self.gusts = m.group("gusts")
        if self.gusts:
            self.gusts = int(self.gusts)
        self.unit = m.group("unit")
        self.variable = (m.group("v_from"), m.group("v_to"))
        if self.variable == (None, None):
            self.variable = None
        else:
            self.variable = (int(m.group("v_from")), int(m.group("v_to")))

    @property
    def raw(self):
        if isinstance(self.direction, int):
            raw = "%03d" % self.direction
        else:
            raw = self.direction
        raw += "%02d" % self.speed
        if self.gusts is not None:
            raw += "G%02d" % self.gusts
        raw += self.unit
        if self.variable:
            raw += " %03dV%03d" % self.variable
        return raw
