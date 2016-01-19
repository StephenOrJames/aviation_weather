class DecodeException(Exception):
    """Something could not be decoded"""
    pass


class ReportDecodeException(DecodeException):
    """Report could not be decoded"""
    pass


class WeatherDecodeException(DecodeException):
    """Weather could not be decoded"""
    pass


class WindDecodeException(WeatherDecodeException):
    """Wind could not be decoded"""
    pass


class VisibilityDecodeException(WeatherDecodeException):
    """Visibility could not be decoded"""
    pass


class RunwayVisualRangeDecodeException(WeatherDecodeException):
    """Runway visual range could not be decoded"""
    pass


class WeatherGroupDecodeException(WeatherDecodeException):
    """Weather group could not be decoded"""
    pass


class SkyConditionDecodeException(WeatherDecodeException):
    """Sky condition could not be decoded"""
    pass


class TemperatureDecodeException(WeatherDecodeException):
    """Temperature and dew point could not be decoded"""
    pass


class AltimeterSettingDecodeException(WeatherDecodeException):
    """Altimeter setting (QNH) could not be decoded"""
    pass
