from aviation_weather.exceptions import RemarksDecodeException


class Remarks:

    def __init__(self, raw):
        if raw.startswith("RMK "):
            self.text = raw[4:]
        else:
            raise RemarksDecodeException

    def __str__(self):
        return "RMK " + self.text
