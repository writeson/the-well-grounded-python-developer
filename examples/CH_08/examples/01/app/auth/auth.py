from logging import getLogger
from flask import render_template, redirect, url_for, request, flash
from . import auth_bp
from .. models import db_session_manager, User
from .. import login_manager
from .forms import LoginForm
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse


logger = getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    with db_session_manager(session_close=False) as db_session:
        return db_session.get(User, user_id)


@auth_bp.get("/login")
@auth_bp.post("/login")
def login():
    """Determine if the user can login or not with the
    form credentials

    Returns:
        text: Either the login form or the requested destination HTML
    """
    form = LoginForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = (
                db_session
                .query(User)
                .filter(User.email == form.email.data)
                .one_or_none()
            )
            if user is None or not user.verify_password(form.password.data):
                flash("Invalid email or password", "warning")
                return redirect(url_for("auth_bp.login"))
            login_user(user, remember=form.remember_me.data)
            next = request.args.get("next")
            if not next or url_parse(next).netloc != "":
                next = url_for("intro_bp.home")
            return redirect(next)
    return render_template("login.html", form=form)


@auth_bp.get("/logout")
def logout():
    """Log the current user out of the system

    Returns:
        redirect: Redirects to the home page
    """
    logout_user()
    flash("You've been logged out", "light")
    return redirect(url_for("intro_bp.home"))
