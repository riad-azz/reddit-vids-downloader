# Flask modules
from flask import current_app, request
from flask_assets import Environment, Bundle

# Other modules
import os
import shutil

assets = Environment(current_app)
assets.cache = True
assets.url = current_app.static_url_path
assets.directory = current_app.static_folder

# CSS BUNDLES
assets.register(
    "css_all",
    Bundle(
        "css/main.css",
        "css/style.css",
        output="gen/style.css",
        filters="cssmin",
    ),
)

# JAVASCRIPT BUNDLES
assets.register(
    "js_head",
    Bundle(
        "js/theme.js",
        output="gen/head.js",
        filters="jsmin",
    ),
)

assets.register(
    "js_defer",
    Bundle(
        "js/main.js",
        output="gen/defer.js",
        filters="jsmin",
    ),
)

assets.register(
    "reddit_script",
    Bundle(
        "js/reddit-script.js",
        output="gen/reddit-script.js",
        filters="jsmin",
    ),
)

# CLEAR FLASK-ASSETS CACHE
CACHE_DIR = os.path.join(current_app.static_folder, ".webassets-cache")
if os.path.exists(CACHE_DIR):
    shutil.rmtree(CACHE_DIR)


# CACHE STATIC FILES
@current_app.after_request
def add_cache_header(response):
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000"
    return response
