# Flask modules
from flask import (
    render_template,
    Blueprint,
)


pages_bp = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages_bp.route("/")
def home_page():
    return render_template("home.html")
