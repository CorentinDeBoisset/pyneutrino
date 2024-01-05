from flask import Flask, Blueprint, render_template


HomeBp = Blueprint('home', __name__, url_prefix="")


# This is a catch-all route to work with angular navigation
# See here: https://flask.palletsprojects.com/en/3.0.x/patterns/singlepageapplications/
@HomeBp.route("/", defaults={"path": ""})
@HomeBp.route("/<path:path>")
def catch_all_route(path: str):
    return render_template("home.html")


def register(app: Flask):
    app.register_blueprint(HomeBp)
