from flask import Blueprint

# create the auth_pb Blueprint instance
content_bp = Blueprint(
    "content_bp", __name__,
    static_folder="static",
    static_url_path="/content/static",
    template_folder="templates"
)

from . import content
