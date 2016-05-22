from flask.app import Flask
from flask.templating import render_template

from .api import api


app = Flask(__name__)


@app.route("/")
def documentation():
    return render_template("documentation.html")


app.register_blueprint(api, url_prefix="/api")
