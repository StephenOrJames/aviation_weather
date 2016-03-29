from aviation_weather.components import Component
from aviation_weather.exceptions import RemarksDecodeError


class Remarks(Component):

    def __init__(self, raw):
        """Parse `raw` to create a new Remarks object.

        Args:
            raw (str): The remarks to be stored (not actually parsed at the moment).

        Raises:
            RemarksDecodeError: If `raw` could not be parsed.
        """
        if raw.startswith("RMK "):
            self.text = raw
        else:
            raise RemarksDecodeError("Remarks(%s) could not be parsed" % raw)

    @property
    def decoded(self):
        return ""  # We technically don't parse remarks.

    @property
    def raw(self):
        return self.text
