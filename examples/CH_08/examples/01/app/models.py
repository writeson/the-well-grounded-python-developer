from contextlib import contextmanager
from flask_bcrypt import (
    generate_password_hash,
    check_password_hash
)
from . import db
from flask_login import UserMixin
from uuid import uuid4
from datetime import datetime, timezone


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

    def __repr__(self):
        return f"""
        user_uid: {self.user_uid}
        name: {self.first_name} {self.last_name}
        email: {self.email}
        active: {'True' if self.active else 'False'}
        """
