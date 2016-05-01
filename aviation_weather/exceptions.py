class WeatherDecodeError(ValueError):
    """Weather could not be decoded"""
    pass


class ReportDecodeError(WeatherDecodeError):
    """Report could not be decoded"""
    pass


class ComponentDecodeError(WeatherDecodeError):
    """Weather component could not be decoded"""
    pass


class PressureDecodeError(ComponentDecodeError):
    """Pressure could not be decoded"""
    pass


class RemarksDecodeError(ComponentDecodeError):
    """Remarks could not be decoded"""
    pass


class RunwayVisualRangeDecodeError(ComponentDecodeError):
    """Runway visual range could not be decoded"""
    pass


class SkyConditionDecodeError(ComponentDecodeError):
    """Sky condition could not be decoded"""
    pass


class LocationDecodeError(ComponentDecodeError):
    """Location could not be decoded"""
    pass


class TemperatureDecodeError(ComponentDecodeError):
    """Temperature and dew point could not be decoded"""
    pass


class TimeDecodeError(ComponentDecodeError):
    """Time could not be decoded"""
    pass


class VisibilityDecodeError(ComponentDecodeError):
    """Visibility could not be decoded"""
    pass


class WeatherGroupDecodeError(ComponentDecodeError):
    """Weather group could not be decoded"""
    pass


class WindDecodeError(ComponentDecodeError):
    """Wind could not be decoded"""
    pass


class ForecastGroupDecodeError(ComponentDecodeError):
    """Forecast group could not be decoded"""
    pass


class BecomingGroupDecodeError(ForecastGroupDecodeError):
    """BECMG group could not be decoded"""
    pass


class FromGroupDecodeError(ForecastGroupDecodeError):
    """FM group could not be decoded"""
    pass


class ProbabilityGroupDecodeError(ForecastGroupDecodeError):
    """PROB group could not be decoded"""
    pass


class TemporaryGroupDecodeError(ForecastGroupDecodeError):
    """TEMPO group could not be decoded"""
    pass
