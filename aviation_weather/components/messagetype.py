from aviation_weather.components import Component
from aviation_weather.exceptions import MessageTypeDecodeError


class MessageType(Component):

    TYPES = {
        "METAR": "meteorological aerodrome report",
        "SPECI": "special report",
        "TAF": "terminal aerodrome forecast",
        "TAF AMD": "terminal aerodrome forecast (amended)"
    }

    def __init__(self, raw):
        if raw in MessageType.TYPES:
            self.text = raw
        else:
            raise MessageTypeDecodeError("MessageType(%r) could not be parsed" % raw)

    @property
    def raw(self):
        return self.text
