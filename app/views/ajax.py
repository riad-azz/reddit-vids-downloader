# Flask modules
from flask import (
    abort,
    request,
    make_response,
    Blueprint,
    send_from_directory,
    url_for,
)

# App modules
from app.utils import json_response
from app.utils import get_video_path, valid_reddit_post

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.app_errorhandler(500)
def server_error(error):
    return json_response({"error": "500 Internal server error"})


@ajax_bp.route("/download", methods=["POST"])
async def download_reddit_video():
    url = request.args.get("url")
    if not url:
        return json_response({"error": "No reddit post url was provided"}, 400)

    try:
        media_path = await get_video_path(url)
    except Exception as e:
        return json_response({"error": str(e)}, 500)

    media_url = url_for("views.media.media_url", filename=media_path)
    return json_response({"media": media_url}, 200)


@ajax_bp.route("/set-theme", methods=["POST"])
def set_theme():
    theme = request.args.get("theme", "empty")
    allowed_themes = ("dark", "light")
    if theme.lower() not in allowed_themes:
        return abort(400, "Invalid theme")
    response = make_response("Theme set to " + theme)
    max_age = 86400  # 1 day
    response.set_cookie("theme", value=theme, max_age=max_age)
    return response
