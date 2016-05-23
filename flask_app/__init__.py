from flask.app import Flask
from flask.templating import render_template

from . import api


app = Flask(__name__)


@app.route("/")
def documentation():
    return render_template("documentation.html")


@app.route("/sandbox")
def sandbox():
    return render_template("sandbox.html", components=list(sorted(api.COMPONENTS.keys())))


app.register_blueprint(api.api, url_prefix="/api")
