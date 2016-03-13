from aviation_weather.exceptions import RemarksDecodeError


class Remarks:

    def __init__(self, raw):
        if raw.startswith("RMK "):
            self.text = raw
        else:
            raise RemarksDecodeError("Remarks(%s) could not be parsed" % raw)

    def __str__(self):
        return self.text
