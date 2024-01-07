from flask import Blueprint, Response, request, session, current_app
from werkzeug.exceptions import Unauthorized
from itsdangerous.serializer import BadSignature
from itsdangerous.url_safe import URLSafeSerializer

CsrfBp = Blueprint('csrf', __name__)

# This module implements CSRF protection
# See more information here:
#  * https://angular.io/guide/http-security-xsrf-protection
#  * https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html


def check_token(header_value: str, expected_value: str):
    """Checks the validity of a given CSRF token.
    This function must be called within a request context,
    the SECRET_KEY and CSRF_TOKEN_SALT configuration keys must be set on the current Flask app.

    :param header_value: The value of the CSRF token sent by the user in a header.
    :param expected_value: The used to serialize the token
    """
    s = URLSafeSerializer(current_app.config["SECRET_KEY"])

    try:
        value = s.loads(header_value, current_app.config["CSRF_TOKEN_SALT"])
    except BadSignature:
        session.clear()
        raise Unauthorized("Invalid CSRF Token")

    if value != expected_value:
        session.clear()
        raise Unauthorized("Invalid CSRF Token")


@CsrfBp.before_app_request
def check_csrf_token():
    # Skip CSRF token validation on non-mutating requests
    if request.method in ("GET", "HEAD"):
        return

    # Skip CSRF token validation if there is no session
    if "user_id" not in session and "session_id" not in session:
        return

    # If the session contains invalid data, we just clear it
    if "user_id" not in session or "session_id" not in session:
        session.clear()
        return

    xsrf_token_header = request.headers.get("X-XSRF-TOKEN", default=None)
    if xsrf_token_header is None:
        session.clear()
        raise Unauthorized("A CSRF token must be sent in the X-XSRF-TOKEN header")

    check_token(xsrf_token_header, session["session_id"])


@CsrfBp.after_app_request
def generate_csr_token(res: Response):
    if "user_id" in session and "session_id" in session:
        # If there is a session, we ensure there is a CSRF Token in the Cookie
        if "XSRF-TOKEN" not in request.cookies:
            s = URLSafeSerializer(current_app.config["SECRET_KEY"])
            token = s.dumps(session["session_id"], current_app.config["CSRF_TOKEN_SALT"])
            res.set_cookie("XSRF-TOKEN", value=str(token), samesite='Strict')
    else:
        # If there is no session, we ensure the cookie is cleaned up
        if "XSRF-TOKEN" in request.cookies:
            res.delete_cookie("XSRF-TOKEN", samesite='Strict')

    return res
