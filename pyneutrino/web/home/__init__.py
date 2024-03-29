from werkzeug.exceptions import NotFound
from flask import Flask, Blueprint, render_template, current_app


HomeBp = Blueprint("home", __name__, url_prefix="")


# This is a catch-all route to work with angular navigation
# See here: https://flask.palletsprojects.com/en/3.0.x/patterns/singlepageapplications/
@HomeBp.route("/en-US/", defaults={"path": ""})
@HomeBp.route("/en-US/<path:path>")
def english_catch_all_route(path: str):
    if path.startswith("api/"):
        raise NotFound

    # Generate the absolute URL to this endpoint, to send to the JS
    base_url = current_app.url_for("home.english_catch_all_route", path="", _external=True)

    return render_template("home_en-US.html", base_url=base_url)


# This is the same, but with the fr-FR prefix for the french translation
@HomeBp.route("/fr-FR/", defaults={"path": ""})
@HomeBp.route("/fr-FR/<path:path>")
def french_catch_all_route(path: str):
    # Generate the absolute URL to this endpoint, to send to the JS
    base_url = current_app.url_for("home.french_catch_all_route", path="", _external=True)

    return render_template("home_fr-FR.html", base_url=base_url)


def register(app: Flask):
    app.register_blueprint(HomeBp)
