import re

from aviation_weather.components import Component
from aviation_weather.exceptions import SkyConditionDecodeError


class SkyCondition(Component):

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
        """Parse `raw` to create a new SkyCondition object.

        Args:
            raw (str): The sky condition to be parsed.

        Raises:
            SkyConditionDecodeError: If `raw` could not be parsed.
        """
        m = re.search(
            r"\b(?P<type>(?:%(types)s))(?P<height>\d{3})?(?P<cb_tcu>CB|TCU)?\b" % {"types": "|".join(SkyCondition.TYPES)},
            raw
        )
        if not m:
            raise SkyConditionDecodeError("SkyCondition(%r) could not be parsed" % raw)
        self.type = m.group("type")
        self.height = m.group("height")
        if self.height:
            self.height = int(m.group("height")) * 100
        self.cumulonimbus = m.group("cb_tcu") == "CB"
        self.towering_cumulus = m.group("cb_tcu") == "TCU"

    @property
    def raw(self):
        raw = self.type
        if self.height:
            raw += "%03d" % (self.height // 100)
        if self.cumulonimbus:
            raw += "CB"
        if self.towering_cumulus:
            raw += "TCU"
        return raw
