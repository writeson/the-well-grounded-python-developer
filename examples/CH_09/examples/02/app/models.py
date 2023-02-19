from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Flag, auto
from time import time
from uuid import uuid4

import jwt
from flask import current_app
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from . import db


@contextmanager
def db_session_manager(session_close=True):
    """Creates a context manager to use to interact
    with the database session and assure closing
    the session at the end of the scope

    Yields:
        Session: The database session object to use
    """
    try:
        yield db.session
    except Exception:
        db.session.rollback()
        raise
    finally:
        if session_close:
            db.session.close()


def get_uuid():
    """Generate a shortened UUID4 value to use
    as the primary key for database records

    Returns:
        string: A shortened (no '-' characters) UUID4 value
    """
    return uuid4().hex


class User(UserMixin, db.Model):
    """The User class to structure what
    a user looks like for the MyBlog application. This
    capitalizes on the flask_login UserMixin class for
    some default methods. The UserMixin class will be
    used more when users are persisted to a database.
    """
    __tablename__ = "user"
    user_uid = db.Column(db.String, primary_key=True, default=get_uuid)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    hashed_password = db.Column("password", db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )

    def get_id(self):
        return self.user_uid

    @property
    def password(self):
        raise AttributeError("user password can't be read")

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps({"confirm": self.user_uid})

    def confirm_token(self, token):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        with db_session_manager() as db_session:
            confirmation_link_timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
            timeout = confirmation_link_timeout * 60 * 1000
            try:
                data = serializer.loads(token, max_age=timeout)
                if data.get("confirm") != self.user_uid:
                    return False
                self.confirmed = True
                db_session.add(self)
                return True
            except (SignatureExpired, BadSignature):
                return False

    def get_reset_token(self, timeout):
        timeout *= 60
        return jwt.encode(
            {
                "reset_password": self.user_uid,
                "exp": time() + timeout,
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def verify_reset_token(token):
        user_uid = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )["reset_password"]
        return user_uid

    def __repr__(self):
        return f"""
        user_uid: {self.user_uid}
        name: {self.first_name} {self.last_name}
        email: {self.email}
        confirmed: {self.confirmed}
        active: {'True' if self.active else 'False'}
       """
