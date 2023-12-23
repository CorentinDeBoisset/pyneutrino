from flask import Blueprint

LoginBp = Blueprint('responder', __name__, url_prefix="/auth")

@LoginBp.route("/login")
def login():
        return "All right"

@LoginBp.route("/logout")
def logout():
        return "Ok"
