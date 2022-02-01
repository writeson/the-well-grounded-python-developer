from flask import render_template
from logging import getLogger
from . import intro_bp
from flask_login import login_required
from ..decorators import authorization_required
from ..models import Role

logger = getLogger(__file__)


@intro_bp.get("/")
def home():
    logger.debug("rendering home page")
    return render_template("index.html")


@intro_bp.get("/about")
def about():
    logger.debug("rendering about page")
    return render_template("about.html")


@intro_bp.get("/auth_required")
@login_required
def auth_required():
    return render_template("auth_required.html")


@intro_bp.get("/admin_required")
@login_required
@authorization_required(Role.Permissions.ADMINISTRATOR)
def admin_required():
    return render_template("admin_required.html")
