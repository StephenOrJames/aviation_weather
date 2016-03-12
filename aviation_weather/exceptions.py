class WeatherDecodeException(Exception):
    """Weather could not be decoded"""
    pass


class ReportDecodeException(WeatherDecodeException):
    """Report could not be decoded"""
    pass


class ComponentDecodeException(WeatherDecodeException):
    """Weather component could not be decoded"""
    pass


class PressureDecodeException(ComponentDecodeException):
    """Pressure could not be decoded"""
    pass


class RemarksDecodeException(ComponentDecodeException):
    """Remarks could not be decoded"""
    pass


class RunwayVisualRangeDecodeException(ComponentDecodeException):
    """Runway visual range could not be decoded"""
    pass


class SkyConditionDecodeException(ComponentDecodeException):
    """Sky condition could not be decoded"""
    pass


class StationDecodeException(ComponentDecodeException):
    """Weather station could not be decoded"""
    pass


class TemperatureDecodeException(ComponentDecodeException):
    """Temperature and dew point could not be decoded"""
    pass


class TimeDecodeException(ComponentDecodeException):
    """Time could not be decoded"""
    pass


class VisibilityDecodeException(ComponentDecodeException):
    """Visibility could not be decoded"""
    pass


class WeatherGroupDecodeException(ComponentDecodeException):
    """Weather group could not be decoded"""
    pass


class WindDecodeException(ComponentDecodeException):
    """Wind could not be decoded"""
    pass
