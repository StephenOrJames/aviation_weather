import json

from flask import jsonify
from flask.blueprints import Blueprint

import aviation_weather
from aviation_weather.exceptions import (
    ComponentDecodeError,
    ReportDecodeError,
    WeatherDecodeError
)
from flask.helpers import url_for


api = Blueprint("api", __name__)


COMPONENTS = {
    "pressure": aviation_weather.Pressure,
    "runwayvisualrange": aviation_weather.RunwayVisualRange,
    "skycondition": aviation_weather.SkyCondition,
    "temperature": aviation_weather.Temperature,
    "time": aviation_weather.Time,
    "visibility": aviation_weather.Visibility,
    "weathergroup": aviation_weather.WeatherGroup,
    "wind": aviation_weather.Wind,
    "windshear": aviation_weather.WindShear
}


def get_dict(obj):
    """
    Converts the input object to a JSON-serializable dictionary.
    :param obj: The object to be converted.
    :return: A JSON-serializable dictionary representing the input object.
    """

    def _generate_dict_with_raw(obj2):
        """
        Converts the input object into dictionary.
        :param obj2: The object to be converted.
        :return: A dictionary representation of the input object.
        """

        result2 = obj2.__dict__
        if hasattr(obj, "raw"):
            # raw is usually a property, so manually add it if it is available
            result2["raw"] = obj2.raw
        return result2

    result = json.loads(json.dumps(obj, default=_generate_dict_with_raw))
    return result


@api.route("/")
def index():
    return jsonify(
        error="API documentation is available at %s and a sandbox is available at %s" % (
            url_for("documentation"),
            url_for("sandbox")
        )
    )


@api.route("/retrieve/report")
@api.route("/retrieve/report/<location_identifier>")
def retrieve_report(location_identifier=None):
    if location_identifier is None:
        return jsonify(error="Location identifier required (GET {API-base-URL}/retrieve/report/<location_identifier>).")
    else:
        report = aviation_weather.Report.retrieve(location_identifier)
        if report is None:
            return jsonify(error="No report was found for the specified location.")
        else:
            return jsonify(**get_dict(report))


@api.route("/parse/component/<component>/<path:raw>")
def parse_component(component, raw):
    if component in COMPONENTS:
        try:
            c = COMPONENTS[component](raw)
        except ComponentDecodeError:
            return jsonify(error="Your %s component could not be decoded." % component)
        else:
            return jsonify(**get_dict(c))
    else:
        return jsonify(error="The component you specified is not currently supported by this API.")


@api.route("/parse/forecast/<path:raw>")
def parse_forecast(raw):
    try:
        forecast = aviation_weather.Forecast(raw)
    except WeatherDecodeError:
        return jsonify(error="Your forecast could not be decoded.")
    else:
        return jsonify(**get_dict(forecast))


@api.route("/parse/report/<path:raw>")
def parse_report(raw):
    try:
        report = aviation_weather.Report(raw)
    except ReportDecodeError:
        return jsonify(error="Your report could not be decoded.")
    else:
        return jsonify(**get_dict(report))
