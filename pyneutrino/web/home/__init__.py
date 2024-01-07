from werkzeug.exceptions import NotFound
from flask import Flask, Blueprint, render_template, current_app


HomeBp = Blueprint('home', __name__, url_prefix="")


# This is a catch-all route to work with angular navigation
# See here: https://flask.palletsprojects.com/en/3.0.x/patterns/singlepageapplications/
@HomeBp.route("/", defaults={"path": ""})
@HomeBp.route("/<path:path>")
def catch_all_route(path: str):
    if path.startswith("api/"):
        raise NotFound

    # Generate the absolute URL to this endpoint, to send to the JS
    base_url = current_app.url_for("home.catch_all_route", path="", _external=True)

    return render_template("home.html", base_url=base_url)


def register(app: Flask):
    app.register_blueprint(HomeBp)
