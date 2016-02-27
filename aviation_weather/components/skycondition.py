import re
from aviation_weather.exceptions import SkyConditionDecodeException


class SkyCondition:

    TYPES = {
        "VV": "vertical visibility",
        "SKC": "clear",
        "CLR": "clear",
        "NCD": "no cloud detected",
        "FEW": "few",
        "SCT": "scattered",
        "BKN": "broken",
        "OVC": "overcast"
    }

    def __init__(self, raw):
        m = re.search(
            r"\b(?P<type>(?:%(types)s))(?P<height>\d{3})?(?P<cb>CB)?\b" % {"types": "|".join(SkyCondition.TYPES)},
            raw
        )
        if not m:
            raise SkyConditionDecodeException
        self.type = m.group("type")
        self.height = m.group("height")
        self.cumulonimbus = m.group("cb")

    def __str__(self):
        raw = self.type
        if self.height:
            raw += self.height
        if self.cumulonimbus:
            raw += "CB"
        return raw
