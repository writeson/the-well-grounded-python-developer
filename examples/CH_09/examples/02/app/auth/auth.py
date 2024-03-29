from logging import getLogger

from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse

from .. import login_manager
from ..emailer import send_mail
from ..models import User, db_session_manager
from . import auth_bp
from .forms import (LoginForm, RegisterNewUserForm, RequestResetPasswordForm,
                    ResendConfirmationForm, ResetPasswordForm, UserProfileForm)

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


@auth_bp.get("/register_new_user")
@auth_bp.post("/register_new_user")
def register_new_user():
    if current_user.is_authenticated:
        return redirect(url_for("intro_bp.home"))
    form = RegisterNewUserForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
            )
            db_session.add(user)
            db_session.commit()
            send_confirmation_email(user)
            timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
            flash((
                "Please click on the confirmation link just sent "
                f"to your email address within {timeout} hours "
                "to complete your registration"
            ))
            logger.debug(f"new user {form.email.data} added")
            return redirect(url_for("intro_bp.home"))
    return render_template("register_new_user.html", form=form)


@auth_bp.get("/logout")
def logout():
    """Log the current user out of the system

    Returns:
        redirect: Redirects to the home page
    """
    logout_user()
    flash("You've been logged out", "light")
    return redirect(url_for("intro_bp.home"))


@auth_bp.get("/confirm/<confirmation_token>")
@login_required
def confirm(confirmation_token):
    if current_user.confirmed:
        return redirect(url_for("intro_bp.home"))
    try:
        # is the confirmation token confirmed?
        if current_user.confirm_token(confirmation_token):
            with db_session_manager() as db_session:
                current_user.confirmation = True
                db_session.add(current_user)
                db_session.commit()
                flash("Thank you for confirming your account")
    # confirmation token bad or expired
    except Exception as e:
        logger.exception(e)
        flash(e.message)
        return redirect(url_for("auth_bp.resend_confirmation"))
    return redirect(url_for("intro_bp.home"))


@auth_bp.get("/resend_confirmation")
@auth_bp.post("/resend_confirmation")
def resend_confirmation():
    form = ResendConfirmationForm()
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = (
                db_session
                .query(User)
                .filter(User.email == form.email.data)
                .one_or_none()
            )
            if user is not None:
                send_confirmation_email(user)
                timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
                flash((
                    "Please click on the confirmation link just sent "
                    f"to your email address within {timeout} hours "
                    "to complete your registration"
                ))
                return redirect(url_for("intro_bp.home"))
    return render_template("resend_confirmation.html", form=form)


@auth_bp.get("/profile/<user_uid>")
@auth_bp.post("/profile/<user_uid>")
@login_required
def profile(user_uid):
    with db_session_manager() as db_session:
        user = (
            db_session
            .query(User)
            .filter(User.user_uid == user_uid)
            .one_or_none()
        )
        if user is None:
            flash("Unknown user")
            abort(404)
        if user.user_uid != current_user.user_uid:
            flash("Can't view profile for other users")
            return redirect("intro_bp.home")
        form = UserProfileForm(obj=user)
        if form.cancel.data:
            return redirect(url_for("intro_bp.home"))
        if form.validate_on_submit():
            user.password = form.password.data
            db_session.commit()
            flash("Your password has been updated")
            return redirect(url_for("intro_bp.home"))
    return render_template("profile.html", form=form)


@auth_bp.get("/request_reset_password")
@auth_bp.post("/request_reset_password")
def request_reset_password():
    if current_user.is_authenticated:
        return redirect("intro_bp.home")
    form = RequestResetPasswordForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = (
                db_session.query(User)
                .filter(User.email == form.email.data)
                .one_or_none()
            )
            if user is not None:
                send_password_reset(user)
                timeout = current_app.config.get("PASSWORD_RESET_TIMEOUT")
                flash(f"Check your email to reset your password within {timeout} minutes")
                return redirect(url_for("intro_bp.home"))
    return render_template("request_reset_password.html", form=form)


@auth_bp.get("/reset_password/<token>")
@auth_bp.post("/reset_password/<token>")
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("intro_bp.home")
    try:
        user_uid = User.verify_reset_token(token)
        with db_session_manager() as db_session:
            user = (
                db_session
                .query(User)
                .filter(User.user_uid == user_uid)
                .one_or_none()
            )
            if user is None:
                flash("Reset token invalid")
                return redirect("intro_bp.home")
            form = ResetPasswordForm()
            if form.cancel.data:
                return redirect(url_for("intro_bp.home"))
            if form.validate_on_submit():
                user.password = form.password.data
                db_session.commit()
                flash("Your password has been reset")
                return redirect(url_for("intro_bp.home"))
    except Exception as e:
        flash(str(e))
        logger.exception(e)
        return redirect("intro_bp.home")
    return render_template("reset_password.html", form=form)


def send_confirmation_email(user):
    """Send a confirmation email to the user to
    confirm and activate their account after
    registering as a new user.

    Args:
        user (User): The user to send the email to

    Returns:
        None
    """
    confirmation_token = user.confirmation_token()
    confirmation_url = url_for(
        "auth_bp.confirm",
        confirmation_token=confirmation_token,
        _external=True
    )
    timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
    to = user.email
    subject = "Confirm Your Email"
    contents = (
        f"""Hi {user.first_name},<br /><br />
        Welcome to MyBlog, please click the link to confirm your email within {timeout} hours:
        {confirmation_url}<br /><br />
        Thank you!
        """
    )
    send_mail(to=to, subject=subject, contents=contents)


def send_password_reset(user):
    """Send a password reset email to the user

    Args:
        user (User object): The database user object
    """
    timeout = current_app.config.get("PASSWORD_RESET_TIMEOUT")
    token = user.get_reset_token(timeout)
    to = user.email
    subject = "Password Reset"
    contents = (
        f"""{user.first_name},
        Click the following link to reset your password within {timeout} minutes:
        {url_for('auth_bp.reset_password', token=token, _external=True)}
        If you haven't requested a password reset ignore this email.
        Sincerely,
        MyBlog
        """
    )
    send_mail(to=to, subject=subject, contents=contents)
